Цей проєкт реалізує систему обробки заявок з REST API, асинхронними перевірками через Celery та інтеграцією з Redis і PostgreSQL.

---

## 🚀 Як запустити проєкт

1. **Склонуйте репозиторій:**

```bash
git clone <https://github.com/SayHelloRoman/test-project-django-celery.git>
cd <test-project-django-celery>

docker-compose up --build
docker-compose exec web python manage.py migrate
docker-compose ps
```

- web — Django сервер (порт 8000)
- celery_worker — Celery worker для асинхронних задач
- celery_beat — Celery Beat для періодичних задач
- redis — кеш та брокер для Celery
- postgres_db — база даних PostgreSQL

| Метод | Endpoint                     | Опис                                                                                  |
| ----- | ---------------------------- | ------------------------------------------------------------------------------------- |
| POST  | `/api/requests/`             | Створення нової заявки                                                                |
| GET   | `/api/requests/`             | Список всіх заявок (фільтрування за `status` та `source`, сортування за `created_at`) |
| GET   | `/api/requests/<id>/`        | Деталі конкретної заявки                                                              |
| PATCH | `/api/requests/<id>/status/` | Зміна статусу заявки                                                                  |
| GET   | `/api/requests/stats/`       | Статистика заявок: загальна кількість, по статусах та за останні 24 години            |

### ⚡ Особливості
- Захист від дублювання заявок через Redis (10 хвилин на один phone+address)
- Асинхронна перевірка заявок після створення через Celery
- Періодичні задачі для перевірки старих заявок через Celery Beat
- Підготовлено для інтеграції з Telegram Bot API