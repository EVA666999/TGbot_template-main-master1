"""
Setup script for tg_bot_template package.
"""
from setuptools import setup, find_packages

setup(
    name="tg_bot_template",
    version="0.1.0",
<<<<<<< HEAD
    packages=find_packages(include=["tg_bot_template", "tg_bot_template.*"]),
    package_dir={"tg_bot_template": "tg_bot_template"},
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "aiosqlite",
        "pydantic",
        "pydantic-settings",
        "python-dotenv",
        "aiogram",
        "loguru",
        "pytest",
        "pytest-asyncio",
        "httpx",
    ],
    python_requires=">=3.8",
    test_suite="tests",
=======
    packages=find_packages(),
    install_requires=[
        "aiogram>=2.25.1",
        "sqlalchemy[asyncio]>=2.0.0",
        "alembic>=1.13.1",
        "asyncpg>=0.29.0",
        "pydantic>=2.6.1",
        "pydantic-settings>=2.1.0",
        "aiocache>=0.12.2",
        "loguru>=0.7.2",
        "python-dotenv>=1.0.0",
    ],
>>>>>>> c0ce5bcc81f614ac8b3fb8fcde787513781c2614
) 