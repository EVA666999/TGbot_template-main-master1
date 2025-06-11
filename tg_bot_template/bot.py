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
from .config import get_settings

# Настройка логирования в файл
logger.add("bot.log", rotation="10 MB", encoding="utf-8", enqueue=True, backtrace=True, diagnose=True)

async def start_polling():
    """Запуск бота в режиме long polling"""
    settings = get_settings()
    
    # Инициализация бота и диспетчера
    bot = Bot(
        token=settings.TG_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )
    dp = Dispatcher(storage=MemoryStorage())
    
    # Регистрация роутеров
    dp.include_router(system_router)
    dp.include_router(user_router)
    dp.include_router(game_router)
    
    # Запуск планировщика
    scheduler = get_scheduler()
    scheduler.add_job(healthcheck, "interval", seconds=30)
    scheduler.start()
    
    try:
        # Удаляем вебхук перед запуском long polling
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Бот запущен в режиме long polling")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()

def main():
    """Основная функция запуска бота"""
    try:
        asyncio.run(start_polling())
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")

if __name__ == "__main__":
    main()
