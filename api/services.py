import requests
from django.conf import settings

def send_telegram_message(message):
    if settings.TG_BOT_TOKEN and settings.TG_CHAT_ID:
        url = f"https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": settings.TG_CHAT_ID, "text": message})
    else:
        print(f"[NOTIFICATION]: {message}")