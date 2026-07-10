import os
import requests

print("=== 开始测试 ===")

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
user_id = os.environ["USER_ID_1"]

# 获取token
token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
token_resp = requests.get(token_url).json()
print("Token结果:", token_resp)

token = token_resp.get("access_token")

# 发送客服消息
url = f"https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={token}"
body = {
    "touser": user_id,
    "msgtype": "text",
    "text": {
        "content": "✅ 测试消息\n越南西宁安和天气推送已配置成功！\n当前时间：2026年7月\n如果看到这条消息，说明配置完成。"
    }
}

result = requests.post(url, json=body).json()
print("最终发送结果:", result)
