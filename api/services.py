import requests
import logging

logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = None
CHAT_ID = None


def send_telegram_message(text: str):
    if TELEGRAM_BOT_TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

        requests.post(url, json={
            "chat_id": CHAT_ID,
            "text": text
        })
    else:
        logger.info(f"[FAKE TELEGRAM] {text}")