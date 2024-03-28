import asyncio
from concurrent.futures import ThreadPoolExecutor

import asyncpg
from dotenv import load_dotenv
from loguru import logger

from src.constants import EXCEL_FILE, DB_NAME, DB_USERNAME, DB_PASSWORD, GROUP_CHAT_ID, MESSAGE_HEADER, MESSAGE_CONTENT
from src.database import get_product_by_product_id, create_product, update_last_review_time
from src.excel import get_product_ids
from src.parser import parse_product
from src.telegram_bot import send_message_to_group

load_dotenv()


async def handle_reviews():
    logger.info("Start process reviews")

    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor(max_workers=5)

    db_pool = await asyncpg.create_pool(
        database=DB_NAME,
        user=DB_USERNAME,
        password=DB_PASSWORD
    )

    logger.info("Get product ids")
    product_ids = get_product_ids(EXCEL_FILE, first_row=True)

    for product_id in product_ids:
        logger.info(f"Process {product_id=}")
        async with db_pool.acquire() as connection:

            record = await get_product_by_product_id(product_id, connection)
            if not record:
                logger.warning(f"Add new product to database {product_id=}")
                await create_product(product_id, connection)
                continue

            product_details, new_reviews, last_date = await loop.run_in_executor(
                executor,
                parse_product,
                product_id,
                record["updated_at"]
            )
            if not new_reviews:
                logger.warning(f"There are no new reviews for the product {product_id=}")
                continue

            await update_last_review_time(product_id, last_date, connection)

            message = MESSAGE_HEADER.format(
                product_name=product_details.name,
                product_id=product_details.id,
                product_rating=product_details.rating
            )
            for review in new_reviews:
                message += "\n"
                message += MESSAGE_CONTENT.format(
                    review_rating=review.rating,
                    review_text=review.text,
                )

            logger.info(f"Send notifications for the product {product_id=}")
            await send_message_to_group(GROUP_CHAT_ID, message)

    executor.shutdown()
    logger.info("Processing finished")

if __name__ == '__main__':
    asyncio.run(handle_reviews())
