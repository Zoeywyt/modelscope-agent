## 功能

为绘本故事创作编写的接口

## launch service

To launch assistant service, you can use `uvicorn` as the server. Suppose you are in directory of `modelscope-agent`, the command to launch service is:

```
uvicorn assistant_.server:app --reload
```

## use case

Currently, we provide two apis. These two apis may need to associate with `uuid`.

* `chat`: start a conversation use agents.

### chat

To interact with the chat API, you should construct a object like `ChatRequest` on the client side, and then use the requests library to send it as the request body. An example code snippet is as follows:


```Python
url = 'http://localhost:8000/assistant/chat'

# llm config
llm_cfg = {
    'model': 'qwen-max',
    'model_server': 'dashscope',
    'api_key': os.environ.get('DASHSCOPE_API_KEY'),
}
# agent config
agent_cfg = {
    'name': 'test',
    'description': 'test assistant',
    'instruction': 'you are a helpful assistant'
}

#
request = {
    'agent_config': agent_cfg,
    'llm_config': llm_cfg,
    'messages': [
        {'content': '请为我介绍一下modelscope', 'role': 'user'}
    ],
    'uuid_str': 'test',
    'use_knowledge': True # whether to use knowledge
}

response = requests.post(url, json=request)

```

If you want to use `stream` output, you can extract messages like this:

```Python
request = {
    'agent_config': agent_cfg,
    'llm_config': llm_cfg,
    'messages': [
        {'content': '请为我介绍一下modelscope', 'role': 'user'}
    ],
    'uuid_str': 'test',
    'stream': True, # whether to use stream
    'use_knowledge': True
}

response = requests.post(url, json=request)

# extract message
if response.encoding is None:
    response.encoding = 'utf-8'

for line in response.iter_lines(decode_unicode=True):
    if line:
        print(line)
```

test_assistant.py 为测试绘本调用image_gen与speech-generation工具的文件示例

multi_round.py 为编写绘本多轮对话文件示例

chat.py为使用接口并调用工具创作绘本的文件示例
