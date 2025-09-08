# 📚 Library API

REST API для управления библиотекой: авторы, книги, жанры, выдача, аутентификация. Реализовано на Django + DRF с архитектурной прозрачностью, JWT-защитой и полной документацией через Swagger/OpenAPI.


# 🚀 Быстрый старт

# 🔧 Требования

- Docker + Docker Compose
- Python 3.11 (только для локальной разработки)
- PostgreSQL (в контейнере)

# 📦 Установка bash
'''
git clone https://github.com/your-username/library-api.git
cd library-api
cp .env.example .env  # или настрой свой .env
docker-compose up --build
'''

# После запуска:
'''
API доступен на: http://localhost:8000

Swagger UI: http://localhost:8000/api/docs/

OpenAPI-схема: http://localhost:8000/api/schema/
'''

# Переменные окружения (.env)
'''
DEBUG=True
SECRET_KEY=your-secret-key

DB_NAME=library
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=db
DB_PORT=5432

EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=your-email-password

ALLOWED_HOSTS=127.0.0.1,localhost
'''
# 🧱 Архитектура
Backend: Django 5.2 + Django REST Framework

База данных: PostgreSQL

Аутентификация: JWT (djangorestframework-simplejwt)

Документация: Swagger UI + OpenAPI (drf-spectacular)

Инфраструктура: Docker + Docker Compose

Организация кода:

catalog/ — книги, авторы, жанры

users/ — регистрация, авторизация, профиль

config/ — настройки проекта
# 🔐 Аутентификация

Метод	URL	Описание
GET	/api/catalog/authors/	Список авторов
POST	/api/catalog/authors/	Создать автора
GET	/api/catalog/books/	Список книг
POST	/api/catalog/books/	Создать книгу
GET	/api/catalog/books/{id}/	Получить книгу по ID
GET	/api/catalog/genres/	Список жанров
GET	/api/catalog/issued/	Выданные книги текущего пользователя
Полная документация доступна в Swagger UI.

# 📄 Документация API
Swagger UI: /api/docs/

OpenAPI-схема: /api/schema/

Генерация вручную:
python manage.py spectacular --file schema.yml
# 🧠 Архитектурные принципы
Прозрачность: все зависимости и конфигурации вынесены в .env

Воспроизводимость: проект запускается одной командой через Docker

Безопасность: JWT, IsAuthenticated, защита эндпоинтов

Документированность: Swagger + OpenAPI

Масштабируемость: структура проекта готова к расширению

# 📦 Дополнительно
Возможность интеграции с Celery, Redis, Stripe — при необходимости

Поддержка фильтрации, поиска, пагинации

Возможность генерации клиента по OpenAPI (openapi-generator)

# 🧑‍🎓 Автор
Пестов Максим — инженер-архитектор, автор дипломного проекта. 
Проект разработан с акцентом на архитектурную честность, воспроизводимость и прозрачность.