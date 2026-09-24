import requests
import json


def get_weather(location):
    http = f'https://wttr.in/{location}?format=j1'
    response = requests.get(http)
    data = json.loads(response.text)  # 文本 → 字典
    current = data['current_condition'][0]  # 进列表取第1项
    temp = current['temp_C']  # 温度
    desc = current['weatherDesc'][0]['value']  # 天气描述
    return {'location': location, 'temp': temp, 'desc': desc}


if __name__ == "__main__":
    print(get_weather('Jiangxi'))
