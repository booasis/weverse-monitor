import requests
import time
import smtplib
import os
from email.mime.text import MIMEText
from email.utils import formataddr

# ===== 商品页面地址 =====
URL = "https://shop.weverse.io/zh-tw/shop/USD/artists/7/sales/7400"

# ===== 检查间隔（秒）=====
CHECK_INTERVAL = 60  # 每60秒检查一次

# ===== QQ邮箱配置 =====
EMAIL_SENDER = "2215574168@qq.com"
EMAIL_PASSWORD = os.environ["QQ_PASSWORD"]
EMAIL_RECEIVER = "2215574168@qq.com"

headers = {
    "User-Agent": "Mozilla/5.0"
}


def send_email():
    msg = MIMEText("🎉 Weverse 商品已补货！快去购买！", "plain", "utf-8")

    # 正确格式化邮件头
    msg["From"] = formataddr(("Weverse Monitor", EMAIL_SENDER))
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = "Weverse 商品补货提醒"

    server = smtplib.SMTP_SSL("smtp.qq.com", 465)
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_SENDER, [EMAIL_RECEIVER], msg.as_string())
    server.quit()


print("🚀 开始监控...")

while True:
    try:
        response = requests.get(URL, headers=headers)
        html = response.text

        if "SOLD_OUT" in html:
            print("当前状态: SOLD_OUT")

        elif '"status":"SALE"' in html:
            print("🎉 检测到补货！发送邮件...")
            send_email()
            break

        else:
            print("未找到状态字段，可能页面结构变化")

    except Exception as e:
        print("发生错误:", e)


    time.sleep(CHECK_INTERVAL)
