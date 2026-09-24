import json
from weather import get_weather
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
key = os.environ.get("DEEPSEEK_API_KEY")
client = OpenAI(api_key=key, base_url="https://api.deepseek.com")

messages = [{"role": "user", "content": "帮我查一下北京的天气"}]

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
                        "description": "要查询天气的城市或地区名"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

while True:
    resp = client.chat.completions.create(model="deepseek-chat", messages=messages, tools=tools)
    msg = resp.choices[0].message

    if msg.tool_calls:
        messages.append(msg)
        for tc in msg.tool_calls:
            name = tc.function.name
            args = json.loads(tc.function.arguments)
            if name == "get_weather":
                result = get_weather(args["location"])
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": json.dumps(result)})
        continue
    else:
        print("最终回答：", msg.content)
        break
