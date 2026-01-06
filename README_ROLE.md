# RBAC (Role-Based Access Control) — Ролевая модель и права доступа

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

или

```
make migrate
```

### Основные модули ролевой модели:
* config/settings.py - глобальная переменная USER_ROLES с набором ролей;
* config/mixin.py - набор классов обеспечивающих распределение прав;
* user/middleware.py - обеспечиват встаку роли в request запрос;


Для получения роли из request запроса на ходу:

```
role = request.role
```

Для получения роли через модель используеться стандартный API работы с сущностями.

### перечень ролей в базе данных

roles = [
    {'code': 'guest', 'name': 'Guest'},
    {'code': 'user', 'name': 'User'},
    {'code': 'partner', 'name': 'Partner'},
    {'code': 'channel_moderator', 'name': 'Channel Moderator'},
];


## Контроль прав реализован с помощью Django-guardian

В стандартную панель администратора Django добавлен раздел контроля прав.
* Заходим в объект парв (пользователь, группа, канал и т.д.) в верхнем правом углу отображаеться кнопка контроля прав, кликаем попадаем в соответсующий раздел.  