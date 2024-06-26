# Wildberries parser

Структура проекта:

- celery_impl: конфигурация селери и задач
- constants: конфигурация проекта
- database: содержит реализацию подключения к БД и методы для запросов
- excel: работа с excel файлом
- handler: верхний слой, который хранит бизнес-логику
- models: содержит pydantic модели
- parser: модуль для парсинга страницы с помощью Selenium
- telegram_bot: модуль для отправки сообщений телеграм ботом
- utils: утильные методы

## Запуск приложения

Для старта приложения необходимо установить зависимости, запустить докер контейнеры с БД и брокером.
```sh
poetry install
docker compose up -d
```
Создать файл .env на подобии .env.example. Тут нужно будет создать телеграм бота, группу, добавить туда бота и прописать токен бота и id группы в .env

Также нужно создать таблицу в БД с названием reviews и колонками:
1. id - уникальный ключ
2. product_id - SKU товаров (integer)
3. updated_at - последнее обновление записи (timestamp, default=now())

Запустить воркер с планировщиком.
```sh
celery -A src.main.app worker -B
```

## Работа приложения

Сначала задача достаёт из excel файла все SKU. Этот этап можно вынести в main и не повторять при каждом запуске задачи, но тогда, если мы захотим обновить файл с SKU, придётся перезапускать программу.

В цикле обрабатываются все id товаров. Сначала из базы данных получаем этот товар. Это необходимо, для запоминания даты последнего отзыва. Если записи с таким product_id нет, создаётся новая.

С помощью Selenium парсится страница с отзывами и достаются все новые рейтинг которых <5. Также на этом этапе мы получаем общий рейтинг товара и его название.

Если у товара появились новые отзывы, то мы обновляем запись в БД, формируем и отправляем сообщение телеграм ботом.
