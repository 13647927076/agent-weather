import os
from dotenv import load_dotenv
from openai import OpenAI

# 用标准方式从 .env 读 Key
load_dotenv()
key = os.environ.get("DEEPSEEK_API_KEY")

client = OpenAI(
    api_key=key,
    base_url="https://api.deepseek.com"
)

# 多轮对话：messages 一路累积，模型就能"记住"前面说过的话
messages = [
    {"role": "system", "content": "你是一个友好的助手，能用中文简短回答。"},
    {"role": "user", "content": "记住我的名字叫小明。"},
]

resp = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
)
print("第一轮回答：", resp.choices[0].message.content)

# 把模型上一轮的回答也加进消息历史（这是"记忆"的来源）
messages.append({"role": "assistant", "content": resp.choices[0].message.content})
# 再问一个"依赖上文"的问题
messages.append({"role": "user", "content": "我叫什么名字？"})

resp2 = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
)
print("第二轮回答：", resp2.choices[0].message.content)
