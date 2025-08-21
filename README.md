# Менеджер задач (Task Manager)

Простое REST API приложение для управления задачами, построенное на FastAPI и PostgreSQL.

## Функциональность

- Создание, просмотр, обновление и удаление задач
- Поддержка статусов задач: created, in progress, completed
- Получение списка всех задач

## Технологии

- **Backend**: FastAPI
- **База данных**: PostgreSQL
- **Тестирование**: pytest
- **Контейнеризация**: Docker + Docker Compose

## Запуск приложения

### С помощью Docker Compose (рекомендуемый способ)

1. Клонируйте репозиторий
2. Запустите приложение:
```bash
 sudo docker-compose up --build
```

Приложение будет доступно по адресу: http://localhost:8000



## API Endpoints

### Создание задачи
params: name: str, description: str, status: 'created', 'in progress', 'completed'
```
GET /create_task?name={name}&description={description}&status={status}
```

### Получение задачи по ID
params: id
```
GET /get_task?id={id}
```

### Получение списка всех задач
params: None
```
GET /get_list_task
```

### Обновление задачи
params: id, name: str, description: str, status: 'created', 'in progress', 'completed'
```
GET /update_task?id={id}&name={name}&description={description}&status={status}
```

### Удаление задачи
params: id
```
GET /delete_task?id={id}
```

## Документация API

После запуска приложения доступна автоматическая документация:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Запуск тестов

Для запуска тестов выполните:

```bash
python -m pytest tests/
```

Тесты покрывают:
- Создание задач с различными статусами
- Получение задач по ID
- Получение списка задач
- Обновление задач
- Удаление задач

## Структура проекта

```
task_manager/
├── app/
│   ├── __init__.py
│   ├── main.py          # Точка входа приложения
│   ├── api.py           # Маршруты API
│   ├── crud.py          # Бизнес-логика
│   ├── schemas.py       # Pydantic схемы
│   ├── models.py        # SQLAlchemy модели
│   └── database.py      # Настройка базы данных
├── tests/
│   └── test_api.py      # Тесты API
├── requirements.txt     # Зависимости Python
├── Dockerfile          # Конфигурация Docker
└── docker-compose.yml  # Docker Compose конфигурация
```

## Переменные окружения

- `DATABASE_URL` - URL для подключения к PostgreSQL (по умолчанию: postgresql+psycopg2://user:password@db:5432/superhero_db)
- `API_TOKEN` - Токен для аутентификации API

## Примечания

- Для всех операций используются GET-запросы с параметрами
- UUID генерируются автоматически при создании задач
- При удалении задачи возвращается информация об удаленной задати
