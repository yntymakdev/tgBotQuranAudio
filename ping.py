from telegram.ext import Application, CommandHandler, MessageHandler, filters
import tornado.web
import tornado.ioloop
import os


class HealthHandler(tornado.web.RequestHandler):
    def get(self):
        self.write({"status": "ok", "message": "Bot is alive"})


class PingHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("pong")


class WebhookHandler(tornado.web.RequestHandler):
    def initialize(self, telegram_app):
        self.telegram_app = telegram_app

    async def post(self):
        """Обработка webhook от Telegram"""
        try:
            import json
            from telegram import Update

            # Получаем данные от Telegram
            update_data = json.loads(self.request.body.decode())
            update = Update.de_json(update_data, self.telegram_app.bot)

            # Обрабатываем обновление
            await self.telegram_app.process_update(update)

            self.write({"status": "ok"})
        except Exception as e:
            print(f"Ошибка обработки webhook: {e}")
            self.write({"status": "error", "message": str(e)})


def start(update, context):
    """Обработчик команды /start"""
    update.message.reply_text('Привет! Я бот для чтения Корана.')


def echo(update, context):
    """Эхо-обработчик для всех текстовых сообщений"""
    update.message.reply_text(f"Вы написали: {update.message.text}")


def main():
    TOKEN = "8072816097:AAGhI2SLAHbmKpVPhIOHvaIrKT0RiJ5f1So"
    PORT = int(os.environ.get('PORT', 8443))

    # Создаем Telegram приложение
    telegram_app = Application.builder().token(TOKEN).build()

    # Добавляем обработчики
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Создаем веб-приложение
    web_app = tornado.web.Application([
        (r"/health", HealthHandler),
        (r"/ping", PingHandler),
        (r"/", PingHandler),
        (rf"/{TOKEN}", WebhookHandler, {"telegram_app": telegram_app}),
    ])

    # Запуск сервера
    web_app.listen(PORT)
    print(f"Сервер запущен на порту {PORT}")
    print(f"Webhook URL: https://tgbotquranaudio.onrender.com/{TOKEN}")

    # Запуск event loop
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()