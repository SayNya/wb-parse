from src.constants import CELERY_BROKER_URL

broker_url = CELERY_BROKER_URL

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/Minsk'
enable_utc = True
