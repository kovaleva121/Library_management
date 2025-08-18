from __future__ import absolute_import, unicode_literals
import os
from celery.schedules import crontab
from celery import Celery
import config.settings

# Установка переменной окружения для настроек проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создание экземпляра объекта Celery
app = Celery('config')

# Загрузка настроек из файла Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение и регистрация задач из файлов tasks.py в приложениях Django
app.autodiscover_tasks()

# Настройка периодических задач
# config/celery.py

app.conf.beat_schedule = {
    'send-upcoming-reminders': {
        'task': 'library.tasks.send_upcoming_due_reminders',
        'schedule': crontab(hour=9),  # Каждый день в 9 утра
    },
    'send-overdue-notifications': {
        'task': 'library.tasks.send_overdue_notifications',
        'schedule': crontab(hour=9),  # Каждый день в 9 утра
    },
}
app.conf.timezone = config.settings.TIME_ZONE
