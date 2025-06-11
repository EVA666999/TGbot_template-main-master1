"""
Setup script for tg_bot_template package.
"""
from setuptools import setup, find_packages

setup(
    name="tg_bot_template",
    version="0.1.0",
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
) 