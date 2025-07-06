from telegram.ext import Application
from tornado.web import RequestHandler, Application as TornadoApp
import os


class HealthHandler(RequestHandler):
    def get(self):
        self.write({"status": "ok", "message": "Bot is alive"})


class PingHandler(RequestHandler):
    def get(self):
        self.write("pong")


def main():
    TOKEN = os.environ.get('BOT_TOKEN')
    PORT = int(os.environ.get('PORT', 8443))

    # Создаем Telegram приложение
    app = Application.builder().token(TOKEN).build()

    # Добавляем хендлеры бота
    app.add_handler(...)

    # Создаем веб-приложение с дополнительными роутами
    web_app = TornadoApp([
        (r"/health", HealthHandler),
        (r"/ping", PingHandler),
        (r"/", PingHandler),  # Главная страница тоже отвечает
    ])

    # Запуск webhook с кастомным приложением
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://django-webhookbotislam-17.onrender.com/{TOKEN}",
        webhook_app=web_app  # Подключаем наше веб-приложение
    )


if __name__ == '__main__':
    main()