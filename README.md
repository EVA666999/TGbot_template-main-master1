# Telegram Bot Template

Шаблон для создания Telegram ботов с использованием FastAPI, SQLAlchemy и Redis.

## Структура проекта

```
tg_bot_template/
├── app.py                 # Основной файл приложения FastAPI
├── config.py             # Конфигурация приложения
├── di.py                 # Dependency Injection
├── domain/              # Доменный слой
│   ├── entities.py      # Сущности
│   ├── game_service.py  # Сервис игровой логики
│   └── user_service.py  # Сервис пользователей
├── repo/                # Слой репозиториев
│   └── game_repo_sqlalchemy.py  # Реализация репозитория
├── tests/               # Тесты
│   ├── conftest.py      # Фикстуры для тестов
│   └── test_api.py      # Тесты API
└── requirements.txt     # Зависимости проекта
```

## Требования

- Python 3.8+
- PostgreSQL
- Redis
- Telegram Bot Token
- Telegram API ID и API Hash

## Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd tg_bot_template
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` в корневой директории:
```env
# Environment
ENV=dev
DEBUG=True
LOG_LEVEL=DEBUG
LOG_PATH=logs
LOG_ROTATION=10 MB
LOG_RETENTION=7 days

# Database
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
DB_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}

# Redis
REDIS_URL=redis://localhost:6379/0
FSM_REDIS_HOST=localhost
FSM_REDIS_DB=0
FSM_REDIS_PASS=
FSM_STORAGE=redis

# Telegram
TG_BOT_TOKEN=your_bot_token
TG_WEBHOOK_TOKEN=your_webhook_token
REGISTER_PASSPHRASE=your_passphrase
CREATOR_ID=your_creator_id
API_ID=your_api_id
API_HASH=your_api_hash

# API
API_HOST=0.0.0.0
API_PORT=8000
```

## Запуск

1. Запустите PostgreSQL и Redis

2. Запустите приложение:
```bash
uvicorn tg_bot_template.app:app --reload
```

## API Endpoints

- `POST /users` - Создание нового пользователя
- `GET /users/{user_id}` - Получение информации о пользователе
- `POST /push_the_button` - Нажатие кнопки (увеличивает счетчик taps)

## Тестирование

Запуск тестов:
```bash
pytest
```

## Особенности

- Асинхронная работа с базой данных через SQLAlchemy
- Использование Redis для хранения состояний FSM
- Dependency Injection для управления зависимостями
- Типизация с помощью Pydantic
- Автоматическая валидация конфигурации
- Логирование с помощью loguru
- Тесты с использованием pytest и pytest-asyncio

## Лицензия

MIT

