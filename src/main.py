import asyncio

from src.celery_impl import create_celery

TASKS = ('src.celery_impl.reviews',)

loop = asyncio.get_event_loop()
app = create_celery(tasks=TASKS)
