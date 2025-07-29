#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : text_2_audio.py
# @Author: Richard Chiming Xu
# @Date  : 2025/5/12
# @Desc  : 语音合成
import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread
import os
from loguru import logger

from dwspark.config import Config


class Url:
    def __init__(this, host, path, schema):
        this.host = host
        this.path = path
        this.schema = schema
        pass


class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, Text):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.Text = Text

        # 公共参数(common)
        # 在这里通过res_id 来设置通过哪个音库合成
        self.CommonArgs = {"app_id": self.APPID, "status": 2}
        # 业务参数(business)，更多个性化参数可在官网查看
        self.BusinessArgs = {
            "tts": {
                "vcn": "x4_lingxiaoxuan_oral",  # 发音人参数，更换不同的发音人会有不同的音色效果
                "volume": 50,  # 设置音量大小
                "rhy": 0,  # 是否返回拼音标注		0:不返回拼音, 1:返回拼音（纯文本格式，utf8编码）
                "speed": 50,  # 设置合成语速，值越大，语速越快
                "pitch": 50,  # 设置振幅高低，可通过该参数调整效果
                "bgs": 0,  # 背景音	0:无背景音, 1:内置背景音1, 2:内置背景音2
                "reg": 0,  # 英文发音方式 	0:自动判断处理，如果不确定将按照英文词语拼写处理（缺省）, 1:所有英文按字母发音, 2:自动判断处理，如果不确定将按照字母朗读
                "rdn": 0,  # 合成音频数字发音方式	0:自动判断, 1:完全数值, 2:完全字符串, 3:字符串优先
                "audio": {
                    "encoding": "lame",  # 合成音频格式， lame 合成音频格式为mp3
                    "sample_rate": 24000,  # 合成音频采样率，	16000, 8000, 24000
                    "channels": 1,  # 音频声道数
                    "bit_depth": 16,  # 合成音频位深 ：16, 8
                    "frame_size": 0
                }
            }
        }

        self.Data = {
            "text": {
                "encoding": "utf8",
                "compress": "raw",
                "format": "plain",
                "status": 2,
                "seq": 0,
                "text": str(base64.b64encode(self.Text.encode('utf-8')), "UTF8")  # 待合成文本base64格式
            }
        }

    # calculate sha256 and encode to base64
    def __sha256base64(self, data):
        sha256 = hashlib.sha256()
        sha256.update(data)
        digest = base64.b64encode(sha256.digest()).decode(encoding='utf-8')
        return digest

    def __parse_url(self, requset_url):
        stidx = requset_url.index("://")
        host = requset_url[stidx + 3:]
        schema = requset_url[:stidx + 3]
        edidx = host.index("/")
        if edidx <= 0:
            raise AssembleHeaderException("invalid request url:" + requset_url)
        path = host[edidx:]
        host = host[:edidx]
        u = Url(host, path, schema)
        return u

    # build websocket auth request url
    def assemble_ws_auth_url(self, requset_url, method="GET"):
        u = self.__parse_url(requset_url)
        host = u.host
        path = u.path
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        # date = "Thu, 12 Dec 2019 01:57:27 GMT"
        signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1".format(host, date, method, path)
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        values = {
            "host": host,
            "date": date,
            "authorization": authorization
        }

        return requset_url + "?" + urlencode(values)


class AssembleHeaderException(Exception):
    def __init__(self, msg):
        self.message = msg


class Text2Audio():
    def __init__(self, config: Config, model_url: str = 'wss://cbm01.cn-huabei-1.xf-yun.com/v1/private/mcd9m97e6'):
        self.appid = config.XF_APPID
        self.apikey = config.XF_APIKEY
        self.apisecret = config.XF_APISECRET
        self.model_url = model_url

    def generate(self, text: str, audio_path: str) -> bool:
        wsParam = Ws_Param(APPID=self.appid, APISecret=self.apisecret, APIKey=self.apikey, Text=text)
        websocket.enableTrace(False)
        # 创建连接
        wsUrl = wsParam.assemble_ws_auth_url(self.model_url, "GET")
        ws = websocket.WebSocketApp(wsUrl, on_open=self.__on_open, on_message=self.__on_message, on_error=self.__on_error, on_close=self.__on_close)
        # 写入参数
        ws.wsParam = wsParam
        ws.audio_path = audio_path
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        return True

    def __on_message(self, ws, message):
        try:

            message = json.loads(message)

            code = message["header"]["code"]
            sid = message["header"]["sid"]
            if ("payload" in message):
                audio = message["payload"]["audio"]['audio']
                audio = base64.b64decode(audio)
                status = message["payload"]['audio']["status"]
                if status == 2:
                    logger.info("关闭连接，语音合成结束.")
                    ws.close()
                if code != 0:
                    errMsg = message["message"]
                    logger.error("sid:%s call error:%s code is:%s" % (sid, errMsg, code))
                else:
                    with open(ws.audio_path, 'ab') as f:  # 这里文件后缀名，需要和业务参数audio.encoding 对应
                        f.write(audio)

        except Exception as e:
            logger.error("receive msg,but parse exception:", e)

    # 收到websocket错误的处理
    def __on_error(self, ws, error):
        # return 0
        logger.error("### error:", error)

    # 收到websocket关闭的处理
    def __on_close(self, ws, ts, end):
        return 0

    # 收到websocket连接建立的处理
    def __on_open(self, ws):
        def run(ws):
            d = {"header": ws.wsParam.CommonArgs,
                 "parameter": ws.wsParam.BusinessArgs,
                 "payload": ws.wsParam.Data,
                 }
            d = json.dumps(d)
            logger.info("------>开始发送文本数据")
            ws.send(d)
            if os.path.exists(ws.audio_path):
                os.remove(ws.audio_path)

        thread.start_new_thread(run, (ws, ))

if __name__ == '__main__':
    config = Config()
    text2audio = Text2Audio(config)
    text2audio.generate("你好，这里是datawhale团队，请问有什么可以帮你的？", "./demo.mp3")