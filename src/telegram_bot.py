from aiogram import Bot

from src.constants import BOT_API_TOKEN

bot = Bot(token=BOT_API_TOKEN)


async def send_message_to_group(group_chat_id: int | str, message_text: str):
    await bot.send_message(group_chat_id, message_text, parse_mode="Markdown")
