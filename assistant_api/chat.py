import requests
import os
import json
import dashscope
from dotenv import load_dotenv

load_dotenv()  # 这一行会加载同目录下的 .env 文件
# 获取API密钥，确认密钥已正确加载
api_key = os.environ.get('DASHSCOPE_API_KEY')
print('API Key:', api_key)  # 仅用于调试，实际使用时请移除以保护密钥

url = 'http://localhost:8000/assistant/chat'

headers = {"Content-Type": "application/json"}

data = {
    "messages": [
        {"type": "user", "content": '请画出"在我荒瘠的土地上，你是最后的玫瑰"描绘的画面'},
      
    ],
    "llm_config": {
        'model': 'qwen-max',
        'api_key': os.environ.get('DASHSCOPE_API_KEY'),
        'model_server': 'dashscope',
        "generate_config": {}
    },
    "agent_config": {
        'name': 'test',
        'description': 'test assistant',
        'tools': ['image_gen'],
        'instruction': '你是一个绘本创作师'
    },
    "stream": False,
    "use_knowledge": True,
    "uuid_str": "test"
}

response = requests.post(url, headers=headers, data=json.dumps(data))

text = response.text


