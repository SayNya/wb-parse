import os

from dotenv import load_dotenv

load_dotenv()

EXCEL_FILE = os.environ.get("EXCEL_FILE")

DB_NAME = os.environ.get("DB_NAME")
DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")

GROUP_CHAT_ID = os.environ.get("GROUP_CHAT_ID")
BOT_API_TOKEN = os.environ.get("BOT_API_TOKEN")

MESSAGE_HEADER = """*Негативные отзывы*
*Название товара:* {product_name}
*SKU товара:* {product_id}
*Рейтинг товара:* {product_rating}️⭐️
---------------------------------"""

MESSAGE_CONTENT = """*Оценка:* {review_rating}⭐️
*Текст отзыва:* {review_text}
---------------------------------"""

LAST_REVIEW_DATE_XPATH = "/html/body/div[1]/main/div[2]/div/div[2]/div/section/div[2]/div[2]/ul/li[1]/div[1]/div[2]/div/span"

PRODUCT_NAME_XPATH = "/html/body/div[1]/main/div[2]/div/div[2]/div/div[2]/div/div[1]/a/img"
CURRENT_RATING_XPATH = "/html/body/div[1]/main/div[2]/div/div[2]/div/section/div[3]/div/div/div/b"

REVIEW_LIST_XPATH = "/html/body/div[1]/main/div[2]/div/div[2]/div/section/div[2]/div[2]/ul/li"

FEEDBACK_TEXT_XPATH = "./div[2]/p"
FEEDBACK_RATING_XPATH = "./div[1]/div[2]/span"
