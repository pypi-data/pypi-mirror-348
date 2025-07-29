#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : ppt_generator.py
# @Author: anarchy
# @Date  : 2025/5/12
# @Desc  : 讯飞智能PPT在线生成服务SDK封装

import hashlib
import hmac
import base64
import json
import time
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from typing import Optional, Dict, Any, Union # 类型提示

from dwspark.config import Config # 导入配置类
from loguru import logger # 导入日志库


class HttpAuthParams:
    """处理智能PPT HTTP API认证参数和头部生成的辅助类"""
    def __init__(self, app_id: str, api_secret: str):
        """
        初始化认证参数处理器。
        :param app_id: 智能PPT服务的APPID。
        :param api_secret: 智能PPT服务的APISecret。
        """
        if not app_id or not api_secret:
            raise ValueError("APPID 和 APISecret 不能为空。")
        self.app_id = app_id
        self.api_secret = api_secret

    def _md5(self, text: str) -> str:
        """计算文本的MD5哈希值。"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    def _hmac_sha1_encrypt(self, encrypt_text: str, encrypt_key: str) -> str:
        """使用HMAC-SHA1算法加密文本，并返回Base64编码的摘要。"""
        return base64.b64encode(
            hmac.new(encrypt_key.encode('utf-8'), encrypt_text.encode('utf-8'), hashlib.sha1).digest()
        ).decode('utf-8')

    def _get_signature(self, ts: int) -> str:
        """生成API请求所需的签名。"""
        auth = self._md5(self.app_id + str(ts))
        return self._hmac_sha1_encrypt(auth, self.api_secret)

    def generate_headers(self, content_type: str = "application/json; charset=utf-8") -> Dict[str, str]:
        """生成通用的API请求头部。"""
        timestamp = int(time.time())
        signature = self._get_signature(timestamp)
        return {
            "appId": self.app_id,
            "timestamp": str(timestamp),
            "signature": signature,
            "Content-Type": content_type
        }


class PPTGenerator():
    """封装智能PPT生成相关API的类"""
    BASE_URL = "https://zwapi.xfyun.cn/api/ppt/v2"  # API基础地址
    CREATE_TASK_URL = f"{BASE_URL}/create"  # 创建PPT任务（直接基于文本或文档）
    PROGRESS_URL = f"{BASE_URL}/progress"  # 查询任务进度
    TEMPLATE_LIST_URL = f"{BASE_URL}/template/list"  # 获取PPT模板列表
    CREATE_OUTLINE_URL = f"{BASE_URL}/createOutline"  # 根据文本创建大纲
    CREATE_OUTLINE_BY_DOC_URL = f"{BASE_URL}/createOutlineByDoc"  # 根据文档创建大纲
    CREATE_PPT_BY_OUTLINE_URL = f"{BASE_URL}/createPptByOutline"  # 根据大纲创建PPT


    def __init__(self, config: Config):
        """
        初始化PPT生成器实例。

        :param config: Config对象，包含必要的API凭证 (XF_APPID, XF_APISECRET)。
        :raises ValueError: 如果Config对象中缺少必要的APPID或APISecret。
        """
        app_id_to_use = getattr(config, 'XF_APPID', None)
        api_secret_to_use = getattr(config, 'XF_APISECRET', None)

        if not app_id_to_use or not api_secret_to_use:
            raise ValueError(
                "Config对象必须提供 XF_APPID 和 XF_APISECRET 以供PPT生成器使用。"
            )
        
        # 初始化 HttpAuthParams 实例
        self.auth_handler = HttpAuthParams(app_id=app_id_to_use, api_secret=api_secret_to_use)

    def _handle_response(self, response: requests.Response, context: str = "API请求") -> Optional[Dict[str, Any]]:
        """统一处理API响应，包括错误检查和日志记录。"""
        logger.debug(f"{context} - 响应状态码: {response.status_code}, 响应体: {response.text}")
        try:
            resp_json = response.json()
        except json.JSONDecodeError:
            logger.error(f"{context} - 解析JSON响应失败: {response.text}")
            return None

        if response.status_code == 200 and resp_json.get('code') == 0:
            return resp_json.get('data') # 成功时返回 data 字段
        else:
            error_code = resp_json.get('code', 'N/A')
            error_message = resp_json.get('message') or resp_json.get('desc', '未知错误')
            sid = resp_json.get('sid', 'N/A')
            logger.error(f"{context} - 错误: code={error_code}, message='{error_message}', sid='{sid}', 完整响应='{response.text}'")
            return None

    def get_theme_list(self, pay_type: str = "not_free", style: Optional[str] = None,
                         color: Optional[str] = None, industry: Optional[str] = None,
                         page_num: int = 1, page_size: int = 10) -> Optional[Dict[str, Any]]:
        """
        获取PPT主题模板列表。

        :param pay_type: 付费类型 (例如: "free", "not_free", "vip"), 默认 "not_free"。
        :param style: PPT风格 (例如: "简约", "商务"), 可选。
        :param color: PPT颜色 (例如: "红色", "蓝色"), 可选。
        :param industry: 行业分类 (例如: "教育培训"), 可选。
        :param page_num: 页码，从1开始，默认1。
        :param page_size: 每页数量，默认10。
        :return: 包含主题列表的字典，或在失败时返回None。
        """
        params = {
            "payType": pay_type,
            "pageNum": page_num,
            "pageSize": page_size
        }
        if style:
            params["style"] = style
        if color:
            params["color"] = color
        if industry:
            params["industry"] = industry
        
        headers = self.auth_handler.generate_headers() # 使用 auth_handler 生成头部
        try:
            response = requests.get(self.TEMPLATE_LIST_URL, headers=headers, params=params)
            logger.info(f"获取PPT主题列表 - 完整原始响应: {response.text}")
            return self._handle_response(response, "获取PPT主题列表")
        except requests.RequestException as e:
            logger.error(f"获取PPT主题列表 - 请求失败: {e}")
            return None

    def create_outline_from_text(self, query_text: str, language: str = "cn", search: bool = False) -> Optional[Dict[str, Any]]:
        """
        根据输入文本创建PPT大纲。

        :param query_text: 用于生成大纲的文本描述。
        :param language: 语言, 默认 "cn" (中文)。
        :param search: 是否联网搜索以增强内容, 默认 False。
        :return: 包含生成大纲信息的字典 (含sid和outline)，或在失败时返回None。
        """
        fields = {
            "query": query_text,
            "language": language,
            "search": str(search).lower(), # API期望小写的 "true"/"false"
        }
        encoder = MultipartEncoder(fields=fields)
        headers = self.auth_handler.generate_headers(content_type=encoder.content_type) # 使用 auth_handler
        
        try:
            # 使用 data=encoder 发送 multipart/form-data 请求
            response = requests.post(self.CREATE_OUTLINE_URL, data=encoder, headers=headers)
            return self._handle_response(response, "根据文本创建大纲")
        except requests.RequestException as e:
            logger.error(f"根据文本创建大纲 - 请求失败: {e}")
            return None

    def create_outline_from_doc(self, query_text: str, file_name: str, file_path: Optional[str] = None,
                                  file_url: Optional[str] = None, language: str = "cn", search: bool = False) -> Optional[Dict[str, Any]]:
        """
        根据上传的文档创建PPT大纲。

        :param query_text: 对文档内容的简要描述或期望生成大纲的主题。
        :param file_name: 上传的文件名 (包含后缀)。
        :param file_path: 本地文件路径, 与 file_url 任选其一。
        :param file_url: 文件的URL地址, 与 file_path 任选其一。
        :param language: 语言, 默认 "cn"。
        :param search: 是否联网搜索, 默认 False。
        :return: 包含生成大纲信息的字典，或在失败时返回None。
        """
        if not file_path and not file_url:
            logger.error("创建文档大纲时，必须提供 file_path 或 file_url。")
            return None

        fields = {
            "fileName": file_name,
            "query": query_text,
            "language": language,
            "search": str(search).lower(), # API期望小写的 "true"/"false"
        }
        opened_file = None # 用于确保文件被关闭
        if file_path:
            try:
                opened_file = open(file_path, 'rb')
                fields["file"] = (file_name, opened_file, 'application/octet-stream') # 可以更具体，如 application/pdf
            except IOError as e:
                logger.error(f"打开文件 {file_path} 失败: {e}")
                if opened_file: opened_file.close() # 确保关闭
                return None
        elif file_url:
             fields["fileUrl"] = file_url

        encoder = MultipartEncoder(fields=fields)
        headers = self.auth_handler.generate_headers(content_type=encoder.content_type) # 使用 auth_handler
        
        try:
            response = requests.post(self.CREATE_OUTLINE_BY_DOC_URL, data=encoder, headers=headers)
            return self._handle_response(response, "根据文档创建大纲")
        except requests.RequestException as e:
            logger.error(f"根据文档创建大纲 - 请求失败: {e}")
            return None
        finally:
            if opened_file: # 确保在所有情况下都关闭文件
                opened_file.close()

    def create_ppt_from_text(self, query_text: str, template_id: str, author: str = "AI助手",
                               is_card_note: bool = True, search: bool = False, is_figure: bool = True,
                               ai_image_type: str = "normal") -> Optional[str]:
        """
        直接根据输入文本创建PPT。

        :param query_text: 用于生成PPT的文本描述。
        :param template_id: PPT模板ID，从 get_theme_list 获取。
        :param author: PPT作者名, 默认 "AI助手"。
        :param is_card_note: 是否生成PPT演讲者备注, 默认 True。
        :param search: 是否联网搜索, 默认 False。
        :param is_figure: 是否自动配图, 默认 True。
        :param ai_image_type: AI配图类型 ("normal", "advanced"), 默认 "normal"。normal: 20%正文配图; advanced: 50%正文配图。
        :return: 任务的SID (字符串)，或在失败时返回None。
        """
        fields = {
            "query": query_text,
            "templateId": template_id,
            "author": author,
            "isCardNote": str(is_card_note).lower(),
            "search": str(search).lower(),
            "isFigure": str(is_figure).lower(),
            "aiImage": ai_image_type
        }
        # 注意：根据原始xfPPT_demo.py，create_task (对应此方法) 使用MultipartEncoder
        encoder = MultipartEncoder(fields=fields)
        headers = self.auth_handler.generate_headers(content_type=encoder.content_type) # 使用 auth_handler

        try:
            response = requests.post(self.CREATE_TASK_URL, data=encoder, headers=headers)
            data = self._handle_response(response, "直接根据文本创建PPT")
            return data.get("sid") if data else None
        except requests.RequestException as e:
            logger.error(f"直接根据文本创建PPT - 请求失败: {e}")
            return None

    def create_ppt_from_outline(self, query_text: str, outline: Union[str, Dict], template_id: str,
                                  author: str = "AI助手", is_card_note: bool = True, search: bool = False,
                                  is_figure: bool = True, ai_image_type: str = "normal") -> Optional[str]:
        """
        根据提供的大纲创建PPT。

        :param query_text: 生成PPT的主题或原始查询文本。
        :param outline: 大纲内容，可以是JSON字符串或Python字典。
        :param template_id: PPT模板ID。
        :param author: 作者名, 默认 "AI助手"。
        :param is_card_note: 是否生成备注, 默认 True。
        :param search: 是否联网搜索, 默认 False。
        :param is_figure: 是否自动配图, 默认 True。
        :param ai_image_type: AI配图类型, 默认 "normal"。
        :return: 任务的SID (字符串)，或在失败时返回None。
        """

        payload = {
            "query": query_text,
            "outline": outline, # API可能接受字典或已序列化的JSON字符串
            "templateId": template_id,
            "author": author,
            "isCardNote": str(is_card_note).lower(), # 假设此接口也偏好小写字符串布尔值
            "search": str(search).lower(),
            "isFigure": str(is_figure).lower(),
            "aiImage": ai_image_type,
        }
        headers = self.auth_handler.generate_headers() # 使用 auth_handler

        try:
            response = requests.post(self.CREATE_PPT_BY_OUTLINE_URL, json=payload, headers=headers)
            data = self._handle_response(response, "根据大纲创建PPT")
            return data.get("sid") if data else None
        except requests.RequestException as e:
            logger.error(f"根据大纲创建PPT - 请求失败: {e}")
            return None

    def get_task_progress(self, sid: str) -> Optional[Dict[str, Any]]:
        """
        查询指定SID的任务的当前进度。

        :param sid: 任务SID。
        :return: 包含任务状态信息的字典，或在失败时返回None。
        """
        if not sid:
            logger.error("必须提供任务SID才能查询进度。")
            return None
        
        current_headers = self.auth_handler.generate_headers() # 使用 auth_handler

        try:
            response = requests.get(f"{self.PROGRESS_URL}?sid={sid}", headers=current_headers)
            # 进度查询的响应结构可能与 _handle_response 的通用处理略有不同，但通常code=0表示成功
            logger.debug(f"查询任务进度 ({sid}) - 响应状态码: {response.status_code}, 响应体: {response.text}")
            resp_json = response.json()
            if response.status_code == 200 and resp_json.get('code') == 0 :
                return resp_json.get('data') # data字段包含状态信息
            else:
                error_code = resp_json.get('code', 'N/A')
                error_message = resp_json.get('message') or resp_json.get('desc', '未知错误')
                logger.error(f"查询任务进度 ({sid}) - 错误: code={error_code}, message='{error_message}', 完整响应='{response.text}'")
                return None

        except requests.RequestException as e:
            logger.error(f"查询任务进度 ({sid}) - 请求失败: {e}")
            return None
        except json.JSONDecodeError:
            logger.error(f"查询任务进度 ({sid}) - 解析JSON响应失败: {response.text}")
            return None

    def poll_for_result(self, sid: str, poll_interval: int = 10, max_attempts: int = 30) -> Optional[str]:
        """
        轮询任务直到完成或超时，返回最终的PPT链接。

        :param sid: 任务SID。
        :param poll_interval: 轮询间隔秒数, 默认10秒。
        :param max_attempts: 最大轮询次数, 默认30次。
        :return: 成功生成PPT的URL，或在失败/超时时返回None。
        """
        if not sid:
            logger.error("必须提供任务SID才能轮询结果。")
            return None

        logger.info(f"开始轮询PPT任务结果，SID: {sid} (间隔: {poll_interval}s, 最大尝试: {max_attempts}次)")
        last_progress_data = None # 用于在超时时记录最后的状态
        for attempt in range(max_attempts):
            progress_data = self.get_task_progress(sid)
            last_progress_data = progress_data # 更新最后的状态
            if progress_data:
                ppt_status = progress_data.get('pptStatus')
                ai_image_status = progress_data.get('aiImageStatus')
                card_note_status = progress_data.get('cardNoteStatus')
                
                logger.info(f"轮询尝试 {attempt + 1}/{max_attempts}: PPT状态={ppt_status}, AI配图={ai_image_status}, 备注={card_note_status}")

                # 检查所有相关状态是否都已完成 ("done")
                # 注意: 并非所有任务都会有 aiImageStatus 或 cardNoteStatus，取决于创建时的选项
                all_done = ppt_status == 'done'
                # 仅当API返回了这些状态字段时才检查它们是否为 'done'
                if 'aiImageStatus' in progress_data:
                    all_done = all_done and (ai_image_status == 'done')
                if 'cardNoteStatus' in progress_data:
                    all_done = all_done and (card_note_status == 'done')

                if all_done:
                    ppt_url = progress_data.get('pptUrl')
                    if ppt_url:
                        logger.info(f"PPT生成成功！URL: {ppt_url}")
                        return ppt_url
                    else:
                        logger.error(f"所有状态均为 'done' 但缺少 pptUrl。SID: {sid}, 数据: {progress_data}")
                        return None # 状态完成但无URL，异常情况
                
                # 检查是否有明确的失败状态
                # API可能使用如 'failed', 'error' 等字符串表示失败
                failed_statuses = ['failed', 'error', 'fail'] # 可能的失败状态字符串
                if any(s in failed_statuses for s in [ppt_status, ai_image_status, card_note_status] if s):
                    logger.error(f"任务失败。SID: {sid}, 状态: ppt={ppt_status}, 配图={ai_image_status}, 备注={card_note_status}")
                    return None

            else: # get_task_progress 返回 None (查询进度时出错)
                logger.warning(f"获取任务 {sid} 的进度失败 (尝试 {attempt + 1})。将重试...")

            time.sleep(poll_interval)
        
        logger.error(f"轮询超时 {max_attempts * poll_interval} 秒后，任务 {sid} 仍未完成。最后状态: {last_progress_data}")
        return None

# 主模块测试代码
if __name__ == '__main__':
    # 配置日志输出：控制台和文件
    logger.remove() # 移除默认的stderr日志处理器
    logger.add(lambda msg: print(msg, end=''), format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", level="INFO") # 控制台输出
    logger.add("ppt_generator.log", rotation="10 MB", retention="3 days", level="DEBUG") # 日志文件输出

    try:
        logger.info("--- 初始化智能PPT生成器测试 ---")
        import os
        # 从环境变量加载星火大模型凭证 (推荐)
        spark_appid = os.environ.get("SPARKAI_APP_ID")
        spark_apikey = os.environ.get("SPARKAI_API_KEY")
        spark_apisecret = os.environ.get("SPARKAI_API_SECRET")

        if not all([spark_appid, spark_apikey, spark_apisecret]):
            logger.warning("一个或多个星火大模型环境变量 (SPARKAI_APP_ID, SPARKAI_API_KEY, SPARKAI_API_SECRET) 未设置.")
            logger.warning("将使用代码中硬编码的占位符凭证进行测试 (API调用很可能会失败).")
            
            if spark_appid == "06ebab34":
                 print("\n**************************************************************************************")
                 print("警告: PPT生成器正在使用占位符星火凭证。API 调用将失败。")
                 print("请设置 SPARKAI_APP_ID, SPARKAI_API_KEY, SPARKAI_API_SECRET 环境变量或在代码中提供有效值。")
                 print("**************************************************************************************\n")

        test_config = Config(
            appid=spark_appid,
            apikey=spark_apikey, 
            apisecret=spark_apisecret
        )
        
        ppt_gen = PPTGenerator(config=test_config)
        logger.info("PPTGenerator 初始化成功.")

        # --- 流程1: 获取主题列表 ---
        logger.info("\n--- 演示: 获取PPT主题列表 ---")
        themes_data = ppt_gen.get_theme_list()
        selected_template_id = "20240718489569D" # 默认/备用模板ID
        if themes_data and themes_data.get('list'):
            logger.info(f"成功获取到 {len(themes_data['list'])} 个主题 (根据 _handle_response 解析结果).")
            for i, theme in enumerate(themes_data['list']):
                logger.info(f"  主题 {i+1}: ID={theme.get('templateId')}, 名称='{theme.get('name')}', 风格='{theme.get('style')}', 颜色='{theme.get('color')}'")
            if themes_data['list']:
                 selected_template_id = themes_data['list'][0].get('templateId', selected_template_id)
        logger.info(f"测试将使用模板ID: {selected_template_id} (原始响应已在 get_theme_list 方法中记录)")

        # --- 流程2: 根据文本生成大纲 ---
        logger.info("\n--- 演示: 根据文本生成PPT大纲 ---")
        outline_query = "介绍一下人工智能在教育领域的应用"
        logger.info(f"大纲主题: \"{outline_query}\"")
        outline_result = ppt_gen.create_outline_from_text(query_text=outline_query)
        generated_outline_content = None
        if outline_result and outline_result.get("outline"):
            generated_outline_content = outline_result["outline"]
            logger.info(f"成功生成大纲: \n{json.dumps(generated_outline_content, ensure_ascii=False, indent=2)}")
        else:
            logger.warning("根据文本生成大纲失败.")

        # --- 流程3: 根据生成的大纲创建PPT ---
        if generated_outline_content:
            logger.info("\n--- 演示: 根据上方生成的大纲创建PPT ---")
            sid_from_outline = ppt_gen.create_ppt_from_outline(
                query_text=outline_query, 
                outline=generated_outline_content,
                template_id=selected_template_id,
                author="SDK测试脚本 (大纲生成)"
            )
            if sid_from_outline:
                logger.info(f"基于大纲的PPT创建任务已启动，SID: {sid_from_outline}")
                ppt_url_from_outline = ppt_gen.poll_for_result(sid_from_outline)
                if ppt_url_from_outline:
                    logger.info(f"基于大纲的PPT已生成！下载链接: {ppt_url_from_outline}")
                else:
                    logger.warning("基于大纲的PPT生成失败或超时.")
            else:
                logger.warning("启动基于大纲的PPT创建任务失败.")
        else:
            logger.info("\n跳过 [根据大纲创建PPT] 的演示，因为前一步大纲生成失败.")

        # --- 流程4: 直接根据文本创建PPT ---
        logger.info("\n--- 演示: 直接根据文本创建PPT ---")
        direct_ppt_query = "请帮我制作一份关于可再生能源的科普PPT，包含太阳能、风能和水能"
        logger.info(f"PPT主题: \"{direct_ppt_query}\"")
        sid_direct = ppt_gen.create_ppt_from_text(
            query_text=direct_ppt_query,
            template_id=selected_template_id,
            author="SDK测试脚本 (直接生成)",
            is_card_note=True,
            ai_image_type="normal" # 使用 "normal" 或 "advanced"
        )
        if sid_direct:
            logger.info(f"直接文本PPT创建任务已启动，SID: {sid_direct}")
            ppt_url_direct = ppt_gen.poll_for_result(sid_direct)
            if ppt_url_direct:
                logger.info(f"直接文本PPT已生成！下载链接: {ppt_url_direct}")
            else:
                logger.warning("直接文本PPT生成失败或超时.")
        else:
            logger.warning("启动直接文本PPT创建任务失败.")

        # --- 流程5: 根据文档生成大纲 (需要准备测试文件) ---
        logger.info("\n--- (可选演示): 根据文档生成PPT大纲 ---")
        test_doc_path = "./example_document.txt" # 替换为您的测试文档路径
        test_doc_query = "总结文档要点"
        if os.path.exists(test_doc_path):
            logger.info(f"将使用文档 '{test_doc_path}' 和主题 '{test_doc_query}' 生成大纲")
            doc_outline_result = ppt_gen.create_outline_from_doc(
                query_text=test_doc_query, 
                file_name=os.path.basename(test_doc_path),
                file_path=test_doc_path
            )
            if doc_outline_result and doc_outline_result.get("outline"):
                logger.info(f"成功根据文档生成大纲: \n{json.dumps(doc_outline_result['outline'], ensure_ascii=False, indent=2)}")
            else:
                logger.warning(f"根据文档 '{test_doc_path}' 生成大纲失败.")
        else:
            logger.info(f"跳过 [根据文档生成大纲] 的演示，测试文件 '{test_doc_path}' 不存在或路径不正确.")

        logger.info("\n--- 智能PPT生成器所有演示流程结束 ---")

    except ValueError as ve:
        logger.error(f"配置或参数错误: {ve}")
    except requests.exceptions.RequestException as re:
        logger.error(f"网络请求错误: {re}")
    except Exception as e:
        logger.error(f"测试过程中发生意外错误: {e}", exc_info=True) 