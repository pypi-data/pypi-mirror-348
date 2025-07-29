#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : llm_embedding.py
# @Author: hcy
# @Date  : 2025/5/17
# @Desc  : 讯飞星火大模型Embedding服务SDK封装

import base64
import hashlib
import hmac
import json
import time
from typing import Optional, Dict, Any, List, Union

import numpy as np
import requests
from dwspark.config import Config
from loguru import logger


class ApiAuthAlgorithm:
    """处理讯飞星火Embedding服务API认证的辅助类。"""
    
    def __init__(self, app_id: str, api_secret: str, api_key: str):
        """
        初始化星火Embedding服务认证处理器。
        :param app_id: 应用ID
        :param api_secret: API密钥
        :param api_key: API Key
        """
        if not app_id or not api_secret or not api_key:
            raise ValueError("应用ID、API密钥和API Key不能为空。")
        self.app_id = app_id
        self.api_secret = api_secret
        self.api_key = api_key
    
    def generate_auth_params(self, host: str, path: str) -> Dict[str, str]:
        """
        生成鉴权参数
        :param host: 请求的主机名
        :param path: 请求的路径
        :return: 包含鉴权参数的字典
        """
        try:
            # 生成RFC1123格式的日期
            cur_time = time.gmtime()
            date = time.strftime("%a, %d %b %Y %H:%M:%S GMT", cur_time)
            
            # 构建签名原文
            signature_origin = f"host: {host}\ndate: {date}\nPOST {path} HTTP/1.1"
            
            # 使用hmac-sha256算法结合API Secret对签名原文签名
            signature_sha = hmac.new(
                self.api_secret.encode('utf-8'),
                signature_origin.encode('utf-8'),
                digestmod=hashlib.sha256
            ).digest()
            
            # 得到签名
            signature = base64.b64encode(signature_sha).decode('utf-8')
            
            # 构建authorization_origin
            authorization_origin = (
                f'api_key="{self.api_key}", algorithm="hmac-sha256", '
                f'headers="host date request-line", signature="{signature}"'
            )
            
            # 生成最终的authorization
            authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode('utf-8')
            
            return {
                "authorization": authorization,
                "date": date,
                "host": host
            }
        except Exception as e:
            logger.error(f"生成鉴权参数失败: {e}")
            raise


class LLMEmbedding:
    """封装讯飞星火大模型Embedding API的类。"""
    # 服务的基础URL和路径
    BASE_HOST = "emb-cn-huabei-1.xf-yun.com"
    BASE_PATH = "/"
    
    def __init__(self, config: Config):
        """
        初始化星火Embedding实例。
        :param config: Config对象，包含API凭证 (XF_APPID, XF_APISECRET, XF_APIKEY)。
        :raises ValueError: 如果Config对象中缺少必要的凭证。
        """
        self.app_id = getattr(config, 'XF_APPID', None)
        self.api_secret = getattr(config, 'XF_APISECRET', None)
        self.api_key = getattr(config, 'XF_APIKEY', None)
        
        if not self.app_id or not self.api_secret or not self.api_key:
            raise ValueError("Config对象必须提供 XF_APPID、XF_APISECRET 和 XF_APIKEY。")
        
        self.auth = ApiAuthAlgorithm(app_id=self.app_id, api_secret=self.api_secret, api_key=self.api_key)
    
    def _prepare_request_data(self, text: str, domain: str = "query") -> Dict:
        """
        准备请求数据
        :param text: 需要向量化的文本
        :param domain: 向量化领域，可选值：query(用户问题向量化)、para(知识原文向量化)
        :return: 请求数据字典
        """
        # 构建消息内容
        message_content = {
            "messages": [
                {
                    "content": text,
                    "role": "user"
                }
            ]
        }
        
        # 将消息内容转为JSON字符串，然后进行base64编码
        message_text = base64.b64encode(json.dumps(message_content).encode('utf-8')).decode('utf-8')
        
        # 构建完整请求数据
        request_data = {
            "header": {
                "app_id": self.app_id,
                "uid": "39769795890",  # 固定值或可配置
                "status": 3,  # 一次传完
            },
            "parameter": {
                "emb": {
                    "domain": domain,  # query 或 para
                    "feature": {
                        "encoding": "utf8",
                        "compress": "raw",
                        "format": "plain"
                    }
                }
            },
            "payload": {
                "messages": {
                    "encoding": "utf8",
                    "compress": "raw",
                    "format": "json",
                    "status": 3,
                    "text": message_text
                }
            }
        }
        
        return request_data
    
    def _handle_response(self, response: requests.Response, context: str = "星火Embedding API请求") -> Optional[Dict]:
        """
        处理API响应
        :param response: 响应对象
        :param context: 上下文描述，用于日志
        :return: 处理后的响应数据，失败时返回None
        """
        logger.debug(f"{context} - 响应状态码: {response.status_code}, 响应文本: {response.text}")
        
        try:
            resp_json = response.json()
        except json.JSONDecodeError:
            logger.error(f"{context} - 解析JSON响应失败: {response.text}")
            return None
        
        # 检查响应状态
        header = resp_json.get("header", {})
        code = header.get("code", -1)
        
        if code == 0:  # 成功
            logger.info(f"{context} - 请求成功")
            return resp_json
        else:
            # 错误处理
            message = header.get("message", "未知错误")
            sid = header.get("sid", "N/A")
            logger.error(f"{context} - 错误: code={code}, message='{message}', sid='{sid}'")
            return None
    
    def get_embedding(self, text: str, domain: str = "query") -> Optional[List[float]]:
        """
        获取文本的向量表示
        :param text: 需要向量化的文本
        :param domain: 向量化领域，可选值：query(用户问题向量化)、para(知识原文向量化)
        :return: 向量表示（2560维浮点数数组），失败时返回None
        """
        if not text:
            logger.warning("获取文本向量 - 文本内容为空")
            return None
            
        # 准备请求数据
        request_data = self._prepare_request_data(text, domain)
        
        try:
            # 获取鉴权参数
            auth_params = self.auth.generate_auth_params(self.BASE_HOST, self.BASE_PATH)
            
            # 构建请求URL
            from urllib.parse import urlencode
            url = f"https://{self.BASE_HOST}{self.BASE_PATH}?{urlencode(auth_params)}"
            
            # 设置请求头
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            # 发送请求
            response = requests.post(url, headers=headers, json=request_data)
            result = self._handle_response(response, "获取文本向量")
            
            if result:
                # 从响应中提取向量数据
                payload = result.get("payload", {})
                feature = payload.get("feature", {})
                text_base64 = feature.get("text", "")
                
                if text_base64:
                    # 解码base64数据为向量
                    vector_bytes = base64.b64decode(text_base64)
                    # 将字节转换为浮点数数组（假设是2560维的float32数组）
                    vector = np.frombuffer(vector_bytes, dtype=np.float32).tolist()
                    return vector
                else:
                    logger.error("获取文本向量 - 响应中没有向量数据")
            
            return None
        except Exception as e:
            logger.error(f"获取文本向量 - 错误: {e}")
            return None
    
    def get_embeddings(self, texts: List[str], domain: str = "query") -> List[Optional[List[float]]]:
        """
        批量获取多个文本的向量表示
        :param texts: 需要向量化的文本列表
        :param domain: 向量化领域，可选值：query(用户问题向量化)、para(知识原文向量化)
        :return: 向量表示列表，每个元素是一个2560维浮点数数组或None（如果该文本处理失败）
        """
        results = []
        for text in texts:
            vector = self.get_embedding(text, domain)
            results.append(vector)
        return results
    
    def calculate_similarity(self, text1: str, text2: str, domain: str = "query") -> Optional[float]:
        """
        计算两段文本的相似度
        :param text1: 第一段文本
        :param text2: 第二段文本
        :param domain: 向量化领域，可选值：query(用户问题向量化)、para(知识原文向量化)
        :return: 相似度分数（0-1之间的浮点数），失败时返回None
        """
        # 获取两段文本的向量表示
        vector1 = self.get_embedding(text1, domain)
        vector2 = self.get_embedding(text2, domain)
        
        if vector1 is None or vector2 is None:
            return None
        
        # 计算余弦相似度
        try:
            vector1_np = np.array(vector1)
            vector2_np = np.array(vector2)
            
            # 计算点积
            dot_product = np.dot(vector1_np, vector2_np)
            
            # 计算范数
            norm1 = np.linalg.norm(vector1_np)
            norm2 = np.linalg.norm(vector2_np)
            
            # 计算余弦相似度
            similarity = dot_product / (norm1 * norm2)
            
            return float(similarity)
        except Exception as e:
            logger.error(f"计算文本相似度 - 错误: {e}")
            return None


if __name__ == '__main__':
    # 初始化配置
    conf = Config()
    
    # 初始化Embedding实例
    model = LLMEmbedding(conf)
    
    # 测试文本向量化
    logger.info('----------测试文本向量化----------')
    text1 = '今天天气真不错'
    text2 = '今日的天气非常好'
    text3 = '人工智能技术发展迅速'
    
    # 获取单个文本的向量表示
    logger.info('获取单个文本的向量表示：')
    vector = model.get_embedding(text1)
    if vector:
        logger.info(f'向量维度: {len(vector)}')
    
    # 批量获取多个文本的向量表示
    logger.info('批量获取多个文本的向量表示：')
    vectors = model.get_embeddings([text1, text2, text3])
    for i, vec in enumerate(vectors, 1):
        if vec:
            logger.info(f'文本{i}向量维度: {len(vec)}')
    
    # 测试文本相似度计算
    logger.info('----------测试文本相似度计算----------')
    # 计算语义相近的两段文本的相似度
    similarity1 = model.calculate_similarity(text1, text2)
    if similarity1 is not None:
        logger.info(f'相似文本的相似度: {similarity1}')
    
    # 计算语义不同的两段文本的相似度
    similarity2 = model.calculate_similarity(text1, text3)
    if similarity2 is not None:
        logger.info(f'不相似文本的相似度: {similarity2}')