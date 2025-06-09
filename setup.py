"""
Setup script for tg_bot_template package.
"""
from setuptools import setup, find_packages

setup(
    name="tg_bot_template",
    version="0.1.0",
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
) 