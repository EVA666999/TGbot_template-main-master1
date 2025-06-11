from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
import httpx
from pydantic import BaseModel
from typing import Optional, List
from .config import get_settings
import uvicorn
from .domain.entities import User
from .repo.unit_of_work import UnitOfWork
from .repo.user_repo_sqlalchemy import UserRepoSQLAlchemy
from .repo.game_repo_sqlalchemy import GameRepoSQLAlchemy
from .di import session_factory

# Настройка логирования
settings = get_settings()
logger.add(
    f"{settings.LOG_PATH}/bot.log",
    rotation=settings.LOG_ROTATION,
    retention=settings.LOG_RETENTION,
    level=settings.LOG_LEVEL,
    encoding="utf-8",
    enqueue=True,
    backtrace=True,
    diagnose=True
)

app = FastAPI(title="Telegram Bot API")

class Message(BaseModel):
    """Модель сообщения"""
    chat_id: int
    text: str

class Update(BaseModel):
    """Модель обновления от Telegram"""
    update_id: int
    message: Optional[dict] = None
    callback_query: Optional[dict] = None

class UserInfo(BaseModel):
    """Модель информации о пользователе"""
    user_id: int
    info: str

class ButtonPress(BaseModel):
    """Модель нажатия кнопки"""
    user_id: int

class UserProfile(BaseModel):
    """Модель профиля пользователя"""
    user_id: int
    name: str
    info: str

async def process_message(message: dict) -> str:
    """Обработка сообщения (та же логика, что и в боте)"""
    chat_id = message["chat"]["id"]
    text = message.get("text", "")
    
    # Проверка на создателя бота
    if settings.CREATOR_ID and chat_id == settings.CREATOR_ID:
        return "Привет, создатель!"
    
    # Обработка команд
    if text.startswith("/"):
        command = text.split()[0][1:]
        if command == "start":
            return "Добро пожаловать в главное меню"
        elif command == "help":
            return "Бот для соревнования по тыканью по кнопке. Тыкай в кнопку и побеждай!"
        else:
            return f"Получена команда: {command}"
    else:
        return f"Получено сообщение: {text}"

@app.get("/")
async def root():
    """Проверка работоспособности API"""
    return {"status": "ok", "message": "Bot is running"}

@app.post("/webhook")
async def webhook(request: Request):
    """Обработчик вебхуков от Telegram"""
    try:
        # Получаем данные от Telegram
        update = await request.json()
        
        # Проверяем токен вебхука
        if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != settings.TG_WEBHOOK_TOKEN:
            return JSONResponse(status_code=403, content={"error": "Invalid webhook token"})
        
        # Обрабатываем сообщение
        if "message" in update:
            message = update["message"]
            chat_id = message["chat"]["id"]
            text = message.get("text", "")
            
            # Проверка на создателя бота
            if settings.CREATOR_ID and chat_id == settings.CREATOR_ID:
                response_text = "Привет, создатель!"
            else:
                # Простая обработка команд
                if text.startswith("/"):
                    command = text.split()[0][1:]
                    if command == "start":
                        response_text = "Добро пожаловать в главное меню"
                    elif command == "help":
                        response_text = "Бот для соревнования по тыканью по кнопке. Тыкай в кнопку и побеждай!"
                    else:
                        response_text = f"Получена команда: {command}"
                else:
                    response_text = f"Получено сообщение: {text}"
            
            # Отправляем ответ
            async with httpx.AsyncClient() as client:
                await client.post(
                    f"https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": response_text
                    }
                )
        
        return JSONResponse(content={"status": "ok"})
        
    except Exception as e:
        logger.error(f"Ошибка при обработке вебхука: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/send_message")
async def send_message(message: Message):
    """Отправка сообщения через бота"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendMessage",
                json={
                    "chat_id": message.chat_id,
                    "text": message.text
                }
            )
            
            if response.status_code == 200:
                return JSONResponse(content={"status": "ok"})
            else:
                raise HTTPException(status_code=400, detail="Ошибка отправки сообщения")
                
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/user/{user_id}")
async def get_user(user_id: int):
    """Получение информации о пользователе"""
    try:
        uow = UnitOfWork(session_factory=session_factory)
        async with uow as session:
            repo = UserRepoSQLAlchemy(session)
            user = await repo.get_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return {
                "user_id": user.id,
                "info": user.info
            }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при получении информации о пользователе: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/info")
async def get_info():
    """Получение информации о боте"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/getMe"
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=400, detail="Ошибка получения информации о боте")
                
    except Exception as e:
        logger.error(f"Ошибка при получении информации о боте: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_updates")
async def get_updates(offset: Optional[int] = None, limit: Optional[int] = 100):
    """Получение обновлений от Telegram"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/getUpdates",
                params={
                    "offset": offset,
                    "limit": limit
                }
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=400, detail="Ошибка получения обновлений")
                
    except Exception as e:
        logger.error(f"Ошибка при получении обновлений: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process_update")
async def process_update(update: Update):
    """Обработка обновления от Telegram"""
    try:
        if update.message:
            response_text = await process_message(update.message)
            
            async with httpx.AsyncClient() as client:
                await client.post(
                    f"https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendMessage",
                    json={
                        "chat_id": update.message["chat"]["id"],
                        "text": response_text
                    }
                )
            
            return JSONResponse(content={"status": "ok", "response": response_text})
        else:
            return JSONResponse(content={"status": "ok", "message": "No message in update"})
            
    except Exception as e:
        logger.error(f"Ошибка при обработке обновления: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/push_the_button")
async def push_the_button(button_press: ButtonPress):
    """Обработка нажатия кнопки"""
    try:
        uow = UnitOfWork(session_factory=session_factory)
        async with uow as session:
            repo = GameRepoSQLAlchemy(session)
            taps = await repo.increment_taps(button_press.user_id)
            total_taps = await repo.get_total_taps()
            return {
                "user_id": button_press.user_id,
                "taps": taps,
                "total_taps": total_taps
            }
    except Exception as e:
        logger.error(f"Ошибка при обработке нажатия кнопки: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/set_info")
async def set_info(profile: UserProfile):
    """Установка информации о пользователе"""
    try:
        uow = UnitOfWork(session_factory=session_factory)
        async with uow as session:
            repo = UserRepoSQLAlchemy(session)
            user = User(id=profile.user_id, name=profile.name, info=profile.info)
            await repo.save(user)
            return {
                "user_id": profile.user_id,
                "name": profile.name,
                "info": profile.info
            }
    except Exception as e:
        logger.error(f"Ошибка при установке информации: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/profile/{user_id}")
async def get_profile(user_id: int):
    """Получение профиля пользователя"""
    try:
        uow = UnitOfWork(session_factory=session_factory)
        async with uow as session:
            repo = UserRepoSQLAlchemy(session)
            user = await repo.get_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return {
                "user_id": user.id,
                "name": user.name,
                "info": user.info
            }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при получении профиля: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/rating/{user_id}")
async def get_rating(user_id: int):
    """Получение рейтинга пользователя"""
    try:
        uow = UnitOfWork(session_factory=session_factory)
        async with uow as session:
            repo = GameRepoSQLAlchemy(session)
            user_taps = await repo.get_taps(user_id)
            total_taps = await repo.get_total_taps()
            return {
                "user_id": user_id,
                "user_taps": user_taps,
                "total_taps": total_taps,
                "rank": 1  # TODO: Добавить расчет ранга
            }
    except Exception as e:
        logger.error(f"Ошибка при получении рейтинга: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Запускаем сервер без SSL
    uvicorn.run(app, host="127.0.0.1", port=settings.API_PORT, ssl_keyfile=None, ssl_certfile=None) 