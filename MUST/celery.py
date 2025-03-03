# your_project/celery.py
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MUST.settings')  

# Create a Celery instance
app = Celery('MUST')  

# Configure Celery using Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.broker_connection_retry_on_startup = True

# Configure the Celery beat schedule for periodic tasks
app.conf.beat_schedule = {
    'send-event-reminders': {
        'task': 'events.tasks.send_event_reminder',  # Adjust this to your actual task path
        'schedule': 86400.0,  # 24 hours in seconds
    },
}