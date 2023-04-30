import os

from celery import Celery

from dotenv import load_dotenv

load_dotenv()

# Initialize Celery with Redis as the broker
broker_url = os.getenv("CELERY_BROKER_URL", "redis://:athena@redis:6379/0")
app = Celery("athena", broker=broker_url, backend=broker_url)

app.conf.task_routes = {"athena.tasks.*": {"queue": "athena_tasks"}}
