import json
import time
import requests
import hashlib
import base64
import hmac
import websocket
import ssl
import logging
import os
import _thread as thread
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
from requests_toolbelt.multipart.encoder import MultipartEncoder
from urllib.parse import urlencode

# Configure logging
logger = logging.getLogger(__name__)

# Config class for API credentials
class Config:
    """Configuration class for Voice Synthesis API"""
    def __init__(self, appid, apikey, apisecret):
        self.XF_APPID = appid
        self.XF_APIKEY = apikey
        self.XF_APISECRET = apisecret

# Authentication utilities
class AuthUtils:
    @staticmethod
    def get_authorization(appId, apikey, timeStamp, data):
        """Generate authorization signature"""
        body = json.dumps(data)
        keySign = hashlib.md5((apikey + str(timeStamp)).encode('utf-8')).hexdigest()
        sign = hashlib.md5((keySign + body).encode("utf-8")).hexdigest()
        return sign

    @staticmethod
    def get_token(appid, apikey):
        """Get authentication token from API"""
        timeStamp = int(time.time() * 1000)
        body = {"base": {"appid": appid, "version": "v1", "timestamp": str(timeStamp)}, "model": "remote"}
        headers = {}
        headers['Authorization'] = AuthUtils.get_authorization(appid, apikey, timeStamp, body)
        headers['Content-Type'] = 'application/json'
        
        try:
            response = requests.post(
                url='http://avatar-hci.xfyousheng.com/aiauth/v1/token', 
                data=json.dumps(body), 
                headers=headers
            ).text
            resp = json.loads(response)
            if ('000000' == resp['retcode']):
                return resp['accesstoken']
            else:
                logger.error(f"Failed to get token: {resp}")
                return None
        except Exception as e:
            logger.error(f"Error getting token: {e}")
            return None

# Model management utilities
class ModelManager:
    @staticmethod
    def save_model(model_id, model_name, config_file):
        """Save voice model ID to the config file"""
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    models = json.load(f)
            else:
                models = {}
            
            models[model_name] = model_id
            
            with open(config_file, 'w') as f:
                json.dump(models, f, indent=4)
            
            logger.info(f"Voice model {model_name} (ID: {model_id}) saved to config file.")
            return True
        except Exception as e:
            logger.error(f"Error saving voice model: {e}")
            return False

    @staticmethod
    def get_model(model_name, config_file):
        """Get voice model ID from the config file"""
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    models = json.load(f)
                
                if model_name in models:
                    return models[model_name]
            
            return None
        except Exception as e:
            logger.error(f"Error loading voice model: {e}")
            return None

# Voice Training Class
class VoiceTrainer:
    def __init__(self, config):
        """Initialize voice trainer with configuration"""
        self.appid = config.XF_APPID
        self.apikey = config.XF_APIKEY
        self.token = AuthUtils.get_token(config.XF_APPID, config.XF_APIKEY)
        self.time = int(time.time() * 1000)
        self.taskId = ''

    def getSign(self, body):
        keySign = hashlib.md5((str(body)).encode('utf-8')).hexdigest()
        sign = hashlib.md5((self.apikey + str(self.time) + keySign).encode("utf-8")).hexdigest()
        return sign

    def getheader(self, sign):
        return {"X-Sign": sign, "X-Token": self.token, "X-AppId": self.appid, "X-Time": str(self.time)}

    def getText(self):
        textid = 5001  # 通用的训练文本集
        body = {"textId": textid}
        sign = self.getSign(body)
        headers = self.getheader(sign)

        response = requests.post(
            url='http://opentrain.xfyousheng.com/voice_train/task/traintext',
            json=body,
            headers=headers
        ).json()
        print("请使用以下官方文本录音，然后进行训练：")
        textlist = response['data']['textSegs']
        for line in textlist:
            print(f"{line['segId']}: {line['segText']}")
        return textlist

    def createTask(self, taskName="VoiceClone", sex=1, resourceName="创建音库"):
        body = {
            "taskName": taskName,  # 任务名称，可自定义
            "sex": sex,  # 训练音色性别   1：男     2：女
            "resourceType": 12,
            "resourceName": resourceName,  # 音库名称，可自定义
            "language": "cn",  # 不传language参数，默认中文；英：en、日：jp、韩：ko、俄：ru
        }
        sign = self.getSign(body)
        headers = self.getheader(sign)
        response = requests.post(
            url='http://opentrain.xfyousheng.com/voice_train/task/add',
            json=body,
            headers=headers
        ).text
        resp = json.loads(response)
        print("创建任务：", resp)
        return resp['data']

    def addAudiofromPC(self, textId, textSegId, path, taskName="VoiceClone", sex=1):
        url = 'http://opentrain.xfyousheng.com/voice_train/task/submitWithAudio'
        self.taskId = self.createTask(taskName=taskName, sex=sex)
        
        # 构造body体
        formData = MultipartEncoder(
            fields={
                "file": (path, open(path, 'rb'), 'audio/wav'),
                "taskId": str(self.taskId),
                "textId": str(textId),
                "textSegId": str(textSegId)
            }
        )

        sign = self.getSign(formData)
        headers = self.getheader(sign)
        headers['Content-Type'] = formData.content_type
        response = requests.post(url=url, data=formData, headers=headers).text
        print(response)
        return response

    def submitTask(self):
        body = {"taskId": self.taskId}
        sign = self.getSign(body)
        headers = self.getheader(sign)
        response = requests.post(
            url='http://opentrain.xfyousheng.com/voice_train/task/submit', 
            json=body, 
            headers=headers
        ).text
        print(response)
        return response

    def getProcess(self):
        body = {"taskId": self.taskId}
        sign = self.getSign(body)
        headers = self.getheader(sign)
        response = requests.post(
            url='http://opentrain.xfyousheng.com/voice_train/task/result', 
            json=body, 
            headers=headers
        ).text
        return response

# TTS WebSocket Parameters
class Ws_Param(object):
    def __init__(self, APPID, APIKey, APISecret, Text, res_id):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.Text = Text

        # 公共参数(common)
        self.CommonArgs = {"app_id": self.APPID, "res_id": res_id, "status": 2}
        # 业务参数(business)
        self.BusinessArgs = {
            "tts": {
                "rhy": 1,
                "vcn": "x5_clone",  # 固定值
                "volume": 50,  # 设置音量大小
                "rhy": 0,
                "pybuffer": 1,
                "speed": 50,  # 设置合成语速，值越大，语速越快
                "pitch": 50,  # 设置振幅高低，可通过该参数调整效果
                "bgs": 0,
                "reg": 0,
                "rdn": 0,
                "audio": {
                    "encoding": "lame",  # 合成音频格式
                    "sample_rate": 16000,  # 合成音频采样率
                    "channels": 1,
                    "bit_depth": 16,
                    "frame_size": 0
                },
                "pybuf": {
                    "encoding": "utf8",
                    "compress": "raw",
                    "format": "plain"
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

# TTS WebSocket Exception
class AssembleHeaderException(Exception):
    def __init__(self, msg):
        self.message = msg

# TTS WebSocket URL class
class Url:
    def __init__(self, host, path, schema):
        self.host = host
        self.path = path
        self.schema = schema

# TTS WebSocket Functions
def sha256base64(data):
    sha256 = hashlib.sha256()
    sha256.update(data)
    digest = base64.b64encode(sha256.digest()).decode(encoding='utf-8')
    return digest

def parse_url(requset_url):
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

def assemble_ws_auth_url(requset_url, method="GET", api_key="", api_secret=""):
    u = parse_url(requset_url)
    host = u.host
    path = u.path
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))
    
    signature_origin = f"host: {host}\ndate: {date}\n{method} {path} HTTP/1.1"
    signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                             digestmod=hashlib.sha256).digest()
    signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
    authorization_origin = f'api_key="{api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha}"'
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
    
    values = {
        "host": host,
        "date": date,
        "authorization": authorization
    }

    return requset_url + "?" + urlencode(values)

# WebSocket Utility classes
class WebSocketUtils:
    """Utility functions for WebSocket operations"""
    @staticmethod
    def dummy():
        pass

# TTS WebSocket callbacks
def on_message(ws, message):
    try:
        message = json.loads(message)
        code = message["header"]["code"]
        sid = message["header"]["sid"]
        
        if "payload" in message:
            audio = message["payload"]["audio"]['audio']
            audio = base64.b64decode(audio)
            status = message["payload"]['audio']["status"]
            
            if status == 2:
                print("WebSocket closed")
                ws.close()
            
            if code != 0:
                errMsg = message["message"]
                print(f"sid:{sid} call error:{errMsg} code is:{code}")
            else:
                # Use the output_path from WebSocket's user_data instead of hardcoded path
                output_path = ws.user_data.get('output_path', './output.mp3')
                with open(output_path, 'ab') as f:
                    f.write(audio)
                    print(f'写入完成: {output_path}')
    except Exception as e:
        print(f"Receive message error: {e}")

def on_error(ws, error):
    print(f"WebSocket error: {error}")

def on_close(ws, ts, end):
    pass

def on_open(ws, wsParam):
    def run(*args):
        d = {
            "header": wsParam.CommonArgs,
            "parameter": wsParam.BusinessArgs,
            "payload": wsParam.Data,
        }
        d = json.dumps(d)
        print("------>开始发送文本数据")
        ws.send(d)
        
        # Use the output_path from WebSocket's user_data instead of hardcoded path
        output_path = ws.user_data.get('output_path', './output.mp3')
        if os.path.exists(output_path):
            os.remove(output_path)

    thread.start_new_thread(run, ())

# Main Voice Synthesis class
class VoiceSynthesis:
    """Main class for voice training and text-to-speech synthesis"""
    
    def __init__(self, config, stream=False):
        """Initialize with config
        
        Args:
            config: Config object with API credentials
            stream: Whether to use streaming mode for synthesis (not implemented yet)
        """
        self.config = config
        self.stream = stream
        self.output_path = "./output.mp3"
        self.appid = config.XF_APPID
        self.apikey = config.XF_APIKEY
        self.apisecret = config.XF_APISECRET
        
    def train_model(self, audio_path, model_name="default_voice", text_id=5001, text_seg_id=1, voice_model_config=None):
        """Train a new voice model
        
        Args:
            audio_path: Path to the audio file for training
            model_name: Name for the voice model
            text_id: Text ID for training
            text_seg_id: Text segment ID for training
            
        Returns:
            model_id: ID of the trained model or None if failed
        """
        logger.info(f"Training new voice model: {model_name}")
        
        # Initialize voice training
        trainer = VoiceTrainer(self.config)
        
        # Get training text (optional, just to display)
        trainer.getText()
        
        # Add audio to training task if audio_path is provided
        if audio_path:
            trainer.addAudiofromPC(textId=text_id, textSegId=text_seg_id, path=audio_path)
        else:
            logger.info("No audio path provided, proceeding with training without audio")
        
        # Submit training task
        trainer.submitTask()
        
        # Wait for training to complete
        while True:
            response = trainer.getProcess()
            resp = json.loads(response)
            status = resp['data']['trainStatus']
            
            if status == -1:
                logger.info("Training in progress, please wait...")
                time.sleep(5)  # Wait 5 seconds before checking again
            elif status == 1:
                logger.info("Training successful")
                model_id = resp['data']['assetId']
                # Save the model ID
                ModelManager.save_model(model_id, model_name, voice_model_config)
                return model_id
            elif status == 0:
                logger.error("Training failed. Please use official training text recordings.")
                return None
    
    def synthesize(self, text, model_name="default_voice", output_path=None, voice_model_config=None):
        """Synthesize text to speech using a trained model
        
        Args:
            text: Text to convert to speech
            model_name: Name of the voice model to use
            output_path: Path to save the output MP3
            
        Returns:
            Path to the output file or None if failed
        """
        if output_path:
            self.output_path = output_path
            
        # Get model ID
        model_id = ModelManager.get_model(model_name, voice_model_config)
        if not model_id:
            logger.error(f"Model '{model_name}' not found. Please train it first.")
            return None
            
        logger.info(f"Synthesizing text using model: {model_name} (ID: {model_id})")
        
        # Initialize WebSocket parameters
        wsParam = Ws_Param(
            APPID=self.appid, 
            APISecret=self.apisecret,
            APIKey=self.apikey, 
            Text=text, 
            res_id=model_id
        )
        
        # Create WebSocket URL
        requrl = 'wss://cn-huabei-1.xf-yun.com/v1/private/voice_clone'
        wsUrl = assemble_ws_auth_url(requrl, "GET", self.apikey, self.apisecret)
        
        # Setup WebSocket callbacks
        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(
            wsUrl,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )
        
        # Add custom on_open that includes wsParam
        def custom_on_open(ws):
            on_open(ws, wsParam)
        
        ws.on_open = custom_on_open
        
        # Store the output path in WebSocket's user_data for callbacks to access
        ws.user_data = {'output_path': self.output_path}
        
        # Run WebSocket
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        
        logger.info(f"Speech synthesis completed. Output saved to {self.output_path}")
        return self.output_path
        
    def generate(self, params):
        """Main method for batch synthesis (similar to multi_lang.py interface)
        
        Args:
            params: Dictionary with parameters:
                - text: Text to synthesize
                - model_name: Name of the voice model
                - output_path: Path to save output
                - audio_path: Path to audio file (only for training)
                - force_train: Whether to train even if model exists
                - voice_model_config: Path to voice model configuration file
                
        Returns:
            Path to the output file or None if failed
        """
        text = params.get('text', "")
        model_name = params.get('model_name', "default_voice")
        output_path = params.get('output_path', self.output_path)
        audio_path = params.get('audio_path', None)
        force_train = params.get('force_train', False)
        voice_model_config = params.get('voice_model_config', "voice_models.json")
        
        # If force_train or no model exists, train model (even if audio_path is empty)
        model_id = ModelManager.get_model(model_name, voice_model_config)
        if force_train or model_id is None:
            logger.info(f"Training model '{model_name}'{' using audio: ' + audio_path if audio_path else ' without audio'}")
            model_id = self.train_model(audio_path, model_name, voice_model_config=voice_model_config)
            if not model_id:
                return None
        
        # Synthesize text
        return self.synthesize(text, model_name, output_path, voice_model_config)

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # 初始化配置
    conf = Config()
    
    # 批式调用示例
    logger.info('----------批式调用----------')
    model = VoiceSynthesis(conf, stream=False)
    
    # Example 1: Using an existing model
    # params = {
    #     'text': "全红婵，2007年3月28日出生于广东省湛江市，中国国家跳水队女运动员，主项为女子10米跳台。",
    #     'model_name': "my_voice_model",
    #     'output_path': './output1.mp3'
    # }
    
    # result = model.generate(params)
    # logger.info(f"Result: {result}")
    
    # Example 2: Training and synthesizing
    params_with_training = {
        'text': "欢迎使用讯飞星火认知大模型。",
        'model_name': "new_model",
        'audio_path': './test.wav',
        # 'force_train': True,  # Force retraining
        'output_path': './new_output.mp3',
        'voice_model_config': 'voice_models.json'  # Add this to params
    }
    
    # Uncomment to run training and synthesis
    result = model.generate(params_with_training)
    logger.info(f"Training and synthesis result: {result}")
