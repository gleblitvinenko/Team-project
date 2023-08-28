import os

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
'''Function to start the bot'''
async def start(message: types.Message):
    await message.answer(f"Hello, {message.from_user.first_name}!")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
