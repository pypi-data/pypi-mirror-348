#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : resume_generator.py
# @Author: anarchy
# @Date  : 2025/5/12
# @Desc  : 讯飞智能简历生成服务SDK封装

import base64
import hashlib
import hmac
import json
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
from typing import Optional, Dict, Any

import requests
from dwspark.config import Config # 导入配置类
from loguru import logger # 导入日志库

class _ResumeUrl:
    """辅助类，用于解析URL的各个部分。"""
    def __init__(self, host: str, path: str, schema: str):
        self.host = host
        self.path = path
        self.schema = schema

def _parse_request_url(request_url: str) -> Optional[_ResumeUrl]:
    """解析请求URL，返回包含host, path, schema的对象。"""
    try:
        stidx = request_url.index("://")
        host_full = request_url[stidx + 3:]
        schema = request_url[:stidx + 3]
        edidx = host_full.index("/")
        if edidx <= 0:
            logger.error(f"无效的请求URL (斜杠解析错误): {request_url}")
            return None
        path = host_full[edidx:]
        host = host_full[:edidx]
        return _ResumeUrl(host, path, schema)
    except ValueError:
        logger.error(f"无效的请求URL (格式错误): {request_url}")
        return None

class ResumeAuth:
    """处理讯飞智能简历服务API认证URL生成的辅助类。"""
    def __init__(self, api_key: str, api_secret: str):
        """
        初始化简历服务认证处理器。
        :param api_key: 智能简历服务的APIKey。
        :param api_secret: 智能简历服务的APISecret。
        """
        if not api_key or not api_secret:
            raise ValueError("APIKey 和 APISecret 不能为空。")
        self.api_key = api_key
        self.api_secret = api_secret

    def build_auth_url(self, request_url: str, method: str = "POST") -> Optional[str]:
        """生成包含认证参数的完整请求URL。"""
        u = _parse_request_url(request_url)
        if not u:
            return None

        host = u.host
        path = u.path
        now = datetime.now()
        date_header = format_date_time(mktime(now.timetuple())) # RFC1123格式日期
        
        signature_origin = f"host: {host}\ndate: {date_header}\n{method.upper()} {path} HTTP/1.1"
        
        signature_sha = hmac.new(self.api_secret.encode('utf-8'), 
                                 signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha_b64 = base64.b64encode(signature_sha).decode(encoding='utf-8')
        
        authorization_origin = (
            f'api_key="{self.api_key}", algorithm="hmac-sha256", ' \
            f'headers="host date request-line", signature="{signature_sha_b64}"'
        )
        authorization_b64 = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        
        auth_params = {
            "host": host,
            "date": date_header,
            "authorization": authorization_b64
        }
        return f"{request_url}?{urlencode(auth_params)}"

class ResumeGenerator:
    """封装讯飞智能简历生成API的类。"""
    # 服务的基础URL，根据 resume.py demo 中的 host
    BASE_API_URL = "https://cn-huadong-1.xf-yun.com/v1/private/s73f4add9"

    def __init__(self, config: Config):
        """
        初始化智能简历生成器实例。
        :param config: Config对象，包含API凭证 (XF_APPID, XF_APIKEY, XF_APISECRET)。
        :raises ValueError: 如果Config对象中缺少必要的凭证。
        """
        self.appid = getattr(config, 'XF_APPID', None)
        api_key = getattr(config, 'XF_APIKEY', None)
        api_secret = getattr(config, 'XF_APISECRET', None)

        if not self.appid or not api_key or not api_secret:
            raise ValueError("Config对象必须提供 XF_APPID, XF_APIKEY, 和 XF_APISECRET。")
        
        self.auth_handler = ResumeAuth(api_key=api_key, api_secret=api_secret)

    def _build_request_body(self, resume_text: str) -> Dict[str, Any]:
        """构建API请求体。"""
        text_b64 = base64.b64encode(resume_text.encode("utf-8")).decode('utf-8')
        return {
            "header": {
                "app_id": self.appid,
                "status": 3, # 根据demo中的值
            },
            "parameter": {
                "ai_resume": {
                    "resData": {
                        "encoding": "utf8",
                        "compress": "raw",
                        "format": "json" # 期望的响应格式
                    }
                }
            },
            "payload": {
                "reqData": {
                    "encoding": "utf8",
                    "compress": "raw",
                    "format": "plain", # 输入文本的格式
                    "status": 3,       # 根据demo中的值
                    "text": text_b64
                }
            }
        }

    def _handle_api_response(self, response: requests.Response, context: str = "智能简历API请求") -> Optional[bytes]:
        """处理API响应，提取并解码简历数据。"""
        logger.debug(f"{context} - 响应状态码: {response.status_code}, 响应文本: {response.text}")
        try:
            resp_json = response.json()
        except json.JSONDecodeError:
            logger.error(f"{context} - 解析JSON响应失败: {response.text}")
            return None

        header = resp_json.get("header", {})
        api_code = header.get("code")

        if response.status_code == 200 and api_code == 0:
            payload = resp_json.get("payload", {})
            res_data = payload.get("resData", {})
            encoded_text = res_data.get("text")
            if encoded_text:
                try:
                    decoded_resume_bytes = base64.b64decode(encoded_text)
                    logger.info(f"{context} - 成功获取并解码简历数据。")
                    # 尝试将bytes解码为UTF-8字符串显示，实际结果为json格式，字段为img_url和word_url
                    try:
                        generated_resume_text = decoded_resume_bytes.decode('utf-8')
                        logger.info(f"{context} - 成功解码为UTF-8文本，完整内容如下:\n------ 简历开始 ------\n{generated_resume_text}\n------ 简历结束 ------")
                    except UnicodeDecodeError:
                        logger.info(f"{context} - 获取的简历数据不是有效的UTF-8文本 (可能是二进制文件，如PDF)。数据长度: {len(decoded_resume_bytes)} bytes.")
                    return decoded_resume_bytes
                except Exception as e:
                    logger.error(f"{context} - Base64解码简历数据失败: {e}")
                    return None
            else:
                logger.warning(f"{context} - 响应成功但未找到简历数据 (payload.resData.text为空)。")
                return None
        else:
            error_message = header.get("message", "未知错误")
            sid = header.get("sid", "N/A")
            logger.error(f"{context} - 错误: code={api_code}, message='{error_message}', sid='{sid}', 完整响应='{response.text}'")
            return None

    def generate(self, resume_description_text: str) -> Optional[bytes]:
        """
        根据输入的文本描述生成智能简历。
        :param resume_description_text: 用于生成简历的文本描述。
        :return: 生成的简历文件内容 (bytes)，或在失败时返回None。
        """
        auth_url = self.auth_handler.build_auth_url(self.BASE_API_URL, method="POST")
        if not auth_url:
            logger.error("生成认证URL失败，无法继续请求。")
            return None
        
        request_body = self._build_request_body(resume_text=resume_description_text)
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        logger.info(f"向 {self.BASE_API_URL} 发送智能简历生成请求...")
        try:
            response = requests.post(auth_url, json=request_body, headers=headers)
            generated_resume_bytes = self._handle_api_response(response)
            
            return generated_resume_bytes

        except requests.RequestException as e:
            logger.error(f"智能简历生成请求 - 网络错误: {e}")
            return None

# 主模块测试代码
if __name__ == '__main__':
    logger.remove()
    logger.add(lambda msg: print(msg, end=''), format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", level="INFO")
    logger.add("resume_generator.log", rotation="10 MB", retention="3 days", level="DEBUG")

    try:
        logger.info("--- 初始化智能简历生成器测试 ---")
        import os
        # 从环境变量加载凭证 (推荐)
        # 这些是Config类期望的主要凭证
        spark_appid = os.environ.get("SPARKAI_APP_ID")
        spark_apikey = os.environ.get("SPARKAI_API_KEY")
        spark_apisecret = os.environ.get("SPARKAI_API_SECRET")

        if not all([spark_appid, spark_apikey, spark_apisecret]):
            logger.warning("一个或多个星火大模型环境变量 (SPARKAI_APP_ID, SPARKAI_API_KEY, SPARKAI_API_SECRET) 未设置.")
            logger.warning("将使用代码中硬编码的占位符凭证进行测试 (API调用很可能会失败).")
            # 替换为您的真实测试凭证，或确保环境变量已设置
            spark_appid = "06ebab34"  # 替换: 您的有效AppID
            spark_apisecret = "YzI4YjlmNGFhYjFmYTYyYWNlY2UyOWM4" # 替换: 您的有效APISecret
            spark_apikey = "31f704523a9c6d75f8aa7671e318e64b" # 替换: 您的有效APIKey
            if spark_appid == "06ebab34":
                 print("\n*****************************************************************")
                 print("警告: 智能简历服务 (通过Config) 正在使用占位符凭证。")
                 print("请设置 SPARKAI_APP_ID, SPARKAI_API_KEY, SPARKAI_API_SECRET 环境变量。")
                 print("*****************************************************************\n")
        
        # Config 只接受 appid, apikey, apisecret
        test_config = Config(
            appid=spark_appid, 
            apikey=spark_apikey, 
            apisecret=spark_apisecret
        )
        
        resume_gen = ResumeGenerator(config=test_config)
        logger.info("智能简历生成器初始化成功.")

        # --- 演示: 生成简历 ---
        logger.info("\n--- 演示: 根据文本描述生成智能简历 ---")
        # 从原始demo获取的示例描述
        description = """姓名：张三，年龄：28岁，教育经历：2018年本科毕业于合肥工业大学；工作经历：java开发工程师..."""
        logger.info(f"输入的简历描述: \n{description}")
        
        generated_resume_bytes = resume_gen.generate(resume_description_text=description)
        
        if generated_resume_bytes:
            logger.info(f"智能简历API调用成功，接收到 {len(generated_resume_bytes)} bytes 的数据。")
            try:
                response_str = generated_resume_bytes.decode('utf-8')
                response_json = json.loads(response_str)
                logger.info("API响应内容 (格式化):")
                # 使用logger.info打印格式化的JSON，Loguru能很好地处理多行消息
                logger.info(f"\n{json.dumps(response_json, indent=2, ensure_ascii=False)}")
                
                # 您可以根据需要取消注释以下代码，以提取并单独记录特定字段：
                if "links" in response_json and isinstance(response_json.get("links"), list):
                    logger.info("提取到的链接详情:")
                    for i, link_info in enumerate(response_json["links"]):
                        img_url = link_info.get("img_url")
                        word_url = link_info.get("word_url")
                        logger.info(f"  链接组 {i+1}:")
                        logger.info(f"    图片URL: {img_url}")
                        logger.info(f"    文档URL: {word_url}")

            except UnicodeDecodeError:
                logger.error("解码API响应失败：响应内容非UTF-8编码。")
            except json.JSONDecodeError:
                logger.error("解析API响应JSON失败：响应内容非标准JSON格式。")
            except Exception as e:
                logger.error(f"处理或显示API响应时发生未知错误: {e}", exc_info=True)
        else:
            logger.warning("智能简历生成API调用失败或未返回数据 (generate() 方法返回 None)。")

        logger.info("\n--- 智能简历生成器演示流程结束 ---")

    except ValueError as ve:
        logger.error(f"配置或参数错误: {ve}")
    except requests.exceptions.RequestException as re:
        logger.error(f"网络请求错误: {re}")
    except Exception as e:
        logger.error(f"测试过程中发生意外错误: {e}", exc_info=True) 