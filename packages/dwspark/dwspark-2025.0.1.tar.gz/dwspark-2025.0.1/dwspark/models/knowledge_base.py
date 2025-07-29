#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : knowledge_base.py
# @Author: hcy
# @Date  : 2025/5/16
# @Desc  : 讯飞星火知识库服务SDK封装

import os
import base64
import hashlib
import hmac
import json
import time
import websocket
import threading
from typing import Optional, Dict, Any, List, Callable, BinaryIO, Union
from urllib.parse import urlencode

import requests
from dwspark.config import Config
from loguru import logger


class ApiAuthAlgorithm:
    """处理讯飞星火知识库服务API认证的辅助类。"""
    
    def __init__(self, app_id: str, secret: str):
        """
        初始化星火知识库服务认证处理器。
        :param app_id: 应用ID。
        :param secret: 应用秘钥。
        """
        if not app_id or not secret:
            raise ValueError("应用ID和秘钥不能为空。")
        self.app_id = app_id
        self.secret = secret
        
    def get_signature(self, ts: int) -> str:
        """
        获取签名
        :param ts: 时间戳，单位秒
        :return: 返回签名
        """
        try:
            auth = self._md5(self.app_id + str(ts))
            return self._hmac_sha1_encrypt(auth, self.secret)
        except Exception as e:
            logger.error(f"生成签名失败: {e}")
            return ""
    
    def _hmac_sha1_encrypt(self, encrypt_text: str, encrypt_key: str) -> str:
        """
        sha1加密
        :param encrypt_text: 加密文本
        :param encrypt_key: 加密键
        :return: 加密结果
        """
        try:
            data = encrypt_key.encode('utf-8')
            secret_key = hmac.new(data, encrypt_text.encode('utf-8'), digestmod=hashlib.sha1)
            return base64.b64encode(secret_key.digest()).decode('utf-8')
        except Exception as e:
            logger.error(f"HMAC-SHA1加密失败: {e}")
            raise
    
    def _md5(self, cipher_text: str) -> str:
        """
        MD5加密
        :param cipher_text: 加密文本
        :return: MD5加密结果
        """
        try:
            md5_table = '0123456789abcdef'
            data = cipher_text.encode('utf-8')
            md_inst = hashlib.md5()
            md_inst.update(data)
            md = md_inst.digest()
            
            result = []
            for byte in md:
                result.append(md5_table[byte >> 4 & 0xf])
                result.append(md5_table[byte & 0xf])
            return ''.join(result)
        except Exception as e:
            logger.error(f"MD5加密失败: {e}")
            return ""


class KnowledgeBase:
    """封装讯飞星火知识库API的类。"""
    # 服务的基础URL
    BASE_API_URL = "https://chatdoc.xfyun.cn/openapi/v1"
    # 知识库API的基础URL
    REPO_API_URL = "https://chatdoc.xfyun.cn/openapi/v1"
    
    def __init__(self, config: Config):
        """
        初始化星火知识库实例。
        :param config: Config对象，包含API凭证 (XF_APPID, XF_APISECRET)。
        :raises ValueError: 如果Config对象中缺少必要的凭证。
        """
        self.app_id = getattr(config, 'XF_APPID', None)
        self.secret = getattr(config, 'XF_APISECRET', None)
        
        if not self.app_id or not self.secret:
            raise ValueError("Config对象必须提供 XF_APPID 和 XF_APISECRET。")
        
        self.auth = ApiAuthAlgorithm(app_id=self.app_id, secret=self.secret)
    
    def _get_headers(self) -> Dict[str, str]:
        """
        获取请求头，包含鉴权信息
        :return: 请求头字典
        """
        timestamp = int(time.time())  # 当前时间戳，秒级
        signature = self.auth.get_signature(timestamp)
        
        return {
            "Content-Type": "application/json",
            "appId": self.app_id,
            "timestamp": str(timestamp),
            "signature": signature
        }
    
    def _handle_response(self, response: requests.Response, context: str = "星火知识库API请求") -> Optional[Dict]:
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
        
        # 根据文档，成功响应没有明确的success字段，需要根据状态码和响应内容判断
        if response.status_code == 200:
            logger.info(f"{context} - 请求成功")
            return resp_json
        else:
            # 错误处理，根据实际API响应格式调整
            error_msg = resp_json.get("message", "未知错误")
            logger.error(f"{context} - 错误: {error_msg}")
            return None
    
    def upload_document(self, file_path: str, file_name: Optional[str] = None, parse_type: str = "AUTO", step_by_step: bool = False) -> Optional[str]:
        """
        上传文档到星火知识库
        :param file_path: 文件路径
        :param file_name: 文件名称，如果为None则使用file_path中的文件名
        :param parse_type: 文件解析类型，"AUTO"-服务端智能判断是否需要走OCR，"TEXT"-直接读取文件文本内容，"OCR"-强制走OCR
        :param step_by_step: 是否分步处理，默认False
        :return: 成功时返回文档ID，失败时返回None
        """
        url = f"{self.BASE_API_URL}/file/upload"
        timestamp = int(time.time())
        signature = self.auth.get_signature(timestamp)
        
        # 如果没有提供文件名，则从路径中提取
        if file_name is None:
            import os
            file_name = os.path.basename(file_path)
        
        try:
            # 设置请求头，不包含Content-Type，让requests自动设置
            headers = {
                "appId": self.app_id,
                "timestamp": str(timestamp),
                "signature": signature
            }
            
            # 准备表单数据
            data = {
                "fileType": "wiki",
                "parseType": parse_type,
                "stepByStep": str(step_by_step).lower()
            }
            
            # 准备文件数据
            with open(file_path, 'rb') as f:
                files = {'file': (file_name, f, self._get_content_type(file_name))}
                
                # 发送multipart/form-data请求
                response = requests.post(url, headers=headers, data=data, files=files)
                result = self._handle_response(response, "上传文档")
                if result:
                    return result.get("data", {}).get("fileId")
                return None
        except Exception as e:
            logger.error(f"上传文档 - 错误: {e}")
            return None
    
    def _get_content_type(self, file_name: str) -> str:
        """
        根据文件名获取Content-Type
        :param file_name: 文件名
        :return: Content-Type字符串
        """
        ext = file_name.split('.')[-1].lower()
        content_types = {
            'pdf': 'application/pdf',
            'doc': 'application/msword',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'txt': 'text/plain',
            'md': 'text/markdown'
        }
        return content_types.get(ext, 'application/octet-stream')
    
    def get_document_chunks(self, file_id: str) -> Optional[List[Dict]]:
        """
        获取文件分块内容
        :param file_id: 上传的文件ID
        :return: 文件分块内容列表，失败时返回None
        """
        # 根据文档，接口地址未明确提供，使用通用路径
        url = f"{self.BASE_API_URL}/file/chunks"
        timestamp = int(time.time())
        signature = self.auth.get_signature(timestamp)
        
        # 设置请求头，明确指定Content-Type为application/x-www-form-urlencoded
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "appId": self.app_id,
            "timestamp": str(timestamp),
            "signature": signature
        }
        
        # 使用form-data格式发送请求
        data = {"fileId": file_id}
        
        try:
            response = requests.post(url, headers=headers, data=data)
            result = self._handle_response(response, "获取文件分块内容")
            if result:
                return result.get("data", [])
            return None
        except Exception as e:
            logger.error(f"获取文件分块内容 - 错误: {e}")
            return None
    
    def get_document_info(self, file_id: str) -> Optional[Dict]:
        """
        获取文档详情
        :param file_id: 文档ID
        :return: 文档详情信息，失败时返回None
        """
        # 根据文档，接口地址未明确提供，使用通用路径
        url = f"{self.BASE_API_URL}/file/info"
        timestamp = int(time.time())
        signature = self.auth.get_signature(timestamp)
        
        # 设置请求头，明确指定Content-Type为application/x-www-form-urlencoded
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "appId": self.app_id,
            "timestamp": str(timestamp),
            "signature": signature
        }
        
        # 使用form-data格式发送请求
        data = {"fileId": file_id}
        
        try:
            response = requests.post(url, headers=headers, data=data)
            result = self._handle_response(response, "获取文档详情")
            if result:
                return result.get("data")
            return None
        except Exception as e:
            logger.error(f"获取文档详情 - 错误: {e}")
            return None
    
    def list_documents(self, file_name: Optional[str] = None, ext_name: Optional[str] = None, 
                       file_status: Optional[str] = None, page: int = 1, 
                       page_size: int = 10) -> Optional[Dict]:
        """
        获取文档列表
        :param file_name: 文件名称，模糊查询，可选
        :param ext_name: 文件后缀，可选
        :param file_status: 文件状态，可选
        :param page: 页码，从1开始
        :param page_size: 每页数量
        :return: 文档列表信息，失败时返回None
        """
        url = f"{self.BASE_API_URL}/list"
        headers = self._get_headers()
        
        data = {
            "currentPage": page,
            "pageSize": page_size
        }
        
        if file_name:
            data["fileName"] = file_name
        
        if ext_name:
            data["extName"] = ext_name
        
        if file_status:
            data["fileStatus"] = file_status
        
        try:
            response = requests.post(url, headers=headers, json=data)
            return self._handle_response(response, "获取文档列表")
        except Exception as e:
            logger.error(f"获取文档列表 - 错误: {e}")
            return None
    
    def delete_documents(self, file_ids: List[str]) -> bool:
        """
        删除多个文档
        :param file_ids: 文档ID列表
        :return: 操作是否成功
        """
        # 根据文档，接口地址未明确提供，使用通用路径
        url = f"{self.BASE_API_URL}/delete"
        timestamp = int(time.time())
        signature = self.auth.get_signature(timestamp)
        
        # 设置请求头，明确指定Content-Type为application/x-www-form-urlencoded
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "appId": self.app_id,
            "timestamp": str(timestamp),
            "signature": signature
        }
        
        # 将多个文档ID用英文逗号分割
        file_ids_str = ",".join(file_ids)
        
        # 使用form-data格式发送请求
        data = {"fileIds": file_ids_str}
        
        try:
            response = requests.post(url, headers=headers, data=data)
            result = self._handle_response(response, "删除文档")
            return result is not None
        except Exception as e:
            logger.error(f"删除文档 - 错误: {e}")
            return False
    
    def delete_document(self, doc_id: str) -> bool:
        """
        删除单个文档
        :param doc_id: 文档ID
        :return: 操作是否成功
        """
        return self.delete_documents([doc_id])
    
    def chat(self, query: str, file_ids: Optional[List[str]] = None, repo_id: Optional[str] = None,
             repo_ids: Optional[List[str]] = None, history_messages: Optional[List[Dict[str, str]]] = None,
             on_message: Callable[[Dict], None] = None, on_error: Callable[[str], None] = None,
             on_close: Callable[[], None] = None, temperature: float = 0.5,
             wiki_prompt_tpl: Optional[str] = None, retrieval_filter_policy: str = "REGULAR",
             spark_fallback: bool = False, qa_mode: str = "MIX") -> bool:
        """
        与星火知识库进行对话
        :param query: 用户问题
        :param file_ids: 文件ID列表，最大200个
        :param repo_id: 知识库ID，单个知识库最多包括100个文档
        :param repo_ids: 知识库ID列表，最大100个
        :param history_messages: 历史消息列表，按时间正序
        :param on_message: 接收消息的回调函数
        :param on_error: 错误处理的回调函数
        :param on_close: 连接关闭的回调函数
        :param temperature: 大模型问答时的温度，取值范围(0,1]
        :param wiki_prompt_tpl: 自定义问答模板
        :param retrieval_filter_policy: 检索过滤级别，STRICT-严格，REGULAR-正常，LENIENT-宽松，OFF-关闭
        :param spark_fallback: 未匹配到文档内容时是否使用大模型兜底
        :param qa_mode: 问答模式，QA_FIRST-qa对优先，QA_SUMMARY-qa对总结，MIX-混合模式，WIKI_ONLY-仅文本
        :return: 连接是否成功建立
        """
        # 构建WebSocket URL
        timestamp = int(time.time())
        signature = self.auth.get_signature(timestamp)
        ws_url = f"wss://chatdoc.xfyun.cn/openapi/chat?appId={self.app_id}&timestamp={timestamp}&signature={signature}"
        
        # 准备消息列表
        messages = history_messages or []
        messages.append({"role": "user", "content": query})
        
        # 准备请求数据
        request_data = {
            "messages": messages,
            "chatExtends": {
                "temperature": temperature,
                "retrievalFilterPolicy": retrieval_filter_policy,
                "spark": spark_fallback,
                "qaMode": qa_mode
            }
        }
        
        # 添加自定义问答模板
        if wiki_prompt_tpl:
            request_data["chatExtends"]["wikiPromptTpl"] = wiki_prompt_tpl
        
        # 添加文档或知识库ID
        if file_ids:
            request_data["fileIds"] = file_ids
        elif repo_id:
            request_data["repoId"] = repo_id
        elif repo_ids:
            request_data["repoIds"] = repo_ids
        
        # 创建WebSocket连接
        try:
            ws = websocket.WebSocketApp(
                ws_url,
                on_message=lambda ws, msg: self._on_ws_message(ws, msg, on_message),
                on_error=lambda ws, err: self._on_ws_error(ws, err, on_error),
                on_close=lambda ws, close_status_code, close_msg: self._on_ws_close(ws, on_close)
            )
            
            # 设置连接打开时的回调
            def on_open(ws):
                logger.info("WebSocket连接已建立，发送查询请求...")
                ws.send(json.dumps(request_data))
            
            ws.on_open = on_open
            
            # 在新线程中运行WebSocket连接
            wst = threading.Thread(target=ws.run_forever)
            wst.daemon = True
            wst.start()
            
            return True
        except Exception as e:
            logger.error(f"建立WebSocket连接失败: {e}")
            if on_error:
                on_error(str(e))
            return False
    
    def _on_ws_message(self, ws, message, callback):
        """
        处理WebSocket消息
        :param ws: WebSocket对象
        :param message: 接收到的消息
        :param callback: 用户提供的回调函数
        """
        try:
            data = json.loads(message)
            logger.debug(f"收到WebSocket消息: {data}")
            
            if callback:
                callback(data)
            
            # 检查是否是最后一条消息
            header = data.get("header", {})
            code = header.get("code", 0)
            status = header.get("status", 2)  # 2表示还有后续消息，3表示最后一条消息
            
            if code != 0:
                error_msg = header.get("message", "未知错误")
                logger.error(f"WebSocket错误: {error_msg}")
                ws.close()
            elif status == 3:  # 最后一条消息
                logger.info("对话完成，关闭WebSocket连接")
                ws.close()
        except json.JSONDecodeError:
            logger.error(f"解析WebSocket消息失败: {message}")
        except Exception as e:
            logger.error(f"处理WebSocket消息时发生错误: {e}")
    
    def _on_ws_error(self, ws, error, callback):
        """
        处理WebSocket错误
        :param ws: WebSocket对象
        :param error: 错误信息
        :param callback: 用户提供的回调函数
        """
        logger.error(f"WebSocket错误: {error}")
        if callback:
            callback(str(error))
    
    def _on_ws_close(self, ws, callback):
        """
        处理WebSocket连接关闭
        :param ws: WebSocket对象
        :param callback: 用户提供的回调函数
        """
        logger.info("WebSocket连接已关闭")
        if callback:
            callback()
    
    # ==================== 知识库管理相关方法 ====================
    
    def create_repository(self, repo_name: str, repo_desc: str = "", repo_tags: str = "") -> Optional[str]:
        """
        创建一个新的知识库
        :param repo_name: 知识库名称，唯一
        :param repo_desc: 知识库简介
        :param repo_tags: 知识库标签
        :return: 成功时返回知识库ID，失败时返回None
        """
        url = f"{self.REPO_API_URL}/repo/create"
        headers = self._get_headers()
        
        data = {
            "repoName": repo_name
        }
        
        if repo_desc:
            data["repoDesc"] = repo_desc
        
        if repo_tags:
            data["repoTags"] = repo_tags
        
        try:
            response = requests.post(url, headers=headers, json=data)
            result = self._handle_response(response, "创建知识库")
            if result:
                return result.get("data")
            return None
        except Exception as e:
            logger.error(f"创建知识库 - 错误: {e}")
            return None
    
    def delete_repository(self, repo_id: str) -> bool:
        """
        删除知识库
        :param repo_id: 知识库ID
        :return: 操作是否成功
        """
        url = f"{self.REPO_API_URL}/repo/del"
        timestamp = int(time.time())
        signature = self.auth.get_signature(timestamp)
        
        # 设置请求头，明确指定Content-Type为application/x-www-form-urlencoded
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "appId": self.app_id,
            "timestamp": str(timestamp),
            "signature": signature
        }
        
        # 使用form-data格式发送请求
        data = {"repoId": repo_id}
        
        try:
            response = requests.post(url, headers=headers, data=data)
            result = self._handle_response(response, "删除知识库")
            return result is not None
        except Exception as e:
            logger.error(f"删除知识库 - 错误: {e}")
            return False
    
    def list_repositories(self, repo_name: Optional[str] = None, page: int = 1, page_size: int = 10) -> Optional[Dict]:
        """
        获取知识库列表
        :param repo_name: 知识库名称，模糊查询，可选
        :param page: 页码，从1开始
        :param page_size: 每页数量
        :return: 知识库列表信息，失败时返回None
        """
        url = f"{self.REPO_API_URL}/repo/list"
        headers = self._get_headers()
        
        data = {
            "currentPage": page,
            "pageSize": page_size
        }
        
        if repo_name:
            data["repoName"] = repo_name
        
        try:
            response = requests.post(url, headers=headers, json=data)
            return self._handle_response(response, "获取知识库列表")
        except Exception as e:
            logger.error(f"获取知识库列表 - 错误: {e}")
            return None
    
    def get_repository_info(self, repo_id: str) -> Optional[Dict]:
        """
        获取知识库详情
        :param repo_id: 知识库ID
        :return: 知识库详情，失败时返回None
        """
        url = f"{self.REPO_API_URL}/repo/info"
        timestamp = int(time.time())
        signature = self.auth.get_signature(timestamp)
        
        # 设置请求头，明确指定Content-Type为application/x-www-form-urlencoded
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "appId": self.app_id,
            "timestamp": str(timestamp),
            "signature": signature
        }
        
        # 使用form-data格式发送请求
        data = {"repoId": repo_id}
        
        try:
            response = requests.post(url, headers=headers, data=data)
            return self._handle_response(response, "获取知识库详情")
        except Exception as e:
            logger.error(f"获取知识库详情 - 错误: {e}")
            return None
    
    def list_repository_files(self, repo_id: str, file_name: Optional[str] = None, 
                              ext_name: Optional[str] = None, page: int = 1, 
                              page_size: int = 20) -> Optional[Dict]:
        """
        获取知识库下的文件列表
        :param repo_id: 知识库ID
        :param file_name: 文件名称，模糊查询，可选
        :param ext_name: 文件后缀，可选
        :param page: 页码，从1开始
        :param page_size: 每页数量
        :return: 文件列表信息，失败时返回None
        """
        url = f"{self.REPO_API_URL}/repo/file/list"
        headers = self._get_headers()
        
        data = {
            "repoId": repo_id,
            "currentPage": page,
            "pageSize": page_size
        }
        
        if file_name:
            data["fileName"] = file_name
        
        if ext_name:
            data["extName"] = ext_name
        
        try:
            response = requests.post(url, headers=headers, json=data)
            return self._handle_response(response, "获取知识库文件列表")
        except Exception as e:
            logger.error(f"获取知识库文件列表 - 错误: {e}")
            return None
    
    def add_files_to_repository(self, repo_id: str, file_ids: List[str]) -> Optional[Dict]:
        """
        向知识库中添加文件
        :param repo_id: 知识库ID
        :param file_ids: 文件ID列表，最多20个
        :return: 操作结果，包含失败的文件ID列表，失败时返回None
        """
        if len(file_ids) > 20:
            logger.warning("添加文件到知识库 - 文件数量超过20个，将只处理前20个")
            file_ids = file_ids[:20]
        
        url = f"{self.REPO_API_URL}/repo/file/add"
        headers = self._get_headers()
        
        data = {
            "repoId": repo_id,
            "fileIds": file_ids
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            return self._handle_response(response, "添加文件到知识库")
        except Exception as e:
            logger.error(f"添加文件到知识库 - 错误: {e}")
            return None
    
    def remove_files_from_repository(self, repo_id: str, file_ids: List[str]) -> Optional[Dict]:
        """
        从知识库中移除文件
        :param repo_id: 知识库ID
        :param file_ids: 文件ID列表，最多20个
        :return: 操作结果，包含失败的文件ID列表，失败时返回None
        """
        if len(file_ids) > 20:
            logger.warning("从知识库移除文件 - 文件数量超过20个，将只处理前20个")
            file_ids = file_ids[:20]
        
        url = f"{self.REPO_API_URL}/repo/file/remove"
        headers = self._get_headers()
        
        data = {
            "repoId": repo_id,
            "fileIds": file_ids
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            return self._handle_response(response, "从知识库移除文件")
        except Exception as e:
            logger.error(f"从知识库移除文件 - 错误: {e}")
            return None
    
    # ==================== 文档处理相关方法 ====================
    
    def get_document_status(self, file_ids: List[str]) -> Optional[List[Dict]]:
        """
        查询文档状态
        :param file_ids: 文件ID列表
        :return: 文档状态列表，失败时返回None
        """
        url = f"{self.REPO_API_URL}/file/status"
        timestamp = int(time.time())
        signature = self.auth.get_signature(timestamp)
        
        # 设置请求头，明确指定Content-Type为application/x-www-form-urlencoded
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "appId": self.app_id,
            "timestamp": str(timestamp),
            "signature": signature
        }
        
        # 将文件ID列表转换为逗号分隔的字符串
        file_ids_str = ",".join(file_ids)
        
        # 使用form-data格式发送请求
        data = {"fileIds": file_ids_str}
        
        # 文档状态顺序
        status_map = {
            "uploaded": "已上传",
            "texted": "已文本化",
            "ocring": "OCR识别中",
            "spliting": "切分中",
            "splited": "文本已切分",
            "vectoring": "向量化处理中",
            "vectored": "已向量化",
            "failed": "处理失败"
        }
        
        try:
            response = requests.post(url, headers=headers, data=data)
            result = self._handle_response(response, "查询文档状态")
            if result:
                # 获取data数组，每个元素包含fileId和fileStatus
                status_list = result.get("data", [])
                # 处理每个文档的状态信息
                for status in status_list:
                    file_status = status.get("fileStatus", "")
                    # 根据状态映射表设置状态描述
                    status["status_desc"] = status_map.get(file_status, "未知状态")
                    # 设置是否可以进行问答
                    status["can_chat"] = file_status == "vectored"
                return status_list
            return None
        except Exception as e:
            logger.error(f"查询文档状态 - 错误: {e}")
            return None

    def wait_for_document_ready(self, file_id: str, timeout_seconds: int = 120, check_interval: int = 5) -> bool:
        """
        等待文档处理完成
        :param file_id: 文件ID
        :param timeout_seconds: 超时时间（秒），默认120秒
        :param check_interval: 检查间隔（秒），默认5秒
        :return: 文档是否处理完成
        """
        max_retries = timeout_seconds // check_interval
        status_sequence = ['uploaded', 'texted', 'ocring', 'spliting', 'splited', 'vectoring', 'vectored']
        
        for _ in range(max_retries):
            status_list = self.get_document_status([file_id])
            if not status_list:
                logger.error('获取文档状态失败')
                return False
            
            file_status = status_list[0].get('fileStatus', '')
            logger.info(f'当前文档状态: {file_status}')
            
            if file_status == 'failed':
                logger.error('文档处理失败')
                return False
            elif file_status == 'vectored':
                logger.info('文档处理完成，可以开始问答')
                return True
            elif file_status in status_sequence:
                current_index = status_sequence.index(file_status)
                total_steps = len(status_sequence)
                progress = (current_index + 1) / total_steps * 100
                logger.info(f'文档处理进度: {progress:.1f}% ({file_status})')
            else:
                logger.warning(f'未知的文档状态: {file_status}')
            
            time.sleep(check_interval)
        
        logger.error('文档处理超时，请稍后再试')
        return False
    
    def get_document_info(self, file_id: str) -> Optional[Dict]:
        """
        获取文档详情
        :param file_id: 文件ID
        :return: 文档详情，失败时返回None
        """
        url = f"{self.REPO_API_URL}/file/info"
        timestamp = int(time.time())
        signature = self.auth.get_signature(timestamp)
        
        # 设置请求头，明确指定Content-Type为application/x-www-form-urlencoded
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "appId": self.app_id,
            "timestamp": str(timestamp),
            "signature": signature
        }
        
        # 使用form-data格式发送请求
        data = {"fileId": file_id}
        
        try:
            response = requests.post(url, headers=headers, data=data)
            result = self._handle_response(response, "获取文档详情")
            if result:
                return result.get("data")
            return None
        except Exception as e:
            logger.error(f"获取文档详情 - 错误: {e}")
            return None
    
    def delete_documents(self, file_ids: List[str]) -> bool:
        """
        批量删除文档
        :param file_ids: 文件ID列表
        :return: 操作是否成功
        """
        url = f"{self.REPO_API_URL}/file/del"
        timestamp = int(time.time())
        signature = self.auth.get_signature(timestamp)
        
        # 设置请求头，明确指定Content-Type为application/x-www-form-urlencoded
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "appId": self.app_id,
            "timestamp": str(timestamp),
            "signature": signature
        }
        
        # 将文件ID列表转换为逗号分隔的字符串
        file_ids_str = ",".join(file_ids)
        
        # 使用form-data格式发送请求
        data = {"fileIds": file_ids_str}
        
        try:
            response = requests.post(url, headers=headers, data=data)
            result = self._handle_response(response, "删除文档")
            return result is not None
        except Exception as e:
            logger.error(f"删除文档 - 错误: {e}")
            return False
    
    def start_document_summary(self, file_id: str) -> bool:
        """
        发起文档总结
        :param file_id: 文件ID
        :return: 操作是否成功
        """
        # 根据文档，接口地址未提供，但根据其他接口推测
        url = f"{self.REPO_API_URL}/file/summary/start"
        timestamp = int(time.time())
        signature = self.auth.get_signature(timestamp)
        
        # 设置请求头，明确指定Content-Type为application/x-www-form-urlencoded
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "appId": self.app_id,
            "timestamp": str(timestamp),
            "signature": signature
        }
        
        # 使用form-data格式发送请求
        data = {"fileId": file_id}
        
        try:
            response = requests.post(url, headers=headers, data=data)
            result = self._handle_response(response, "发起文档总结")
            return result is not None
        except Exception as e:
            logger.error(f"发起文档总结 - 错误: {e}")
            return False
    
    def get_document_summary(self, file_id: str) -> Optional[Dict]:
        """
        获取文档总结信息
        :param file_id: 文件ID
        :return: 文档总结信息，失败时返回None
        """
        # 根据文档，接口地址未提供，但根据其他接口推测
        url = f"{self.REPO_API_URL}/file/summary/query"
        timestamp = int(time.time())
        signature = self.auth.get_signature(timestamp)
        
        # 设置请求头，明确指定Content-Type为application/x-www-form-urlencoded
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "appId": self.app_id,
            "timestamp": str(timestamp),
            "signature": signature
        }
        
        # 使用form-data格式发送请求
        data = {"fileId": file_id}
        
        try:
            response = requests.post(url, headers=headers, data=data)
            result = self._handle_response(response, "获取文档总结信息")
            if result:
                return result.get("data")
            return None
        except Exception as e:
            logger.error(f"获取文档总结信息 - 错误: {e}")
            return None
    
    def split_document(self, file_ids: List[str], is_split_default: bool = True, 
                      chunk_separators: List[str] = None, chunk_size: int = 2000, 
                      min_chunk_size: int = 200) -> bool:
        """
        文档切分
        :param file_ids: 文件ID列表
        :param is_split_default: 是否使用默认切分策略
        :param chunk_separators: 分段分隔符，支持多分隔符，base64编码
        :param chunk_size: 分段最大长度，超过强行切分
        :param min_chunk_size: 分段最小长度，小于该值的分段会向下段聚合
        :return: 操作是否成功
        """
        # 根据文档，接口地址未提供，但根据其他接口推测
        url = f"{self.REPO_API_URL}/file/split"
        headers = self._get_headers()
        
        data = {
            "fileIds": file_ids,
            "isSplitDefault": is_split_default,
            "splitType": "wiki"
        }
        
        if not is_split_default:
            wiki_split_extends = {}
            if chunk_separators:
                wiki_split_extends["chunkSeparators"] = chunk_separators
            wiki_split_extends["chunkSize"] = chunk_size
            wiki_split_extends["minChunkSize"] = min_chunk_size
            data["wikiSplitExtends"] = wiki_split_extends
        
        try:
            response = requests.post(url, headers=headers, json=data)
            result = self._handle_response(response, "文档切分")
            return result is not None
        except Exception as e:
            logger.error(f"文档切分 - 错误: {e}")
            return False
    
    def embed_document(self, file_ids: List[str]) -> bool:
        """
        文档向量化
        :param file_ids: 文件ID列表
        :return: 操作是否成功
        """
        # 根据文档，接口地址未提供，但根据其他接口推测
        url = f"{self.REPO_API_URL}/file/embedding"
        timestamp = int(time.time())
        signature = self.auth.get_signature(timestamp)
        
        # 设置请求头，明确指定Content-Type为application/x-www-form-urlencoded
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "appId": self.app_id,
            "timestamp": str(timestamp),
            "signature": signature
        }
        
        # 将文件ID列表转换为逗号分隔的字符串
        file_ids_str = ",".join(file_ids)
        
        # 使用form-data格式发送请求
        data = {"fileIds": file_ids_str}
        
        try:
            response = requests.post(url, headers=headers, data=data)
            result = self._handle_response(response, "文档向量化")
            return result is not None
        except Exception as e:
            logger.error(f"文档向量化 - 错误: {e}")
            return False
    
    def search_vector(self, content: str, file_ids: Optional[List[str]] = None, 
                     top_n: int = 5, wiki_filter_score: float = 0.82) -> Optional[List[Dict]]:
        """
        文档内容相似度检测
        :param content: 用户的问题
        :param file_ids: 文件ID列表，不传则查询应用下所有文件
        :param top_n: 向量库查询数量
        :param wiki_filter_score: WIKI结果分数阈值，低于这个阈值的结果丢弃
        :return: 检索结果列表，失败时返回None
        """
        # 根据文档，接口地址未提供，但根据其他接口推测
        url = f"{self.REPO_API_URL}/vector/search"
        headers = self._get_headers()
        
        data = {
            "content": content,
            "topN": top_n,
            "chatExtends": {
                "wikiFilterScore": wiki_filter_score
            }
        }
        
        if file_ids:
            data["fileIds"] = file_ids
        
        try:
            response = requests.post(url, headers=headers, json=data)
            result = self._handle_response(response, "文档内容相似度检测")
            if result:
                return result.get("data")
            return None
        except Exception as e:
            logger.error(f"文档内容相似度检测 - 错误: {e}")
            return None
    
    def get_document_chunks(self, file_id: str) -> Optional[List[Dict]]:
        """
        获取文档分块内容
        :param file_id: 文件ID
        :return: 文档分块内容列表，失败时返回None
        """
        url = f"{self.REPO_API_URL}/file/chunks"
        headers = self._get_headers()
        
        # 使用form-data格式发送请求
        data = {"fileId": file_id}
        
        try:
            response = requests.post(url, headers=headers, data=data)
            result = self._handle_response(response, "获取文档分块内容")
            if result:
                return result.get("data")
            return None
        except Exception as e:
            logger.error(f"获取文档分块内容 - 错误: {e}")
            return None
    
    # ==================== 问答对管理相关方法 ====================
    
    def extract_qa(self, file_id: str, chunk_size: int = 2000, num_per_chunk: int = 2, 
                  answer_size: int = 100, include_answer: bool = True) -> Optional[str]:
        """
        提交萃取任务
        :param file_id: 文件ID
        :param chunk_size: 分片长度
        :param num_per_chunk: 每个分片问题数
        :param answer_size: 答案长度
        :param include_answer: 是否包含答案
        :return: 成功时返回任务ID，失败时返回None
        """
        url = f"{self.REPO_API_URL}/qa/extract"
        headers = self._get_headers()
        
        data = {
            "fileId": file_id,
            "chunkSize": chunk_size,
            "numPerChunk": num_per_chunk,
            "answerSize": answer_size,
            "includeAnswer": include_answer
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            result = self._handle_response(response, "提交萃取任务")
            if result:
                return result.get("data")
            return None
        except Exception as e:
            logger.error(f"提交萃取任务 - 错误: {e}")
            return None
    
    def get_extract_status(self, file_id: str) -> Optional[str]:
        """
        查询文件萃取状态
        :param file_id: 文件ID
        :return: 文件萃取状态，失败时返回None
        """
        url = f"{self.REPO_API_URL}/qa/extract/status"
        headers = self._get_headers()
        
        # 构建查询参数
        params = {"fileId": file_id}
        
        try:
            response = requests.get(url, headers=headers, params=params)
            result = self._handle_response(response, "查询文件萃取状态")
            if result:
                return result.get("data")
            return None
        except Exception as e:
            logger.error(f"查询文件萃取状态 - 错误: {e}")
            return None
    
    def get_extract_result(self, task_id: Optional[str] = None, file_id: Optional[str] = None) -> Optional[List[Dict]]:
        """
        获取萃取结果
        :param task_id: 任务ID，与file_id必须传一个
        :param file_id: 文件ID，与task_id必须传一个
        :return: 萃取结果列表，失败时返回None
        """
        if not task_id and not file_id:
            logger.error("获取萃取结果 - task_id和file_id不能同时为空")
            return None
        
        url = f"{self.REPO_API_URL}/qa/extract/result"
        headers = self._get_headers()
        
        # 构建查询参数
        params = {}
        if task_id:
            params["taskId"] = task_id
        if file_id:
            params["fileId"] = file_id
        
        try:
            response = requests.get(url, headers=headers, params=params)
            result = self._handle_response(response, "获取萃取结果")
            if result:
                return result.get("data")
            return None
        except Exception as e:
            logger.error(f"获取萃取结果 - 错误: {e}")
            return None
    
    def apply_qa(self, file_id: str, repo_id: str, question: str, answer: str, 
                emb_type: str = "QA") -> Optional[str]:
        """
        QA对应用
        :param file_id: 文件ID
        :param repo_id: 知识库ID
        :param question: 问题
        :param answer: 答案
        :param emb_type: 向量类型，Q-仅仅问题做向量、QA-问题和内容一起做向量
        :return: 成功时返回QA对ID，失败时返回None
        """
        url = f"{self.REPO_API_URL}/qa/apply"
        headers = self._get_headers()
        
        data = {
            "fileId": file_id,
            "repoId": repo_id,
            "question": question,
            "answer": answer,
            "embType": emb_type
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            result = self._handle_response(response, "QA对应用")
            if result:
                return result.get("data")
            return None
        except Exception as e:
            logger.error(f"QA对应用 - 错误: {e}")
            return None
    
    def update_qa(self, qa_id: str, file_id: str, repo_id: str, question: str, 
                 answer: str, emb_type: str = "QA") -> bool:
        """
        QA对更新
        :param qa_id: QA对ID
        :param file_id: 文件ID
        :param repo_id: 知识库ID
        :param question: 问题
        :param answer: 答案
        :param emb_type: 向量类型，Q-仅仅问题做向量、QA-问题和内容一起做向量
        :return: 操作是否成功
        """
        url = f"{self.REPO_API_URL}/qa/apply/update"
        headers = self._get_headers()
        
        data = {
            "id": qa_id,
            "fileId": file_id,
            "repoId": repo_id,
            "question": question,
            "answer": answer,
            "embType": emb_type
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            result = self._handle_response(response, "QA对更新")
            return result is not None
        except Exception as e:
            logger.error(f"QA对更新 - 错误: {e}")
            return False
    
    def delete_qa(self, qa_ids: List[str]) -> bool:
        """
        QA对删除
        :param qa_ids: QA对ID列表
        :return: 操作是否成功
        """
        url = f"{self.REPO_API_URL}/qa/apply/delete"
        headers = self._get_headers()
        
        # 将QA对ID列表转换为逗号分隔的字符串
        qa_ids_str = ",".join(qa_ids)
        
        # 使用form-data格式发送请求
        data = {"ids": qa_ids_str}
        
        try:
            response = requests.post(url, headers=headers, data=data)
            result = self._handle_response(response, "QA对删除")
            return result is not None
        except Exception as e:
            logger.error(f"QA对删除 - 错误: {e}")
            return False
    
    def list_qa(self, file_id: Optional[str] = None, repo_id: Optional[str] = None, 
               page: int = 1, page_size: int = 10) -> Optional[Dict]:
        """
        QA对查询
        :param file_id: 文件ID，与知识库ID必传一个
        :param repo_id: 知识库ID，与文件ID必传一个
        :param page: 当前第几页
        :param page_size: 每页几条
        :return: QA对列表信息，失败时返回None
        """
        if not file_id and not repo_id:
            logger.error("QA对查询 - file_id和repo_id不能同时为空")
            return None
        
        url = f"{self.REPO_API_URL}/qa/apply/page"
        headers = self._get_headers()
        
        data = {
            "currentPage": page,
            "pageSize": page_size
        }
        
        if file_id:
            data["fileId"] = file_id
        
        if repo_id:
            data["repoId"] = repo_id
        
        try:
            response = requests.post(url, headers=headers, json=data)
            return self._handle_response(response, "QA对查询")
        except Exception as e:
            logger.error(f"QA对查询 - 错误: {e}")
            return None
    
    # ==================== 知识库对话相关方法 ====================
    
    def chat_with_repository(self, query: str, repo_id: Optional[str] = None, repo_ids: Optional[List[str]] = None, 
                           file_ids: Optional[List[str]] = None, top_n: int = 5, temperature: float = 0.5,
                           on_message: Callable[[Dict], None] = None, 
                           on_error: Callable[[str], None] = None, 
                           on_close: Callable[[], None] = None) -> bool:
        """
        与知识库进行对话
        :param query: 用户问题
        :param repo_id: 单个知识库ID
        :param repo_ids: 知识库ID列表，最大100
        :param file_ids: 文件ID列表，最大200
        :param top_n: 向量库文本段查询数量
        :param temperature: 大模型问答时的温度，取值范围(0,1]
        :param on_message: 接收消息的回调函数
        :param on_error: 错误处理的回调函数
        :param on_close: 连接关闭的回调函数
        :return: 连接是否成功建立
        """
        # 参数检查
        if not repo_id and not repo_ids and not file_ids:
            logger.error("与知识库对话 - repo_id、repo_ids和file_ids不能同时为空")
            if on_error:
                on_error("repo_id、repo_ids和file_ids不能同时为空")
            return False
        
        # 构建WebSocket URL
        timestamp = int(time.time())
        signature = self.auth.get_signature(timestamp)
        ws_url = f"wss://chatdoc.xfyun.cn/openapi/chat?appId={self.app_id}&timestamp={timestamp}&signature={signature}"
        
        # 准备请求数据
        request_data = {
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ],
            "chatExtends": {
                "temperature": temperature
            }
        }
        
        # 添加知识库或文件ID
        if repo_id:
            request_data["repoId"] = repo_id
        elif repo_ids:
            request_data["repoIds"] = repo_ids[:100]  # 限制最大100个
        elif file_ids:
            request_data["fileIds"] = file_ids[:200]  # 限制最大200个
        
        if top_n:
            request_data["topN"] = top_n
        
        # 创建WebSocket连接
        try:
            ws = websocket.WebSocketApp(
                ws_url,
                on_message=lambda ws, msg: self._on_ws_message(ws, msg, on_message),
                on_error=lambda ws, err: self._on_ws_error(ws, err, on_error),
                on_close=lambda ws, close_status_code, close_msg: self._on_ws_close(ws, on_close)
            )
            
            # 设置连接打开时的回调
            def on_open(ws):
                logger.info("WebSocket连接已建立，发送查询请求...")
                ws.send(json.dumps(request_data))
            
            ws.on_open = on_open
            
            # 在新线程中运行WebSocket连接
            wst = threading.Thread(target=ws.run_forever)
            wst.daemon = True
            wst.start()
            
            return True
        except Exception as e:
            logger.error(f"建立WebSocket连接失败: {e}")
            if on_error:
                on_error(str(e))
            return False


    def get_document_status(self, file_ids: List[str]) -> Optional[List[Dict]]:
        """
        获取文档处理状态
        :param file_ids: 文档ID列表
        :return: 文档状态列表，失败时返回None
        """
        url = f"{self.BASE_API_URL}/file/status"
        timestamp = int(time.time())
        signature = self.auth.get_signature(timestamp)
        
        # 设置请求头
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "appId": self.app_id,
            "timestamp": str(timestamp),
            "signature": signature
        }
        
        # 将多个文档ID用英文逗号分割
        file_ids_str = ",".join(file_ids)
        
        # 使用form-data格式发送请求
        data = {"fileIds": file_ids_str}
        
        try:
            response = requests.post(url, headers=headers, data=data)
            result = self._handle_response(response, "查询文档状态")
            if result:
                return result.get("data", [])
            return None
        except Exception as e:
            logger.error(f"查询文档状态 - 错误: {e}")
            return None

if __name__ == '__main__':
    # 初始化配置
    conf = Config()
    
    # 初始化知识库实例
    kb = KnowledgeBase(conf)
    
    # 测试文档上传
    logger.info('----------测试文档上传----------')
    doc_id = kb.upload_document(os.path.join(os.path.dirname(__file__), 'test.txt'), '测试文档.txt')
    if doc_id:
        logger.info(f'文档上传成功，ID: {doc_id}')
    
        # 测试创建知识库
        logger.info('----------测试创建知识库----------')
        repo_name = f'测试知识库_{int(time.time())}'
        repo_id = kb.create_repository(repo_name, '这是一个测试用的知识库', '测试,知识库')
        if repo_id:
            logger.info(f'知识库创建成功，ID: {repo_id}')
            
            # 将文档添加到知识库
            result = kb.add_files_to_repository(repo_id, [doc_id])
            if result:
                logger.info('文档成功添加到知识库')
                
                # 检查文档处理状态
                logger.info('----------等待文档处理完成----------')
                max_retries = 24  # 最多等待120秒
                doc_ready = False
                status_sequence = ['uploaded', 'texted', 'ocring', 'spliting', 'splited', 'vectoring', 'vectored']
                
                for _ in range(max_retries):
                    status = kb.get_document_status([doc_id])
                    if not status:
                        logger.error('获取文档状态失败')
                        break
                        
                    current_status = status[0].get('fileStatus', '')
                    logger.info(f'当前文档状态: {current_status}')
                    
                    if current_status == 'failed':
                        logger.error('文档处理失败')
                        break
                    elif current_status == 'vectored':
                        doc_ready = True
                        logger.info('文档处理完成，可以开始问答')
                        break
                    elif current_status in status_sequence:
                        logger.info(f'文档正在处理中: {current_status}')
                    else:
                        logger.warning(f'未知的文档状态: {current_status}')
                    
                    time.sleep(5)
                
                if doc_ready:
                    # 测试对话功能
                    logger.info('----------测试对话功能----------')
                    
                    def on_message(data):
                        # 处理接收到的消息
                        content = data.get('content', '')
                        if content:
                            logger.info(f'收到回复: {content}')
                        
                        # 检查是否有文档引用
                        file_refer = data.get('fileRefer')
                        if file_refer:
                            logger.info(f'文档引用: {file_refer}')
                    
                    def on_error(error):
                        logger.error(f'发生错误: {error}')
                    
                    def on_close():
                        logger.info('对话结束')
                    
                    # 发起对话
                    kb.chat(
                        query='这个文档的主要内容是什么？',
                        file_ids=[doc_id],  # 使用文件ID列表
                        history_messages=[],  # 空的历史消息列表
                        on_message=on_message,
                        on_error=on_error,
                        on_close=on_close,
                        temperature=0.7,  # 设置较高的温度以获得更多样的回答
                        retrieval_filter_policy='LENIENT',  # 使用宽松的过滤策略
                        spark_fallback=True,  # 启用大模型兜底
                        qa_mode='MIX'  # 使用混合问答模式
                    )
                    # 等待一段时间以接收响应
                    time.sleep(10)
                else:
                    logger.error('文档处理超时，请稍后再试')
            else:
                logger.error('添加文档到知识库失败')
        else:
            logger.error('创建知识库失败')
    else:
        logger.error('文档上传失败')