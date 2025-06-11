from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger
from typing import Optional

scheduler: Optional[AsyncIOScheduler] = None

def get_scheduler() -> AsyncIOScheduler:
    """
    Возвращает экземпляр асинхронного планировщика APScheduler.
    """
    global scheduler
    if scheduler is None:
        scheduler = AsyncIOScheduler()
    return scheduler

async def healthcheck() -> None:
    """Периодическая задача для проверки работоспособности бота."""
    logger.info("Healthcheck: бот работает!")
    # Здесь можно отправить сообщение админу или выполнить другую задачу
