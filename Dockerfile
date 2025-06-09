FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install poetry

# Copy project files
COPY pyproject.toml poetry.lock ./
COPY tg_bot_template ./tg_bot_template/

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --without lint --no-interaction --no-ansi --no-root

# Set environment variables
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Run the bot
CMD ["python", "-m", "tg_bot_template.bot"]