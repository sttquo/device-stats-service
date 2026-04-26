# Device Stats Service

REST-сервис для сбора и анализа статистики с устройств.

## Стек

- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker / Docker Compose

## Возможности

- создание устройств;
- прием показаний устройства в формате `{"x": float, "y": float, "z": float}`;
- сохранение показаний в БД с временной меткой;
- получение аналитики по устройству за все время;
- получение аналитики по устройству за период;
- расчет минимального значения, максимального значения, количества, суммы и медианы;
- создание пользователей;
- привязка устройств к пользователям;
- получение агрегированной аналитики пользователя.

## Запуск

```bash
docker compose up --build
```

После запуска API доступен по адресу:

```text
http://localhost:8000
```

Swagger-документация:

```text
http://localhost:8000/docs
```

## Основные endpoints

### Пользователи

```text
POST /users/
GET /users/
POST /users/{user_id}/devices/{external_id}
GET /users/{user_id}/analytics
```

### Устройства

```text
POST /devices/
GET /devices/
POST /devices/{external_id}/measurements
GET /devices/{external_id}/analytics
```

## Примеры запросов

### Создать устройство

```bash
curl -X POST http://localhost:8000/devices/ \
  -H "Content-Type: application/json" \
  -d "{\"external_id\":\"device-1\",\"user_id\":null}"
```

### Отправить показания

```bash
curl -X POST http://localhost:8000/devices/device-1/measurements \
  -H "Content-Type: application/json" \
  -d "{\"x\":1.5,\"y\":2.0,\"z\":3.25}"
```

### Получить аналитику устройства

```bash
curl http://localhost:8000/devices/device-1/analytics
```

### Получить аналитику за период

```bash
curl "http://localhost:8000/devices/device-1/analytics?start_at=2026-04-01T00:00:00&end_at=2026-04-30T23:59:59"
```

## Пример ответа аналитики

```json
{
  "x": {
    "min": 1.5,
    "max": 10.0,
    "count": 2,
    "sum": 11.5,
    "median": 5.75
  },
  "y": {
    "min": 2.0,
    "max": 5.0,
    "count": 2,
    "sum": 7.0,
    "median": 3.5
  },
  "z": {
    "min": 3.25,
    "max": 7.5,
    "count": 2,
    "sum": 10.75,
    "median": 5.375
  }
}
```

## Статус проверки

Сервис проверен локально через FastAPI Swagger UI:

- создание устройства;
- отправка показаний;
- получение аналитики за все время;
- получение аналитики за период.

Dockerfile и docker-compose.yml подготовлены для запуска сервиса и PostgreSQL.


