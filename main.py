from fastapi import FastAPI
from weather import get_weather

app = FastAPI()

@app.get("/")
def home():
    return {"message": "天气服务已启动"}


@app.get("/weather/{city}")
def weather(city):
    print("服务器收到请求了！城市是:", city)  # ← 加这一行
    return get_weather(city)
