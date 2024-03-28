from loguru import logger

from src.handler import handle_reviews
from src.main import app, loop


@app.task()
def process_reviews():
    loop.run_until_complete(handle_reviews())


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    logger.info("Setup tasks")
    sender.add_periodic_task(
        30,
        process_reviews.s(),
    )
