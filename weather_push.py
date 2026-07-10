import os
import requests

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
template_id = "DP6-B-LjIP8GKDVbkjl5IeT8nJbmON6NHsA1qKQB-qQ"   # 新模板ID
user_id = os.environ["USER_ID_1"]

def get_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=11.05&longitude=106.25&daily=weather_code,precipitation_probability_max,temperature_2m_max,temperature_2m_min&timezone=Asia/Ho_Chi_Minh"
    data = requests.get(url).json()['daily']
    rain_prob = data['precipitation_probability_max'][1]
    
    return {
        "city": "越南西宁省安和 Trảng Bàng",
        "temp": f"{data['temperature_2m_min'][0]}~{data['temperature_2m_max'][0]}°C",
        "rain": f"明日降雨概率 {rain_prob}%",
        "tip": "明天可能下雨，记得带伞！" if rain_prob > 40 else "天气不错，祝你愉快！"
    }

def send_wechat():
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    token = requests.get(token_url).json().get("access_token")
    
    weather = get_weather()
    
    url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
    body = {
        "touser": user_id,
        "template_id": template_id,
        "data": {
            "first": {"value": "西宁安和天气提醒"},
            "keyword1": {"value": weather["city"]},
            "keyword2": {"value": weather["temp"]},
            "keyword3": {"value": weather["rain"]},
            "remark": {"value": weather["tip"]}
        }
    }
    result = requests.post(url, json=body)
    print("推送结果：", result.json())

send_wechat()
