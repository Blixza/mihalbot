import asyncio
import logging
import os
import random
import json
from dotenv import load_dotenv, dotenv_values
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultPhoto, InputFile

load_dotenv("secret.env")

TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    raise Exception("No token")

bot = Bot(token=TOKEN)
dp = Dispatcher()

folder = 'images'
files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

mapping = {f: os.path.splitext(f)[0] for f in files}

with open('images.json', 'r', encoding='utf-8') as f:
    mapping = json.load(f)

async def main():
    await dp.start_polling(bot)

@dp.inline_query()
async def inline_echo(inline_query: InlineQuery):
    text = inline_query.query or ''
    filename, description = random.choice(list(mapping.items()))
    input_content = InputTextMessageContent(message_text=description)
    result_id: str = '1'
    item = InlineQueryResultPhoto(
        id=result_id,
        photo_url=InputFile(filename=f'images/{filename}'),
        thumbnail_url='',
        title='Узнай какой михал ты сегодня!',
        input_message_content=input_content,
    )

    await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)

if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.DEBUG)
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')