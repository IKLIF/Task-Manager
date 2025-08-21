FROM python:3.12

WORKDIR /app

# Установка зависимостей отдельным шагом для кэширования
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && \
    apt-get install -y build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Копирование остальных файлов
COPY . .

CMD ["uvicorn", "task_manager.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]