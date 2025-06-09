from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from tg_bot_template.di import get_user_service
from loguru import logger

class UserForm(StatesGroup):
    name = State()
    info = State()

router = Router()
user_service = get_user_service()

@router.message(Command("set_info"))
async def set_info_cmd(message: Message, state: FSMContext) -> None:
    """Запросить у пользователя имя для профиля."""
    await message.answer("Введите ваше имя:")
    await state.set_state(UserForm.name)

@router.message(UserForm.name)
async def process_name(message: Message, state: FSMContext) -> None:
    """Сохранить имя и запросить инфо."""
    await state.update_data(name=message.text)
    await message.answer("Введите информацию о себе:")
    await state.set_state(UserForm.info)

@router.message(UserForm.info)
async def process_info(message: Message, state: FSMContext) -> None:
    """Сохранить профиль пользователя через сервис и показать результат."""
    data = await state.get_data()
    name = data.get("name") or ""
    info = message.text or ""
    user_id = message.from_user.id if message.from_user else 0
    await user_service.set_profile(user_id, name, info)
    logger.info(f"User {user_id} set profile: name={name}, info={info}")
    await message.answer(f"Профиль обновлён!\nИмя: {name}\nИнфо: {info}")
    await state.clear()

@router.message(Command("profile"))
async def get_profile_cmd(message: Message) -> None:
    """Показать профиль пользователя."""
    user_id = message.from_user.id if message.from_user else 0
    user = await user_service.get_profile(user_id)
    if user:
        await message.answer(f"Ваш профиль:\nИмя: {user.name}\nИнфо: {user.info}")
    else:
        await message.answer("Профиль не найден. Используйте /set_info для создания профиля.") 