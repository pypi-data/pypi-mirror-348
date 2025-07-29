#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : character_simulator.py
# @Author: hcy
# @Date  : 2025/5/15
# @Desc  : 讯飞角色模拟服务SDK封装

import base64
import hashlib
import hmac
import json
import time
import threading
import websocket
from typing import Optional, Dict, Any, List, Callable
from urllib.parse import urlencode

import requests
from dwspark.config import Config
from loguru import logger


class ApiAuthAlgorithm:
    """处理讯飞角色模拟服务API认证的辅助类。"""
    
    def __init__(self, app_id: str, secret: str):
        """
        初始化角色模拟服务认证处理器。
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
        :param ts: 时间戳，单位毫秒
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


class CharacterSimulator:
    """封装讯飞角色模拟API的类。"""
    # 服务的基础URL
    BASE_API_URL = "https://ai-character-v2.xfyun.cn/personality/open"
    
    def __init__(self, config: Config):
        """
        初始化角色模拟器实例。
        :param config: Config对象，包含API凭证 (XF_APPID, XF_APIKEY, XF_APISECRET)。
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
        timestamp = int(time.time() * 1000)  # 当前时间戳，毫秒级
        signature = self.auth.get_signature(timestamp)
        
        return {
            "Content-Type": "application/json",
            "appId": self.app_id,
            "timestamp": str(timestamp),
            "signature": signature
        }
    
    def _handle_response(self, response: requests.Response, context: str = "角色模拟API请求") -> Optional[Dict]:
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
        
        if response.status_code == 200 and resp_json.get("success", False):
            logger.info(f"{context} - 请求成功")
            return resp_json
        else:
            code = resp_json.get("code", "未知")
            message = resp_json.get("message", "未知错误")
            description = resp_json.get("description", "")
            sid = resp_json.get("sid", "N/A")
            logger.error(f"{context} - 错误: code={code}, message='{message}', description='{description}', sid='{sid}'")
            return None
    
    def create_player(self, player_name: str, player_identity: str = "") -> Optional[str]:
        """
        创建玩家账号
        :param player_name: 玩家名称（同一应用下不允许重复），50字符以内
        :param player_identity: 玩家职业身份（300字符以内，描述玩家的职业身份、和人格的关系、使命职责等）
        :return: 成功时返回玩家ID，失败时返回None
        """
        url = f"{self.BASE_API_URL}/player/register"
        headers = self._get_headers()
        
        data = {
            "playerName": player_name
        }
        
        if player_identity:
            data["playerIdentity"] = player_identity
        
        try:
            response = requests.post(url, json=data, headers=headers)
            result = self._handle_response(response, "创建玩家账号")
            if result:
                return result.get("data")
            return None
        except requests.RequestException as e:
            logger.error(f"创建玩家账号 - 网络错误: {e}")
            return None
    
    def modify_player(self, player_id: str, player_name: str = None, player_identity: str = None) -> bool:
        """
        编辑玩家账号
        :param player_id: 玩家ID
        :param player_name: 玩家姓名（同一应用下不允许重复）
        :param player_identity: 玩家身份标识，300字符以内
        :return: 操作是否成功
        """
        url = f"{self.BASE_API_URL}/player/modify"
        headers = self._get_headers()
        
        data = {
            "playerId": player_id
        }
        
        if player_name is not None:
            data["playerName"] = player_name
        
        if player_identity is not None:
            data["playerIdentity"] = player_identity
        
        try:
            response = requests.post(url, json=data, headers=headers)
            result = self._handle_response(response, "编辑玩家账号")
            return result is not None
        except requests.RequestException as e:
            logger.error(f"编辑玩家账号 - 网络错误: {e}")
            return False
    
    def delete_player(self, player_id: str) -> bool:
        """
        删除玩家账号
        :param player_id: 玩家账号ID
        :return: 操作是否成功
        """
        url = f"{self.BASE_API_URL}/player/delete/{player_id}"
        headers = self._get_headers()
        
        try:
            response = requests.post(url, headers=headers)
            result = self._handle_response(response, "删除玩家账号")
            if result and result.get("data", False):
                return True
            return False
        except requests.RequestException as e:
            logger.error(f"删除玩家账号 - 网络错误: {e}")
            return False
    
    def create_agent(self, player_id: str, agent_name: str, agent_hobby: str = None, 
                     agent_identity: str = None, agent_personality_desc: str = None) -> Optional[str]:
        """
        创建人格
        :param player_id: 玩家ID
        :param agent_name: 人格名称（50字符以内）
        :param agent_hobby: 爱好（使用人格名称指代，100字符以内）
        :param agent_identity: 社会身份（职业身份、和他人的关系、使命职责等。使用人格名称指代，100字符以内）
        :param agent_personality_desc: 性格描述（身世背景，影响性格的重要事件，体现性格的典型表现等。使用人格名称指代。2000字符以内）
        :return: 成功时返回人格ID，失败时返回None
        """
        url = f"{self.BASE_API_URL}/agent/save"
        headers = self._get_headers()
        
        data = {
            "playerId": player_id,
            "agentName": agent_name
        }
        
        # 添加可选参数
        if agent_hobby is not None:
            data["agentHobby"] = agent_hobby
        if agent_identity is not None:
            data["agentIdentity"] = agent_identity
        if agent_personality_desc is not None:
            data["agentPersonalityDesc"] = agent_personality_desc
        
        try:
            response = requests.post(url, json=data, headers=headers)
            result = self._handle_response(response, "创建人格")
            if result:
                return result.get("data")
            return None
        except requests.RequestException as e:
            logger.error(f"创建人格 - 网络错误: {e}")
            return None
            
    def edit_agent(self, agent_id: str, agent_name: str = None, agent_hobby: str = None,
                   agent_identity: str = None, agent_personality_desc: str = None) -> bool:
        """
        编辑人格的属性
        :param agent_id: 人格ID
        :param agent_name: 人格名称（50字符以内）
        :param agent_hobby: 爱好（使用人格名称指代，100字符以内）
        :param agent_identity: 社会身份（职业身份、和他人的关系、使命职责等。使用人格名称指代，100字符以内）
        :param agent_personality_desc: 性格描述（身世背景，影响性格的重要事件，体现性格的典型表现等。使用人格名称指代。2000字符以内）
        :return: 操作是否成功
        """
        url = f"{self.BASE_API_URL}/agent/edit"
        headers = self._get_headers()
        
        data = {
            "agentId": agent_id
        }
        
        if agent_name is not None:
            data["agentName"] = agent_name
        if agent_hobby is not None:
            data["agentHobby"] = agent_hobby
        if agent_identity is not None:
            data["agentIdentity"] = agent_identity
        if agent_personality_desc is not None:
            data["agentPersonalityDesc"] = agent_personality_desc
        
        try:
            response = requests.post(url, json=data, headers=headers)
            result = self._handle_response(response, "编辑人格")
            return result is not None
        except requests.RequestException as e:
            logger.error(f"编辑人格 - 网络错误: {e}")
            return False
            
    def get_agent(self, agent_id: str) -> Optional[Dict]:
        """
        查询人格的所有属性信息
        :param agent_id: 人格ID
        :return: 成功时返回人格信息字典，失败时返回None
        """
        url = f"{self.BASE_API_URL}/agent/get-agent/{agent_id}"
        headers = self._get_headers()
        
        try:
            response = requests.get(url, headers=headers)
            result = self._handle_response(response, "查询人格")
            if result:
                return result.get("data")
            return None
        except requests.RequestException as e:
            logger.error(f"查询人格 - 网络错误: {e}")
            return None
    
    def list_agents(self, page_num: int = 1, page_size: int = 15, search_key: str = None, player_id: str = None) -> Optional[Dict]:
        """
        分页搜索人格列表
        :param page_num: 查询页码，默认为1
        :param page_size: 每页条数，默认为15
        :param search_key: 搜索关键词
        :param player_id: 创建玩家ID
        :return: 成功时返回包含人格列表的字典，失败时返回None
        """
        url = f"{self.BASE_API_URL}/agent/list"
        headers = self._get_headers()
        
        data = {
            "pageNum": page_num,
            "pageSize": page_size
        }
        
        if search_key is not None:
            data["searchKey"] = search_key
        
        if player_id is not None:
            data["playerId"] = player_id
        
        try:
            response = requests.post(url, json=data, headers=headers)
            result = self._handle_response(response, "分页搜索人格列表")
            if result:
                return result.get("data")
            return None
        except requests.RequestException as e:
            logger.error(f"分页搜索人格列表 - 网络错误: {e}")
            return None
    
    def delete_agent(self, agent_id: str) -> bool:
        """
        删除人格，且同步删除角色的所有记忆
        :param agent_id: 人格ID
        :return: 操作是否成功
        """
        url = f"{self.BASE_API_URL}/agent/delete/{agent_id}"
        headers = self._get_headers()
        
        try:
            response = requests.post(url, headers=headers)
            result = self._handle_response(response, "删除人格")
            if result and result.get("data", False):
                return True
            return False
        except requests.RequestException as e:
            logger.error(f"删除人格 - 网络错误: {e}")
            return False
    
    def set_relationship(self, player_id: str, agent_id: str, player_nickname: str = None, 
                         player_identity: str = None, agent_nickname: str = None, relationship: str = None) -> bool:
        """
        设置玩家和人格之间的关系、玩家对于人格的身份，以及独属双方的昵称
        :param player_id: 玩家ID
        :param agent_id: 人格ID
        :param player_nickname: 人格对玩家的称呼
        :param player_identity: 玩家对于人格的身份
        :param agent_nickname: 玩家对人格的称呼
        :param relationship: 玩家和人格的关系
        :return: 操作是否成功
        """
        url = f"{self.BASE_API_URL}/agent/set-relationship"
        headers = self._get_headers()
        
        data = {
            "playerId": player_id,
            "agentId": agent_id
        }
        
        if player_nickname is not None:
            data["playerNickname"] = player_nickname
        if player_identity is not None:
            data["playerIdentity"] = player_identity
        if agent_nickname is not None:
            data["agentNickname"] = agent_nickname
        if relationship is not None:
            data["relationship"] = relationship
        
        try:
            response = requests.post(url, json=data, headers=headers)
            result = self._handle_response(response, "设置人格角色关系")
            if result and result.get("data", False):
                return True
            return False
        except requests.RequestException as e:
            logger.error(f"设置人格角色关系 - 网络错误: {e}")
            return False
    
    def get_relationship(self, player_id: str, agent_id: str) -> Optional[Dict]:
        """
        查询玩家和人格之间的关系、玩家对于人格的身份，以及独属双方的昵称
        :param player_id: 玩家ID
        :param agent_id: 人格ID
        :return: 成功时返回关系信息字典，失败时返回None
        """
        url = f"{self.BASE_API_URL}/agent/get-relationship"
        headers = self._get_headers()
        
        data = {
            "playerId": player_id,
            "agentId": agent_id
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            result = self._handle_response(response, "查询人格角色关系")
            if result:
                return result.get("data")
            return None
        except requests.RequestException as e:
            logger.error(f"查询人格角色关系 - 网络错误: {e}")
            return None
    
    def create_chat(self, player_id: str, agent_id: str, mission: str = None, conversation_scene: str = None) -> Optional[str]:
        """
        新建会话，在玩家和角色开始聊天之前，需要创建一个会话实例
        :param player_id: 玩家ID
        :param agent_id: 人格ID
        :param mission: 人格在本会话中的任务或目标
        :param conversation_scene: 会话场景，比如环境、前情提要等
        :return: 成功时返回新增会话ID，失败时返回None
        """
        url = f"{self.BASE_API_URL}/chat/new-chat"
        headers = self._get_headers()
        
        data = {
            "playerId": player_id,
            "agentId": agent_id
        }
        
        if mission is not None:
            data["mission"] = mission
        if conversation_scene is not None:
            data["conversationScene"] = conversation_scene
        
        try:
            response = requests.post(url, json=data, headers=headers)
            result = self._handle_response(response, "新建会话")
            if result:
                return result.get("data")
            return None
        except requests.RequestException as e:
            logger.error(f"新建会话 - 网络错误: {e}")
            return None
            
    def edit_chat_scene(self, chat_id: str, scene: str) -> bool:
        """
        编辑会话场景
        :param chat_id: 会话ID
        :param scene: 新会话场景的描述
        :return: 操作是否成功
        """
        url = f"{self.BASE_API_URL}/chat/add-scene"
        headers = self._get_headers()
        
        data = {
            "chatId": chat_id,
            "scene": scene
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            result = self._handle_response(response, "编辑会话场景")
            if result and result.get("data", False):
                return True
            return False
        except requests.RequestException as e:
            logger.error(f"编辑会话场景 - 网络错误: {e}")
            return False
    
    def chat(self, chat_id: str, player_id: str, agent_id: str, content: str = None, 
             on_message: Callable[[Dict], None] = None, on_error: Callable[[str], None] = None, 
             on_close: Callable[[], None] = None, type: str = "chat") -> bool:
        """
        与角色进行对话
        :param chat_id: 会话ID
        :param player_id: 玩家ID
        :param agent_id: 人格ID
        :param content: 用户发言内容，type为chat时必填
        :param on_message: 接收消息的回调函数
        :param on_error: 错误处理的回调函数
        :param on_close: 连接关闭的回调函数
        :param type: 会话类型，支持"ping"、"chat"、"reanswer"
        :return: 连接是否成功建立
        """
        # 构建WebSocket URL
        timestamp = int(time.time() * 1000)
        signature = self.auth.get_signature(timestamp)
        ws_url = f"wss://ai-character-v2.xfyun.cn/personality/open/chat/{chat_id}/{player_id}/{agent_id}?appId={self.app_id}&timestamp={timestamp}&signature={signature}"
        
        # 准备请求数据
        request_data = {
            "header": {
                "appId": self.app_id
            },
            "parameter": {
                "type": type
            },
            "payload": {}
        }
        
        if type == "chat" and content is not None:
            request_data["payload"]["content"] = content
        
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
                logger.info(f"WebSocket连接已建立，发送{type}消息...")
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
            logger.debug(f"收到WebSocket消息: {message}")
            
            # 检查是否是pong消息
            if data.get("header", {}).get("type") == "pong":
                logger.debug("收到pong消息")
                return
            
            # 调用用户提供的回调函数
            if callback:
                callback(data)
                
            # 检查会话是否完成
            status = data.get("header", {}).get("status")
            if status == 2:
                logger.info("会话已完成")
                # 可以选择在这里关闭连接
                # ws.close()
        except json.JSONDecodeError as e:
            logger.error(f"解析WebSocket消息失败: {e}, 消息内容: {message}")
        except Exception as e:
            logger.error(f"处理WebSocket消息时发生错误: {e}")
    
    def _on_ws_error(self, ws, error, callback):
        """
        处理WebSocket错误
        :param ws: WebSocket对象
        :param error: 错误信息
        :param callback: 用户提供的错误处理回调函数
        """
        logger.error(f"WebSocket错误: {error}")
        if callback:
            callback(str(error))
    
    def _on_ws_close(self, ws, callback):
        """
        处理WebSocket连接关闭
        :param ws: WebSocket对象
        :param callback: 用户提供的连接关闭回调函数
        """
        logger.info("WebSocket连接已关闭")
        if callback:
            callback()
    
    def clear_chat(self, chat_id: str) -> bool:
        """
        清空会话历史，删除角色记忆缓存中的对话历史
        :param chat_id: 会话ID
        :return: 操作是否成功
        """
        url = f"{self.BASE_API_URL}/chat/clear-chat/{chat_id}"
        headers = self._get_headers()
        
        try:
            response = requests.get(url, headers=headers)
            result = self._handle_response(response, "清空会话历史")
            if result and result.get("data", False):
                return True
            return False
        except requests.RequestException as e:
            logger.error(f"清空会话历史 - 网络错误: {e}")
            return False


if __name__ == '__main__':
    # 初始化配置
    conf = Config()
    
    # 初始化角色模拟器
    simulator = CharacterSimulator(conf)
    
    # 创建玩家账号
    logger.info('----------创建玩家账号----------')
    player_name = "测试玩家"
    player_identity = "一个热爱探索AI的学习者"
    player_id = simulator.create_player(player_name, player_identity)
    if player_id:
        logger.info(f"玩家创建成功，ID: {player_id}")
        
        # 创建人格
        logger.info('----------创建人格----------')
        agent_name = "AI助手"
        agent_hobby = "AI助手喜欢学习新知识，探索科技前沿"
        agent_identity = "一个专业的AI助手，擅长解答各类问题"
        agent_personality_desc = "AI助手性格温和，乐于助人，有丰富的知识储备，善于倾听和解答问题"
        agent_id = simulator.create_agent(player_id, agent_name, agent_hobby, agent_identity, agent_personality_desc)
        
        if agent_id:
            logger.info(f"人格创建成功，ID: {agent_id}")
            
            # 设置关系
            logger.info('----------设置玩家和人格关系----------')
            success = simulator.set_relationship(
                player_id=player_id,
                agent_id=agent_id,
                player_nickname="学习者",
                player_identity="知识探索者",
                agent_nickname="小助手",
                relationship="亦师亦友"
            )
            if success:
                logger.info("关系设置成功")
                
                # 创建会话
                logger.info('----------创建会话----------')
                chat_id = simulator.create_chat(
                    player_id=player_id,
                    agent_id=agent_id,
                    mission="帮助用户学习和解答问题",
                    conversation_scene="在线学习场景"
                )
                
                if chat_id:
                    logger.info(f"会话创建成功，ID: {chat_id}")
                    
                    # 定义回调函数
                    def on_message(data):
                        try:
                            content = data.get("content", "")
                            if content:
                                logger.info(f"收到回复: {content}")
                        except Exception as e:
                            logger.error(f"处理回复时发生错误: {e}")
                    
                    def on_error(error):
                        logger.error(f"对话错误: {error}")
                    
                    def on_close():
                        logger.info("对话已结束")
                    
                    # 开始对话
                    logger.info('----------开始对话----------')
                    message = "你好，请介绍一下你自己"
                    logger.info(f"发送消息: {message}")
                    
                    success = simulator.chat(
                        chat_id=chat_id,
                        player_id=player_id,
                        agent_id=agent_id,
                        content=message,
                        on_message=on_message,
                        on_error=on_error,
                        on_close=on_close
                    )
                    
                    if success:
                        logger.info("对话请求已发送，等待回复...")
                        # 等待对话完成
                        import time
                        time.sleep(10)  # 等待10秒钟
                    else:
                        logger.warning("发起对话失败")
                else:
                    logger.error("创建会话失败")
            else:
                logger.error("设置关系失败")
        else:
            logger.error("创建人格失败")
    else:
        logger.error("创建玩家失败")
    
    logger.info("测试完成")