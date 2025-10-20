### Инструкция по локальному развертыванию и тестированию

**Цель:** Запустить проект и проверить работу API для поиска Telegram-каналов.

#### Часть 1: Установка и настройка

1.  **Клонировать репозиторий:**

    - Открой терминал и выполни:
      ```sh
      git clone https://github.com/IvanFoksha/tg-marketing-service
      cd tg-marketing-service/
      ```

2.  **Установить системные зависимости:**

    - **Python, Node.js, Git:** Убедись, что они установлены.
    - **PostgreSQL и Redis:** Выполни в терминале:
      ```sh
      sudo apt update
      sudo apt install postgresql postgresql-contrib redis-server -y
      ```

3.  **Создать и настроить базу данных:**

    - Запусти сервис PostgreSQL:
      ```sh
      sudo service postgresql start
      ```
    - Войди в консоль `psql`:
      ```sh
      sudo -u postgres psql
      ```
    - Внутри `psql` выполни команды (замени `'пароль'` на свой):
      ```sql
      CREATE DATABASE marketing_db;
      CREATE USER marketing_user WITH PASSWORD 'пароль';
      GRANT ALL PRIVILEGES ON DATABASE marketing_db TO marketing_user;
      \q
      ```

4.  **Настроить переменные окружения (`.env`):**

    - Найди файл `env.example` и создай его копию с названием `.env`.
    - Открой `.env` и заполни его **обязательными** значениями:

      ```env
      # Основные настройки
      SECRET_KEY=любая_случайная_строка
      DEBUG=True

      # Настройки базы данных
      NAMEDB=marketing_db
      USERDB=marketing_user
      PASSWORDDB=пароль_который_ты_придумал
      HOSTDB=localhost
      PORTDB=5432

      # Настройки Telegram API (получить на my.telegram.org)
      TELEGRAM_API_ID=...
      TELEGRAM_API_HASH=...
      PHONE=+7...
      ```

    - Поле `TELEGRAM_SESSION_STRING` пока оставь пустым.

5.  **Установить зависимости проекта:**

    - Создай и активируй виртуальное окружение:
      ```sh
      python3 -m venv .venv
      source .venv/bin/activate
      ```
    - Установи Python-пакеты (включая `uv`, если его нет):
      ```sh
      pip install uv
      uv pip install -r requirements.txt
      ```
    - Установи Node.js-пакеты:
      ```sh
      cd frontend
      npm install
      cd ..
      ```

6.  **Сгенерировать сессию Telegram:**

    - Выполни команду и следуй инструкциям (введи код из Telegram):
      ```sh
      uv run python manage.py set_telegram_session
      ```
    - Скопируй полученную строку и вставь ее в `.env` в поле `TELEGRAM_SESSION_STRING`.

7.  **Применить миграции:**
    - Создай структуру таблиц в новой базе данных:
      ```sh
      uv run python manage.py migrate
      ```

#### Часть 2: Запуск и проверка с Inertia.js

1.  **Запустить все сервисы:**

    - Убедись, что Redis запущен (`sudo service redis-server start`).
    - Открой **три отдельных терминала** в корневой папке проекта (`tg-marketing-service`).
    - **Терминал 1 (Celery):** Активируй окружение (`source .venv/bin/activate`) и запусти: `make celery`
    - **Терминал 2 (Бэкенд):** Активируй окружение (`source .venv/bin/activate`) и запусти: `make dev`
    - **Терминал 3 (Фронтенд):** Перейди в папку `frontend` и запусти: `npm run dev`

2.  **Наполнить базу тестовыми данными:**

    - Создай суперпользователя для доступа к админке (если еще не создан):
      ```sh
      uv run python manage.py createsuperuser
      ```
    - Открой админ-панель: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
    - Войди в "Parser" -> "Categories", "Countries", "Languages" и создай несколько записей (например, Категория: "Технологии", Страна: "Россия" (код RU)).
    - Зайди в "Telegram каналы" и создай 2-3 тестовых канала с разными данными.

3.  **Протестировать вывод данных через Inertia:**

    - **Основной URL для проверки:** [http://127.0.0.1:8000/parser/channels/search/](http://127.0.0.1:8000/parser/channels/search/)

    - **Способ 1: Проверка HTML-ответа (доказательство работы бэкенда):**

      - Открой основной URL в браузере.
      - Нажми `Ctrl+U` (или правый клик -> "Посмотреть исходный код страницы").
      - Найди в коде тег `<div id="app" ...>`.
      - **Ожидаемый результат:** Внутри атрибута `data-page` ты увидишь большую JSON-строку. Она должна содержать ключ `"component": "Channels/SearchPage"` и ключ `"props"`, внутри которого будут твои тестовые каналы. Это подтверждает, что бэкенд отработал верно.

    - **Способ 2: Проверка в инструментах разработчика (проверка работы фронтенда):**
      - Открой основной URL в браузере.
      - Нажми `F12` и перейди на вкладку **"Console"**.
      - **Ожидаемый результат:** В консоли не должно быть красных ошибок, связанных с Inertia или React. Это значит, что JavaScript успешно "подхватил" данные от бэкенда.

4.  **Протестировать фильтры:**

    - Используй разные параметры в URL, чтобы проверить логику фильтрации. После каждого изменения обновляй страницу и смотри на содержимое `data-page` в исходном коде.
      - **Поиск по тексту:** `http://127.0.0.1:8000/parser/channels/search/?q=технологии`
      - **Фильтр по категории:** `http://127.0.0.1:8000/parser/channels/search/?category=1` (используй ID созданной категории)
      - **Фильтр по флагу:** `http://127.0.0.1:8000/parser/channels/search/?verified=true`
      - **Комбинированный запрос:** `http://127.0.0.1:8000/parser/channels/search/?q=новости&country=1`

5.  **Протестировать парсер Telegram-каналов:**

    - **Цель:** Убедиться, что Celery-задача для парсинга работает корректно и все данные (включая фото, username и статус верификации) сохраняются в базу данных.

    - **Действия:**
      1.  **Открой Django shell** в новом терминале (не закрывая остальные):
          ```sh
          uv run python manage.py shell
          ```
      2.  **Запусти задачу парсинга** для любого публичного канала (например, `@durov`):
          ```python
          from config.parser.tasks import parse_channel_task
          parse_channel_task.delay('@durov')
          ```
      3.  **Проверь логи Celery:** В терминале, где запущен `make celery`, ты должен увидеть, что задача была получена (`received`) и успешно выполнена (`succeeded`).
      4.  **Проверь результат в админ-панели:**
          - Перейди в раздел "Parser" -> "Telegram каналы".
          - Найди в списке добавленный канал (например, "Pavel Durov").
          - **Ожидаемый результат:** Все поля должны быть заполнены корректно:
            - `Title`, `Description`, `Subscribers count`.
            - `Is verified` должен стоять флажок (галочка).
            - `Username` должно быть `durov`.
            - `Photo url` должен содержать путь к файлу, например: `media/photos/channel_1006503122.jpg`. Если кликнуть по этому URL (открыв его на `http://127.0.0.1:8000/media/...`), должно отобразиться изображение.

#### Часть 3: Проверка API рейтинга каналов (для 50 issue)

1.  **Открыть документацию API (Swagger):**

    - Перейди по ссылке: [http://127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/)
    - **Ожидаемый результат:** Ты увидишь интерфейс Swagger, в котором будет доступен эндпоинт `GET /parser/api/v1/channels/ratings/`. Через этот интерфейс можно отправлять тестовые запросы.

2.  **Протестировать API напрямую:**

    - Используй следующие URL для проверки фильтрации и сортировки.
      - **Базовый запрос:** `http://127.0.0.1:8000/parser/api/v1/channels/ratings/`
      - **Сортировка по подписчикам (убывание):** `http://127.0.0.1:8000/parser/api/v1/channels/ratings/?ordering=-subscribers_count`
      - **Фильтр по категории (ID=1):** `http://127.0.0.1:8000/parser/api/v1/channels/ratings/?category=1`
    - **Ожидаемый результат:** В ответ должен приходить JSON-массив с данными каналов, соответствующими параметрам запроса.
