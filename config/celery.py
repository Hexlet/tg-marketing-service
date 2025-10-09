from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Устанавливаем переменную окружения, чтобы Celery знал, где искать настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создаем экземпляр приложения Celery
app = Celery('config')

# Загружаем конфигурацию из настроек Django.
# namespace='CELERY' означает, что все настройки Celery в settings.py
# должны начинаться с префикса CELERY_ (например, CELERY_BROKER_URL)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживаем и регистрируем задачи из всех файлов tasks.py
# в установленных Django-приложениях.
app.autodiscover_tasks()
