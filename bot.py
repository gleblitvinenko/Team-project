import os

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

from managers.user import User

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user = User(message.from_user.id)
    await message.answer("Start")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
