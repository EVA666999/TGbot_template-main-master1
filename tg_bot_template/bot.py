"""Main bot module."""
import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
from loguru import logger
from tg_bot_template.api.user import router as user_router
from tg_bot_template.api.game import router as game_router
from tg_bot_template.api.system import router as system_router
from tg_bot_template.scheduler import get_scheduler, healthcheck

# Настройка логирования в файл
logger.add("bot.log", rotation="10 MB", encoding="utf-8", enqueue=True, backtrace=True, diagnose=True)

async def main():
    """Main function to run the bot."""
    # Настройка бота и диспетчера
    load_dotenv()
    token = os.getenv("TG_BOT_TOKEN")
    creator_id = os.getenv("CREATOR_ID")
    if not token:
        raise RuntimeError("TG_BOT_TOKEN not set in .env!")
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(user_router)
    dp.include_router(game_router)
    dp.include_router(system_router)

    logger.info("Бот запущен!")

    # Запуск APScheduler
    scheduler = get_scheduler()
    scheduler.add_job(healthcheck, "interval", seconds=60)  # пример: каждую минуту
    scheduler.start()

    # Отправить сообщение о запуске (один раз)
    if creator_id:
        await bot.send_message(creator_id, "Бот работает ✅")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
