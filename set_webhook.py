import requests

TOKEN = "8072816097:AAGhI2SLAHbmKpVPhIOHvaIrKT0RiJ5f1So"
WEBHOOK_URL = "https://tgbotquranaudio-7.onrender.com/"

# Устанавливаем Webhook для Telegram
response = requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}")
print(response.json())