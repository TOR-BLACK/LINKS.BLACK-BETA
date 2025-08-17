# DVI ADMIN BACKEND

## СТЕК

- Django
- DRF
- MySQL

## Установка

### .ENV

```
DEVELOPMENT_MODE=
SECRET_KEY=
DEBUG=
ALLOWED_HOSTS=
AUTH_JWT_SECRET=
AUTH_JWT_ALGORITHMS=
CSRF_TRUSTED_ORIGINS= url через пробелы

SENTRY_DSN=

# POSTGRES
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DB_ROOT_PASSWORD=

# REDIS
REDIS_HOST=
REDIS_PORT=

# OPENAI
OPENAI_API_KEY=

# GOOGLE
GOOGLE_OAUTH2_TYPE=
GOOGLE_OAUTH2_PROJECT_ID=
GOOGLE_OAUTH2_PRIVATE_KEY_ID=
GOOGLE_OAUTH2_PRIVATE_KEY=
GOOGLE_OAUTH2_CLIENT_EMAIL=
GOOGLE_OAUTH2_CLIENT_ID=
GOOGLE_OAUTH2_AUTH_URI=
GOOGLE_OAUTH2_TOKEN_URI=
GOOGLE_OAUTH2_AUTH_PROVIDER_X509_CERT_URL=
GOOGLE_OAUTH2_CLIENT_X509_CERT_URL=
GOOGLE_OAUTH2_UNIVERSE_DOMAIN=

# DEEPL
DEEPL_API_KEY=

SWAGGER_API_URL=


```

## СТРУКТУРА ПРОЕКТА

```plaintext
project/
├── etc/                        # Деплой и т.п
│   ├── compose                 
├── src/                       # Бэкенд Django
│   ├── api                         # Апи бэкенд
│   ├── apps                        # Приложения Django
│   ├── core                        # Настройки проекта и утилиты 
│   ├── services                    # Объекты системы

```

## **Запуск проекта**

> docker-compose up -d --build

#### Создать тестовые данные для DVI api

> docker-compose exec django_backend ./manage.py create_test_data

#### Запуск тестов

> docker-compose exec django_backend pytest

## Документация API SWAGGER для DVINFO

> http://localhost:8000/api/v1/dvi-docs/

## Документация API SWAGGER для DV Админ панель

> http://localhost:8000/api/v1/dv-admin-docs/






