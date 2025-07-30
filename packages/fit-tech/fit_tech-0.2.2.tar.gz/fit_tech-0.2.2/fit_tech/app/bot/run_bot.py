import logging
import os
import asyncio
from aiogram import types, Bot, Dispatcher

logger = logging.getLogger(__name__)

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBAPP_BASE_URL = os.getenv("WEBAPP_BASE_URL", "http://127.0.0.1:8000")

if not API_TOKEN:
    logger.error("Переменная окружения TELEGRAM_BOT_TOKEN не задана.")
    exit(1)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def on_startup():
    await bot.set_chat_menu_button(
        menu_button=types.MenuButtonWebApp(
            type="web_app",
            text="Открыть приложение",
            web_app=types.WebAppInfo(url=WEBAPP_BASE_URL)
        )
    )
    await bot.delete_my_commands()
    logger.info("Меню бота настроено — кнопка WebApp установлена.")

async def main():
    await on_startup()

    logger.info("Запуск поллинга бота…")
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.exception(f"Ошибка при работе бота: {e}")