# Telegram Bot Template

## Структура проекта

```
tg_bot_template/
├── api/              # Роутеры и хендлеры aiogram (user, game, system)
│   ├── game.py
│   ├── user.py
│   └── system.py
├── bot_content/      # Текстовые константы, кнопки, описания фич, ошибки
│   ├── features.py
│   ├── errors.py
│   └── __init__.py
├── db_infra/         # SQLAlchemy-модели и инфраструктура БД
│   └── models.py
├── domain/           # Бизнес-логика, use cases, сервисы, сущности
│   ├── entities.py
│   ├── game_service.py
│   ├── user_service.py
│   └── __init__.py
├── repo/             # Репозитории (интерфейсы и реализации), Unit of Work
│   ├── game_repo_sqlalchemy.py
│   ├── user_repo_sqlalchemy.py
│   ├── unit_of_work.py
│   └── __init__.py
├── scheduler.py      # Планировщик задач (APScheduler)
├── di.py             # DI-контейнер: engine, session_factory, UoW, сервисы
├── bot.py            # Точка входа, запуск aiogram-бота
├── config.py         # Конфиги, переменные окружения, настройки
└── __init__.py
```

## Описание слоёв

- **api/** — только роутеры и хендлеры aiogram. Не содержит бизнес-логики.
- **bot_content/** — текстовые шаблоны, кнопки, описания команд, ошибки.
- **db_infra/** — только SQLAlchemy-модели, без логики.
- **domain/** — бизнес-логика, use cases, сервисы, сущности (dataclass, pydantic).
- **repo/** — репозитории, Unit of Work, только работа с БД, без бизнес-логики.
- **scheduler.py** — отдельный модуль для планировщика задач (APScheduler).
- **di.py** — связывает все слои, реализует dependency injection (engine, session_factory, UoW, сервисы).
- **bot.py** — точка входа, инициализация aiogram, запуск бота.
- **config.py** — конфиги, переменные окружения, настройки.

