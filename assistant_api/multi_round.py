# -*- coding: utf-8 -*-
import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()  # 这一行会加载同目录下的 .env 文件
# 获取当前文件的绝对路径
current_dir = os.path.abspath(os.path.dirname(__file__))
# 获取agent目录的绝对路径（当前目录的父目录）
parent_dir = os.path.dirname(current_dir)
# 将agent目录添加到sys.path
sys.path.append(parent_dir)

# 现在可以正常导入包中的模块
from modelscope_agent.agents.role_play import RolePlay
from modelscope_agent.memory.memory_with_retrieval_knowledge import MemoryWithRetrievalKnowledge
from modelscope_agent.schemas import Message
from modelscope_agent.tools.dashscope_tools.image_generation import TextToImageTool
from modelscope_agent.tools.modelscope_tools.text_to_speech_tool import TexttoSpeechTool

# 配置API密钥（应该在环境变量中设置，这里仅作为示例）
os.environ['MODELSCOPE_API_TOKEN'] = ""
os.environ['DASHSCOPE_API_KEY'] = ""


# 角色模板定义
role_template = '你是一个儿童绘本创作师，可以按照用户需求生成绘本故事，并且可以利用工具为绘本故事生成图画以及合成语音'

# 模型配置
llm_config = {
    'model': 'qwen-max',  # 确保这里使用正确的模型名称
    'model_server': 'dashscope',
}

# 配置功能列表
function_list = ['image_gen', 'speech-generation']  # 使用正确的工具名称

# 实例化角色扮演代理
bot = RolePlay(function_list=function_list, llm=llm_config, instruction=role_template)

# 存储路径配置
DEFAULT_UUID_HISTORY = "assistant_api/data/history"
storage_path = "assistant_api/data/storage"
memory_history_path = os.path.join(DEFAULT_UUID_HISTORY, 'default_user.json')
memory_agent_name = 'default_memory'

# 实例化记忆系统
memory = MemoryWithRetrievalKnowledge(storage_path=storage_path,
                                      name=memory_agent_name,
                                      memory_path=memory_history_path)

preprompt1='根据用户需求生成绘本故事，限制包括年龄，故事类型，故事大纲，故事寓意，'
# 获取用户输入的故事要求
input_prompt = "请输入您想要的绘本故事主题和要求，供限制的年龄类别如下：“0-3岁，3-4岁，4-6岁，6-10岁，10岁以上。”故事类型供限制的选择为：“尝识认知，社交礼仪，心智解读，趣味四个类别”确定完后生成故事给用户。将按照要求生成的故事输出打印给用户后，支持拥护对故事进行调整。"
input_text = preprompt1+input(input_prompt)

# 获取历史记录
history = memory.get_history()

# 第一轮对话：生成儿童绘本故事
response = bot.run(input_text, remote=False, print_info=True, history=history)

# 处理生成的故事文本
story_text = ''
for chunk in response:
    story_text += chunk

preprompt2='根据用户希望的画风为上述绘本故事生成图画，有四个风格类型供用户选择。具体内容如下：画风一：颜色鲜明，色彩强对比，大面积撞色，造型抽象，比例夸张有记忆点。画风二：水彩风，笔触质感清晰，轻松感黑色线条描边，画面整体治愈系色彩，任务表情夸张。画风三：纯色暖色背景，主体清晰，毛笔粗线条描边、笔触明显，造型简洁，使用几何形状概括。画风四：彩铅风，暖色系，用色和谐治愈、大面积纯色色块、纯白色背景、表情夸张。沟通中确定用户想要的画风故事合理分段生成图片。用户选择的画风为：'
# 接收用户输入的画风
style_input = story_text + preprompt2 + input("请输入您想要的画风：画风一：颜色鲜明，色彩强对比，大面积撞色，造型抽象，比例夸张有记忆点。画风二：水彩风，笔触质感清晰，轻松感黑色线条描边，画面整体治愈系色彩，任务表情夸张。画风三：纯色暖色背景，主体清晰，毛笔粗线条描边、笔触明显，造型简洁，使用几何形状概括。画风四：彩铅风，暖色系，用色和谐治愈、大面积纯色色块、纯白色背景、表情夸张。 ")
image_response = bot.run(style_input, print_info=True,history=history)

text = ''
for chunk in image_response:
    text += chunk
assert isinstance(text, str)

preprompt3='为上述故事按章节生成语音'
# 为每个章节生成语音并保存
speech_input = story_text + preprompt3
speech_response = bot.run(speech_input, print_info=True, history=history)

text = ''
for chunk in speech_response:
    text += chunk
assert isinstance(text, str)


