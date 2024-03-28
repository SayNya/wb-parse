from datetime import datetime

import asyncpg


async def get_connection(db_name: str, username: str, password: str) -> asyncpg.Connection:
    connection = await asyncpg.connect(user=username, password=password, database=db_name)
    return connection


async def get_product_by_product_id(product_id: int, conn: asyncpg.Connection) -> asyncpg.Record | None:
    async with conn.transaction():
        record = await conn.fetchrow("SELECT * FROM reviews WHERE product_id=$1", product_id)
    return record


async def create_product(product_id: int, conn: asyncpg.Connection):
    async with conn.transaction():
        await conn.execute("INSERT INTO reviews (product_id) VALUES ($1)", product_id)


async def update_last_review_time(product_id: int, time: datetime, conn: asyncpg.Connection):
    async with conn.transaction():
        await conn.execute("UPDATE reviews SET updated_at=$1 WHERE product_id=$2", time, product_id)
