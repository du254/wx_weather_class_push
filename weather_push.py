import os
import requests

# 从环境变量中读取密钥
app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
template_id = "DP6-B-LjIP8GKDVbkjl5IeT8nJbmON6NHsA1qKQB-qQ"   # 你的模板ID
user_id = os.environ["USER_ID_1"]

def get_weather():
    # 越南西宁省安和 Trảng Bàng 坐标
    url = "https://api.open-meteo.com/v1/forecast?latitude=11.05&longitude=106.25&daily=weather_code,precipitation_probability_max,temperature_2m_max,temperature_2m_min&timezone=Asia/Ho_Chi_Minh"
    
    # 获取天气数据
    response = requests.get(url).json()
    data = response['daily']
    
    # 【已修复】统一获取今天（索引为 0 ）的数据，避免今天和明天的数据混淆
    rain_prob = data['precipitation_probability_max'][0]
    temp_min = data['temperature_2m_min'][0]
    temp_max = data['temperature_2m_max'][0]
    
    return {
        "city": "越南西宁省安和 Trảng Bàng",
        "temp": f"{temp_min}~{temp_max}°C",
        "rain": f"{rain_prob}%",
        "tip": "今天可能下雨，出门记得带伞！" if rain_prob > 40 else "天气不错，祝你愉快！"
    }

def send_wechat():
    # 1. 获取微信 Access Token
    token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    token_res = requests.get(token_url).json()
    token = token_res.get("access_token")
    
    if not token:
        print("❌ 错误：获取微信 Token 失败！请检查后台的 APP_ID 和 APP_SECRET 是否正确。微信返回：", token_res)
        return
    
    # 2. 获取整理好的天气数据
    weather = get_weather()
    
    # 3. 发送模板消息
    url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token}"
    
    # 【已修复】严格对应你微信后台的模板变量名：first, keyword1, keyword2, keyword3, remark
    body = {
        "touser": user_id,
        "template_id": template_id,
        "data": {
            "first": {
                "value": "🌦️ 西宁安和天气提醒\n", 
                "color": "#173177"
            },
            "keyword1": {
                "value": weather["city"], 
                "color": "#173177"
            },
            "keyword2": {
                "value": weather["temp"], 
                "color": "#173177"
            },
            "keyword3": {
                "value": weather["rain"], 
                "color": "#FF0000" if "可能下雨" in weather["tip"] else "#173177"
            },
            "remark": {
                "value": f"\n{weather['tip']}", 
                "color": "#FF1493"
            }
        }
    }
    
    # 4. 打印最终的推送结果
    result = requests.post(url, json=body).json()
    print("====== 微信服务器返回结果 ======")
    print(result)
    print("================================")

# 执行函数
if __name__ == "__main__":
    send_wechat()
