# import os
# import logging
# import asyncio

# from aiogram import Bot, Dispatcher

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# WEBAPP_BASE_URL = os.getenv("WEBAPP_BASE_URL", "http://127.0.0.1:8000")

# if not API_TOKEN:
#     logger.error("Переменная окружения TELEGRAM_BOT_TOKEN не задана.")
#     exit(1)

# bot = Bot(token=API_TOKEN)
# dp = Dispatcher()

# async def main():
#     logger.info("Запускаем Telegram-бота...")
#     await dp.start_polling(bot, skip_updates=True)

# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except (KeyboardInterrupt, SystemExit):
#         logger.info("Бот остановлен.")
