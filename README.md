# its-grade

Клонирование репозитория:
``` Bash
git clone -c http.sslVerify=false https://github.com/ghoulsss/websocket-chat-test.git
```

## Запуск в контейнере
Запуск сервиса и БД с помощью Docker:
``` Bash
docker compose -f .\docker-compose.yaml up --build -d
```

## Локально
Установка poetry:
``` Bash
pip install poetry
```
Создание окружения и установка необходимых пакетов:
``` Bash

[//]: # (cd .\src\)
poetry install
```

[//]: # (Параметры БД для ее создания находятся в ```src/core/config.py```   )

Применение миграций:
``` Bash
poetry run alembic upgrade head
```

Локальный запуск сервиса:
``` Bash
poetry run py main.py
```

## Прекоммит:
``` Bash
poetry run ruff check --fix
poetry run ruff format

[//]: # (poetry run mypy .)
```
# weboscket-chat
# websock-chat
