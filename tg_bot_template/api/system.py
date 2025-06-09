from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """
    Обработчик команды /start.
    """
    await message.answer(
        "Привет! Я бот-шаблон.\n"
        "Доступные команды:\n"
        "/set_info — заполнить профиль\n"
        "/push_the_button — игровая кнопка\n"
        "/rating — рейтинг нажатий"
    )
