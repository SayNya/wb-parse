import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.constants import PRODUCT_NAME_XPATH, CURRENT_RATING_XPATH, LAST_REVIEW_DATE_XPATH, REVIEW_LIST_XPATH, \
    FEEDBACK_RATING_XPATH, FEEDBACK_TEXT_XPATH
from src.models import ReviewModel, ProductModel
from src.utils import parse_date


def parse_product(product_id: int, last_review_time: datetime) -> tuple[ProductModel, list[ReviewModel], datetime]:
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    driver.get(f"https://www.wildberries.ru/catalog/{product_id}/feedbacks")

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "comments__list"))
    )

    product_name = driver.find_element(By.XPATH, PRODUCT_NAME_XPATH).get_attribute("alt")
    current_rating = driver.find_element(By.XPATH, CURRENT_RATING_XPATH).text
    product_model = ProductModel(
        id=product_id,
        name=product_name,
        rating=current_rating
    )

    last_review_date = parse_date(driver.find_element(By.XPATH, LAST_REVIEW_DATE_XPATH).text)

    new_review_count = 0
    while True:
        date_elements = element.find_elements(By.CLASS_NAME, "feedback__date")

        last_loaded_date = parse_date(date_elements[-1].text)

        if last_review_time >= last_loaded_date:
            for date_idx, date_element in enumerate(date_elements):
                parsed_date = parse_date(date_element.text)
                if parsed_date < last_review_time:
                    new_review_count = date_idx
                    break
            break
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    reviews = []

    review_list = driver.find_elements(By.XPATH, REVIEW_LIST_XPATH)[:new_review_count]

    for review_element in review_list:
        feedback_rating = (
            review_element
            .find_element(By.XPATH, FEEDBACK_RATING_XPATH)
            .get_attribute("class")
            .split()[2][-1]
        )
        if feedback_rating == '5':
            continue

        feedback_text = review_element.find_element(By.XPATH, FEEDBACK_TEXT_XPATH).text

        reviews.append(
            ReviewModel(
                text=feedback_text,
                rating=feedback_rating
            )
        )

    driver.close()
    return product_model, reviews, last_review_date
