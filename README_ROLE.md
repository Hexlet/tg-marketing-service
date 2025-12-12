# RBAC (Role-Based Access Control) — Ролевая модель

## Для реализации RBAC использованы встроенные возможности Django-groups и библиотека Django-guardian.

### Установка Django-guardian
По умолчанию добавлена в pyproject.toml устанавливается в виртуальное окружение.

Ручная установка:

```
pip install django-guardian

```
### Настройка settings.py:

```
NSTALLED_APPS = [
......................
    'guardian',
......................
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Основной бекенд аутентификации
    'guardian.backends.ObjectPermissionBackend',  # Бекенд object-level permissions
]

GUARDIAN_RAISE_403 = True  # При ошибке доступа выводить ошибку 403 (опционально)

```

Также настройте middleware для поддержки анонимных запросов:

```
MIDDLEWARE = [
    # ...
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'guardian.middleware.ObjectPermissionMiddleware',             # Обязательно!
]
```
Далее создаются необходимые таблицы баз данных командой миграции:

```
python manage.py migrate guardian
```