# -*- coding: utf-8 -*-
import os
import sys
# 获取当前文件的绝对路径
current_dir = os.path.abspath(os.path.dirname(__file__))
# 获取modelscope-agent目录的绝对路径（当前目录的父目录）
parent_dir = os.path.dirname(current_dir)
# 将modelscope-agent目录添加到sys.path
sys.path.append(parent_dir)
# 现在可以正常导入modelscope_agent包中的模块
from modelscope_agent.agents.role_play import RolePlay
from modelscope_agent.memory.memory_with_retrieval_knowledge import MemoryWithRetrievalKnowledge
from modelscope_agent.schemas import Message
from modelscope_agent.tools.dashscope_tools.image_generation import TextToImageTool 
from modelscope_agent.tools.modelscope_tools.text_to_speech_tool import TexttoSpeechTool 
 # 确保这里正确导入

# 配置API密钥
os.environ['MODELSCOPE_API_TOKEN'] = ""
os.environ['DASHSCOPE_API_KEY'] = ""

role_template = '你可以分析用户输入的文本生成图像。'
llm_config = {
    'model': 'qwen-max', 
    'model_server': 'dashscope',
}
function_list = ['image_gen','speech-generation']  # 使用正确的工具名称
bot = RolePlay(function_list=function_list, llm=llm_config, instruction=role_template)

DEFAULT_UUID_HISTORY = "assistant_api/data/history"
storage_path = "assistant_api/data/storage"
memory_history_path = os.path.join(DEFAULT_UUID_HISTORY, 'default_user.json')
memory_agent_name = 'default_memory'
memory = MemoryWithRetrievalKnowledge(storage_path=storage_path,
        name=memory_agent_name,
        memory_path=memory_history_path,
        )
history = memory.get_history()

# 第一轮对话
input_text = '请生成下列引号内文本故事“在一个遥远的森林里,住着一只聪明的小狐狸。”对应的语音描述。'
response = bot.run(input_text, remote=False, print_info=True, history=history)

text = ''
for chunk in response:
    text += chunk

if len(history) == 0:
    memory.update_history(Message(role='system', content=bot.system_prompt))
memory.update_history([
                Message(role='user', content=input_text),
                Message(role='assistant', content=text),
            ])
text = ''
for chunk in response:
    text += chunk
assert isinstance(text, str)

# 第二轮对话
history = memory.get_history()
input_text = "请为我画一只猫"
response = bot.run(input_text, remote=False, print_info=True, history=history)

text = ''
for chunk in response:
    text += chunk
assert isinstance(text, str)

