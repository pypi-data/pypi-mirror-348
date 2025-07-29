#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : audio_2_text.py
# @Author: Richard Chiming Xu
# @Date  : 2025/5/13
# @Desc  : 中英语音识别
import _thread as thread
import time
from time import mktime
from loguru import logger
import websocket

import base64
import datetime
import hashlib
import hmac
import json
import ssl
from datetime import datetime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

from dwspark.config import Config

STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识


class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, AudioFile):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.AudioFile = AudioFile
        self.iat_params = {
            "domain": "slm", "language": "zh_cn", "accent": "mandarin","dwa":"wpgs", "result":
                {
                    "encoding": "utf8",
                    "compress": "raw",
                    "format": "plain"
                }
        }

    # 生成url
    def create_url(self):
        url = 'ws://iat.xf-yun.com/v1'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "iat.xf-yun.com" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v1 " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "iat.xf-yun.com"
        }
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)

        return url

class Audio2Text():
    def __init__(self, config: Config, model_url: str = 'wss://iat.xf-yun.com/v1'):
        self.appid = config.XF_APPID
        self.apikey = config.XF_APIKEY
        self.apisecret = config.XF_APISECRET
        self.model_url = model_url

    def recognize(self, audio_path: str) -> str:
        wsParam = Ws_Param(APPID=self.appid, APISecret=self.apisecret, APIKey=self.apikey, AudioFile=audio_path)
        websocket.enableTrace(False)
        wsUrl = wsParam.create_url()
        ws = websocket.WebSocketApp(wsUrl, on_message=self.__on_message, on_error=self.__on_error, on_close=self.__on_close)
        ws.on_open = self.__on_open
        ws.wsParam = wsParam
        ws.last_result = ''
        ws.result = ''
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        return ws.result

    # 收到websocket消息的处理
    def __on_message(self, ws, message):
        message = json.loads(message)
        code = message["header"]["code"]
        status = message["header"]["status"]
        if code != 0:
            logger.error(f"请求错误：{code}")
            ws.close()
        else:

            payload = message.get("payload")
            if payload and status != 2:
                text = payload["result"]["text"]
                text = json.loads(str(base64.b64decode(text), "utf8"))
                text_ws = text['ws']
                ws.last_result = ''.join([j["w"] for i in text_ws for j in i["cw"]])

            if status == 2:
                text = payload["result"]["text"]
                text = json.loads(str(base64.b64decode(text), "utf8"))
                text_ws = text['ws']
                if len(ws.last_result) != len(text_ws):
                    ws.result = ws.last_result + text_ws[-1]['cw'][-1]['w']
                else:
                    ws.result = ''.join([j["w"] for i in text_ws for j in i["cw"]])
                ws.close()


    # 收到websocket错误的处理
    def __on_error(self, ws, error):
        logger.error(error)


    # 收到websocket关闭的处理
    def __on_close(self, ws, close_status_code, close_msg):
        logger.info("### socket closed ###")


    # 收到websocket连接建立的处理
    def __on_open(self, ws):
        wsParam = ws.wsParam
        def run(*args):
            frameSize = 1280  # 每一帧的音频大小
            intervel = 0.04  # 发送音频间隔(单位:s)
            status = STATUS_FIRST_FRAME  # 音频的状态信息，标识音频是第一帧，还是中间帧、最后一帧

            with open(wsParam.AudioFile, "rb") as fp:
                while True:

                    buf = fp.read(frameSize)
                    audio = str(base64.b64encode(buf), 'utf-8')

                    # 文件结束
                    if not buf:
                        status = STATUS_LAST_FRAME
                    # 第一帧处理
                    if status == STATUS_FIRST_FRAME:

                        d = {"header":
                            {
                                "status": 0,
                                "app_id": wsParam.APPID
                            },
                            "parameter": {
                                "iat": wsParam.iat_params
                            },
                            "payload": {
                                "audio":
                                    {
                                        "audio": audio, "sample_rate": 16000, "encoding": "lame"
                                    }
                            }}
                        d = json.dumps(d)
                        ws.send(d)
                        status = STATUS_CONTINUE_FRAME
                    # 中间帧处理
                    elif status == STATUS_CONTINUE_FRAME:
                        d = {"header": {"status": 1,
                                        "app_id": wsParam.APPID},
                             "parameter": {
                                 "iat": wsParam.iat_params
                             },
                             "payload": {
                                 "audio":
                                     {
                                         "audio": audio, "sample_rate": 16000, "encoding": "lame"
                                     }}}
                        ws.send(json.dumps(d))
                    # 最后一帧处理
                    elif status == STATUS_LAST_FRAME:
                        d = {"header": {"status": 2,
                                        "app_id": wsParam.APPID
                                        },
                             "parameter": {
                                 "iat": wsParam.iat_params
                             },
                             "payload": {
                                 "audio":
                                     {
                                         "audio": audio, "sample_rate": 16000, "encoding": "lame"
                                     }}}
                        ws.send(json.dumps(d))
                        break

                    # 模拟音频采样间隔
                    time.sleep(intervel)


        thread.start_new_thread(run, ())

if __name__ == '__main__':
    config = Config()
    model = Audio2Text(config)
    logger.info(model.recognize('./demo.mp3'))