#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : MultiLang.py
# @Author: Richard Chiming Xu
# @Date  : 2025/5/10
# @Desc  : 多语种大模型

from typing import List, Iterable

from dwspark.config import Config
from loguru import logger


import _thread as thread
import queue # Added import

import json
import ssl


import websocket



import base64
import datetime
import hashlib
import hmac
from urllib.parse import urlparse
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, Spark_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(Spark_url).netloc
        self.path = urlparse(Spark_url).path
        self.Spark_url = Spark_url

    # 生成url
    def create_url(self):
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"

        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        # 拼接鉴权参数，生成url
        url = self.Spark_url + '?' + urlencode(v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        return url


class MultiLang():
    def __init__(self, config: Config, domain: str = 'multilang', model_url: str = 'wss://spark-api-n.xf-yun.com/v1.1/chat_multilang', stream:bool=False):
        '''
        初始化模型
        :param config: 项目配置文件
        :param domain: 调用模型
        :param llm_url: 模型地址
        :param stream: 是否启用流式调用
        '''

        self.wsParam = Ws_Param(config.XF_APPID, config.XF_APIKEY, config.XF_APISECRET, model_url)
        self.domain = domain
        self.stream = stream # Indicates the intended mode of this instance
        self.appid = config.XF_APPID
        self.apikey = config.XF_APIKEY
        self.apisecret = config.XF_APISECRET

        # For batch mode, to store the full response
        self.full_response_content = "" 
        # self.message_queue is no longer needed at instance level for stream if queue is per-call

    def generate(self, msgs: str | List) -> str:
        '''
        批式调用
        :param msgs: 发送消息，接收字符串或列表形式的消息
        :return:
        '''
        if self.stream is True: # Instance configured for streaming
            raise Exception('模型初始化为流式输出，请调用generate_stream方法')
        
        self.full_response_content = "" # Reset for current call
        messages = self.__trans_msgs(msgs)
        
        websocket.enableTrace(False)
        wsUrl = self.wsParam.create_url()
        
        ws = websocket.WebSocketApp(wsUrl, 
                                    on_message=self.__on_message, 
                                    on_error=self.__on_error, 
                                    on_close=self.__on_close, 
                                    on_open=self.__on_open)

        ws.appid = self.appid
        ws.messages = messages 
        ws.domain = self.domain
        # Add a flag to ws to indicate it's a batch call for callbacks
        ws.is_batch_call = True
        # Give callback access to parent's full_response_content via parent_instance
        # This allows __on_message to update self.full_response_content
        ws.parent_instance = self 

        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        return self.full_response_content

    def generate_stream(self, msgs: str | List) -> Iterable[str]:
        '''
        流式调用
        :param msgs: 发送消息，接收字符串或列表形式的消息
        :return:
        '''
        if not self.stream: # Instance configured for batch
            raise Exception('模型初始化为批式输出，请调用generate方法')

        current_call_queue = queue.Queue() # New queue for this specific call

        messages = self.__trans_msgs(msgs)
        websocket.enableTrace(False)
        wsUrl = self.wsParam.create_url()
        
        ws = websocket.WebSocketApp(wsUrl, 
                                    on_message=self.__on_message, 
                                    on_error=self.__on_error, 
                                    on_close=self.__on_close, 
                                    on_open=self.__on_open)

        ws.appid = self.appid
        ws.domain = self.domain
        ws.messages = self.__trans_msgs(msgs)
        # Add a flag and the queue to ws for callbacks
        ws.is_batch_call = False
        ws.message_queue = current_call_queue 


        # Run WebSocket in a separate thread
        thread.start_new_thread(self._run_ws_thread, (ws,))

        try:
            while True:
                chunk = current_call_queue.get() # Blocks until an item is available
                if chunk is None: # Sentinel for end of stream
                    break
                if isinstance(chunk, Exception): # Propagate exceptions
                    raise chunk
                yield chunk
        finally:
            # Ensure WebSocket is closed if the generator is exited
            if ws and ws.sock and ws.sock.connected:
                ws.close()

    def _run_ws_thread(self, ws):
        # Helper method to run ws.run_forever in a new thread and handle potential errors
        try:
            ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        except Exception as e:
            # If run_forever itself throws an exception (e.g., connection issue before callbacks)
            # Put this into the queue for the generator to pick up.
            if hasattr(ws, 'message_queue') and ws.message_queue is not None:
                ws.message_queue.put(e)
            else: # Should not happen for stream calls, but log defensively
                logger.error(f"WebSocket run_forever error in detached thread (non-stream context or misconfiguration): {e}")

    def __trans_msgs(self, msg: str):
        '''
        内部方法，将字符串转换为消息
        :param msgs: 字符串
        :return:
        '''
        if isinstance(msg, str):
            messages = [dict(role="user", content=msg)]
        else:
            messages = msg
        return messages

    # 收到websocket消息的处理
    def __on_message(self, ws, message):
        # print(message) # Uncomment for debugging
        data = json.loads(message)
        code = data['header']['code']

        if code != 0:
            error_msg = f'请求错误: {code}, {data.get("header", {}).get("message", "Unknown error")}'
            logger.error(error_msg)
            if hasattr(ws, 'is_batch_call') and ws.is_batch_call:
                ws.close() # For batch, close and generate() will return what's accumulated
            elif hasattr(ws, 'message_queue') and ws.message_queue: # Streaming
                ws.message_queue.put(RuntimeError(error_msg))
            return

        choices = data["payload"]["choices"]
        status = choices["status"]
        content_chunk = choices["text"][0]["content"]

        if hasattr(ws, 'is_batch_call') and ws.is_batch_call:
            if hasattr(ws, 'parent_instance') and hasattr(ws.parent_instance, 'full_response_content'):
                 ws.parent_instance.full_response_content += content_chunk
            if status == 2:
                ws.close()
        elif hasattr(ws, 'message_queue') and ws.message_queue: # Streaming
            ws.message_queue.put(content_chunk)
            if status == 2:
                ws.message_queue.put(None) # End of stream sentinel
                # ws.close() # Let run_forever handle closure or the finally block in generate_stream
        else:
             logger.warning("__on_message called on a WebSocket without proper mode (batch/stream) indicators or queue.")


    # 收到websocket错误的处理
    def __on_error(self, ws, error):
        logger.error(f"### WebSocket error: {error}")
        if hasattr(ws, 'is_batch_call') and ws.is_batch_call:
            # For batch, error means the call failed. generate() will return what it has.
            # ws.close() is usually handled by the library upon error before on_close
            pass
        elif hasattr(ws, 'message_queue') and ws.message_queue: # Streaming
            ws.message_queue.put(error)


    # 收到websocket关闭的处理
    def __on_close(self, ws, close_status_code, close_msg): # Corrected signature
        # For streaming, ensure the generator loop terminates if not already done by a sentinel or error
        if hasattr(ws, 'is_batch_call') and not ws.is_batch_call: # Check it's a stream call
            if hasattr(ws, 'message_queue') and ws.message_queue:
                try:
                    ws.message_queue.put_nowait(None) 
                except queue.Full:
                    # Queue is full, likely means it's being processed or already has a sentinel/error.
                    pass
                except AttributeError: # Should not happen if ws.message_queue is always set for stream
                    pass


    # 收到websocket连接建立的处理
    def __on_open(self, ws):
        # Pass ws instance to __run, so it can access ws.appid, ws.messages, ws.domain
        thread.start_new_thread(self.__run, (ws,))


    def __run(self, ws, *args): # ws object is passed here
        # Construct params using attributes from the ws object itself
        data_payload = self.gen_params(appid=ws.appid, messages=ws.messages, domain=ws.domain)
        data = json.dumps(data_payload, ensure_ascii=False)
        ws.send(data)

    def gen_params(self, appid, messages, domain):
        """
        通过appid和用户的提问来生成请参数
        """

        data = {
            "header": {
                "app_id": appid,
            },
            "parameter": {
                "chat": {
                    "domain": domain
                }
            },
            "payload": {
                "message": {
                    "text": messages
                }
            }
        }
        return data

if __name__ == '__main__':
    # 初始化配置
    conf = Config()
    # 模拟问题
    message = [{"role": "system", "content": "あなたはとても専門的な日本語の国語の先生で、文才が華麗です。"},{"role": "user", "content": '100字の作文を書いてください。'}]
    '''
        批式调用
    '''
    logger.info('----------批式调用----------')
    model = MultiLang(conf, stream=False)
    logger.info(model.generate(message))
    '''
        流式调用
    '''
    logger.info('----------流式调用----------')
    model = MultiLang(conf, stream=True)
    for chunk in model.generate_stream(message):
        logger.info(chunk)




