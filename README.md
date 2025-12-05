# Documents API - Сервис хранения документов с версионированием

Мини-сервис для хранения документов с автоматической версионацией, метаданными и моковым AI-анализом.

## Возможности

- Загрузка файлов любых форматов
- Автоматическое версионирование (при загрузке файла с тем же именем)
- Хранение метаданных (размер, дата, версия)
- Mock AI-анализ документов
- REST API с документацией
- SQLite база данных
- Docker поддержка

## Быстрый старт

### Без Docker

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Скопируйте `.env.example` в `.env`:
```bash
cp .env.example .env
```

3. Запустите сервер:
```bash
uvicorn main:app --reload
```

4. Откройте документацию: http://localhost:8000/docs

### С Docker

```bash
docker-compose up --build
```

API будет доступно на http://localhost:8000

## API Endpoints

### 1. Загрузка файла

```
POST /files/upload
Content-Type: multipart/form-data
```

**Параметры:**
- `file`: файл для загрузки

**Ответ:**
```json
{
  "id": 1,
  "original_name": "document.pdf",
  "version": 1,
  "uploaded_at": "2024-01-15T10:00:00",
  "file_size": 20480
}
```

### 2. Список файлов

```
GET /files
```

**Ответ:** массив файлов с метаданными

### 3. Анализ файла

```
POST /files/{file_id}/analyze
```

**Ответ:**
```json
{
  "id": 1,
  "file_id": 1,
  "result": "Файл относительно небольшой, новое изменение...",
  "analyzed_at": "2024-01-15T10:05:00"
}
```

### 4. Получить результат анализа

```
GET /files/{file_id}/analysis
```

## Версионирование

При загрузке файла с существующим именем:
- `plan.pdf` → версия 1
- `plan_v2.pdf` (повторная загрузка) → версия 2
- `plan_v3.pdf` (еще одна загрузка) → версия 3

Все версии сохраняются и доступны.

## Структура проекта

```
docsAPI/
├── main.py              # FastAPI приложение
├── database.py          # Настройка БД
├── models.py            # SQLAlchemy модели
├── schemas.py           # Pydantic схемы
├── ai_service.py        # Mock AI-анализ
├── requirements.txt     # Зависимости
├── Dockerfile           # Docker образ
├── docker-compose.yml   # Docker Compose
├── .env.example         # Пример конфигурации
├── README.md            # Документация
└── storage/             # Хранилище файлов
```

## База данных

SQLite (можно легко заменить на PostgreSQL):

**Таблица files:**
- `id`
- `original_name`
- `version`
- `path`
- `file_size`
- `uploaded_at`
- `uploaded_by`

**Таблица analyses:**
- `id`
- `file_id`
- `result`
- `analyzed_at`

## Примеры использования

### cURL

```bash
# Загрузка
curl -X POST "http://localhost:8000/files/upload" \
  -F "file=@document.pdf"

# Список файлов
curl "http://localhost:8000/files"

# Анализ
curl -X POST "http://localhost:8000/files/1/analyze"

# Получить анализ
curl "http://localhost:8000/files/1/analysis"
```

## Технологии

- **FastAPI** - современный веб-фреймворк
- **SQLAlchemy** - ORM для работы с БД
- **SQLite/aiosqlite** - асинхронная БД
- **Pydantic** - валидация данных
- **Docker** - контейнеризация

## Основные особенности

1. **Версионирование**: автоматически увеличивается при загрузке файла с тем же именем
2. **Метаданные**: сохраняются размер, дата, версия, путь
3. **Mock AI**: не требует OpenAI ключей, генерирует комментарии
4. **REST API**: полная документация доступна по `/docs`
5. **Docker**: готов к деплою
