import os
import json
from dotenv import load_dotenv
from openai import OpenAI

from weather import get_weather  # 复用你写好的天气函数

load_dotenv()
key = os.environ.get("DEEPSEEK_API_KEY")

client = OpenAI(
    api_key=key,
    base_url="https://api.deepseek.com"
)

# ---------- ① 给模型的"工具说明书" ----------
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询某个地方的实时天气，返回温度和天气描述",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "要查询天气的城市或地区名，比如 Beijing、Nanchang"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

# 用户的真实提问
messages = [
    {"role": "user", "content": "帮我查一下北京现在的天气"},
]

# ================== 真正的 Agent 循环（核心！） ==================
# while 会反复问模型：直到它不再要工具、真正开口回答为止
while True:
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools,
    )
    print("🔍【探针】看一下 create() 到底返回了什么结构：")
    print(resp)
    print("=" * 60)
    msg = resp.choices[0].message

    if msg.tool_calls:
        # 有请求单 → 模型想调工具，我们就真去执行（多个工具也能循环处理）
        print("🔧 模型想调用工具了")
        messages.append(msg)  # 先把"请求单"记进历史

        for tc in msg.tool_calls:
            name = tc.function.name
            args = json.loads(tc.function.arguments)
            print(f"   → 调用 {name}({args})")

            if name == "get_weather":  # 真正的函数分发
                result = get_weather(args["location"])

            messages.append({  # 把执行后的真实结果塞回去
                "role": "tool",
                "tool_call_id": tc.id,
                "content": json.dumps(result),
            })

        continue  # 把结果喂回去，让模型基于真实数据再组织回答
    else:
        # 没有请求单 → 模型直接开口说人话，任务结束
        print("💬 模型直接回答（不需要工具）")
        print("最终回答：", msg.content)
        break
