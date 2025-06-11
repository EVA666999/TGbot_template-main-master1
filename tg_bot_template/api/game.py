from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from loguru import logger
from ..domain.game_service import GameService
from ..repo.game_repo_sqlalchemy import GameRepoSQLAlchemy
<<<<<<< HEAD
from ..repo.unit_of_work import UnitOfWork
from ..di import session_factory

router = Router()

# Инициализация game_service через DI
async def get_game_service():
    """Получение экземпляра GameService с новой сессией"""
    uow = UnitOfWork(session_factory=session_factory)
    async with uow as session:
        game_repo = GameRepoSQLAlchemy(session)
        return GameService(game_repo)
=======
from tg_bot_template.di import uow

router = Router()
# Инициализация game_service через DI

game_repo = GameRepoSQLAlchemy(uow)
game_service = GameService(game_repo)
>>>>>>> c0ce5bcc81f614ac8b3fb8fcde787513781c2614

def get_button_markup(taps: int = 0) -> InlineKeyboardMarkup:
    """Создать inline-кнопку с количеством нажатий."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"Нажми! ({taps})", callback_data=f"tap:{taps}")]
        ]
    )

def markup_to_dict(markup):
    # Для aiogram 3.x: model_dump, для aiogram 2.x: to_python
    if markup is None:
        return None
    if hasattr(markup, 'model_dump'):
        return markup.model_dump()
    if hasattr(markup, 'to_python'):
        return markup.to_python()
    return str(markup)

@router.message(Command("push_the_button"))
async def push_the_button_cmd(message: Message) -> None:
<<<<<<< HEAD
    """Обработка команды /push_the_button"""
    user_id = message.from_user.id if message.from_user else 0
    logger.info(f"User {user_id} used /push_the_button")
    
    try:
        game_service = await get_game_service()
        taps = await game_service.tap_button(user_id)
        total_taps = await game_service.get_total_taps()
        
        await message.answer(
            f"Нажатий за последнюю сессию: {taps}\nВсего нажатий: {total_taps}",
            reply_markup=get_button_markup(taps)
        )
    except Exception as e:
        logger.error(f"Error in push_the_button_cmd: {e}")
        await message.answer("Произошла ошибка при обработке команды")

@router.callback_query(F.data.startswith("tap:"))
async def process_tap(callback: CallbackQuery) -> None:
    """Обработка нажатия на кнопку"""
    user_id = callback.from_user.id if callback.from_user else 0
    try:
        game_service = await get_game_service()
        taps = await game_service.tap_button(user_id)
        total_taps = await game_service.get_total_taps()
        
        await callback.message.edit_text(
            f"Нажатий за последнюю сессию: {taps}\nВсего нажатий: {total_taps}",
            reply_markup=get_button_markup(taps)
        )
        await callback.answer()
    except Exception as e:
        logger.error(f"Error in process_tap: {e}")
        await callback.answer("Произошла ошибка при обработке нажатия")

@router.message(Command("rating"))
async def rating_cmd(message: Message) -> None:
    """Обработка команды /rating"""
    user_id = message.from_user.id if message.from_user else 0
    try:
        game_service = await get_game_service()
        user_taps = await game_service.get_user_taps(user_id)
        total_taps = await game_service.get_total_taps()
        
        await message.answer(
            f"Всего нажатий твоих: {user_taps}\nВсего нажатий: {total_taps}"
        )
    except Exception as e:
        logger.error(f"Error in rating_cmd: {e}")
        await message.answer("Произошла ошибка при получении рейтинга") 
=======
    """Обработчик команды /push_the_button."""
    logger.info(f"User {message.from_user.id} used /push_the_button")
    user_id = message.from_user.id if message.from_user else 0
    taps = await game_service.get_user_taps(user_id)
    await message.answer("Нажмите на кнопку ниже!", reply_markup=get_button_markup(taps))

@router.callback_query(F.data.startswith("tap:"))
async def button_tap_callback(callback: CallbackQuery) -> None:
    """Обработчик нажатия на inline-кнопку."""
    user_id = callback.from_user.id if callback.from_user else 0
    taps = await game_service.tap_button(user_id)
    logger.info(f"User {user_id} tapped the button {taps} times")
    new_text = f"Кнопка нажата {taps} раз!"
    new_markup = get_button_markup(taps)
    current_markup = callback.message.reply_markup
    if (
        callback.message.text != new_text or
        markup_to_dict(current_markup) != markup_to_dict(new_markup)
    ):
        await callback.message.edit_text(new_text, reply_markup=new_markup)
    await callback.answer("Ещё раз!")

@router.message(Command("rating"))
async def rating_cmd(message: Message) -> None:
    """Обработчик команды /rating."""
    user_id = message.from_user.id if message.from_user else 0
    user_taps = await game_service.get_user_taps(user_id)
    total_taps = await game_service.get_total_taps()
    logger.info(f"User {user_id} requested /rating")
    await message.answer(f"Ваши нажатия: {user_taps}\nВсего нажатий: {total_taps}") 
>>>>>>> c0ce5bcc81f614ac8b3fb8fcde787513781c2614
