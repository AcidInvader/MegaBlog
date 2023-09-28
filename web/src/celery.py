import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')

app = Celery('src')
# Загрузка настроек из файла settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')
# Автоматическое обнаружение и регистрация задач из файлов tasks.py приложений Django
app.autodiscover_tasks()
