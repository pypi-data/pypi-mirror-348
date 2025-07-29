#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : text_2_picture.py
# @Author: Richard Chiming Xu
# @Date  : 2025/5/14
# @Desc  : 文本生成图片
import time

import requests
from datetime import datetime
from wsgiref.handlers import format_date_time
from time import mktime
import hashlib
import base64
import hmac
from urllib.parse import urlencode
import json
from PIL import Image
from io import BytesIO
from dwspark.config import Config
from loguru import logger

class AssembleHeaderException(Exception):
    def __init__(self, msg):
        self.message = msg


class Url:
    def __init__(this, host, path, schema):
        this.host = host
        this.path = path
        this.schema = schema
        pass



class Text2Picture(object):
    def __init__(self, config:Config, model_url:str = 'http://spark-api.cn-huabei-1.xf-yun.com/v2.1/tti'):
        self.appid = config.XF_APPID
        self.apikey = config.XF_APIKEY
        self.apisecret = config.XF_APISECRET
        self.model_url = model_url

    def generate(self, text: str, save_path: str) -> str:
        # 生成地址和请求体
        url = self.__assemble_ws_auth_url(method='POST')
        content = self.__getBody(self.appid, text)
        # 发起请求
        response = requests.post(url,json=content,headers={'content-type': "application/json"}).text
        # 解释结果
        data = json.loads(response)
        code = data['header']['code']
        if code != 0:
            logger.error(f'请求错误: {code}, {data}')
            return ''
        else:
            text = data["payload"]["choices"]["text"]
            imageContent = text[0]
            imageBase = imageContent["content"]
            imageName = data['header']['sid']
            savePath = f"{save_path}/{imageName}.jpg"
            self.__base64_to_image(imageBase,savePath)
            logger.info("图片保存路径：" + savePath)
            return savePath


    #将base64 的图片数据存在本地
    def __base64_to_image(self, base64_data, save_path):
        # 解码base64数据
        img_data = base64.b64decode(base64_data)

        # 将解码后的数据转换为图片
        img = Image.open(BytesIO(img_data))

        # 保存图片到本地
        img.save(save_path)
    def __getBody(self, appid,text):
        body= {
            "header": {
                "app_id": appid,
                "uid":"123456789"
            },
            "parameter": {
                "chat": {
                    "domain": "general",
                    "temperature":0.5,
                    "max_tokens":4096
                }
            },
            "payload": {
                "message":{
                    "text":[
                        {
                            "role":"user",
                            "content":text
                        }
                    ]
                }
            }
        }
        return body


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
    def __assemble_ws_auth_url(self, method="GET"):
        u = self.__parse_url(self.model_url)
        host = u.host
        path = u.path
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        # print(date)
        # date = "Thu, 12 Dec 2019 01:57:27 GMT"
        signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1".format(host, date, method, path)
        # print(signature_origin)
        signature_sha = hmac.new(self.apisecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.apikey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # print(authorization_origin)
        values = {
            "host": host,
            "date": date,
            "authorization": authorization
        }

        return self.model_url + "?" + urlencode(values)

if __name__ == '__main__':
    conf = Config()
    model = Text2Picture(conf)
    img_path = model.generate("请生成一张关于机器学习的图片", "D://")
    print(img_path)
