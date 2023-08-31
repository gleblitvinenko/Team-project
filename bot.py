import os

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

from managers.item_category import ItemCategory
from managers.user import User
from templates.inline_buttons import generate_inline_markup

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)

user_data = {}

user = User()


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    if not user.user_exists(message.from_user.id):
        user.create_user(message.from_user.id)
        await message.answer(
            f"Welcome, {message.from_user.username}! Let's get to know you better."
        )
        await message.answer("Please provide your first name:")
        user_data[message.from_user.id] = {"state": "waiting_first_name"}


@dp.message_handler(
    lambda message: user_data.get(message.from_user.id, {}).get("state")
    == "waiting_first_name"
)
async def get_first_name(message: types.Message):
    user_data[message.from_user.id]["first_name"] = message.text
    user.update_profile(message.from_user.id, first_name=message.text)
    await message.answer("Great! Now please provide your last name:")
    user_data[message.from_user.id]["state"] = "waiting_last_name"


@dp.message_handler(
    lambda message: user_data.get(message.from_user.id, {}).get("state")
    == "waiting_last_name"
)
async def get_last_name(message: types.Message):
    user_data[message.from_user.id]["last_name"] = message.text
    user.update_profile(message.from_user.id, last_name=message.text)
    await message.answer("Awesome! Now please provide your phone number:")
    user_data[message.from_user.id]["state"] = "waiting_phone_number"


@dp.message_handler(
    lambda message: user_data.get(message.from_user.id, {}).get("state")
    == "waiting_phone_number"
)
async def get_phone_number(message: types.Message):
    user_data[message.from_user.id]["phone_number"] = message.text
    user.update_profile(message.from_user.id, phone_number=message.text)
    await message.answer("Thank you! Your profile is complete.")
    user_data[message.from_user.id]["state"] = "complete"


@dp.message_handler(commands=["test_categories"])
async def test_categories(message: types.Message):
    """TEST FUNCTION"""
    item_categories_manager = ItemCategory()
    item_categories_list = item_categories_manager.get_titles()
    item_categories_markup = generate_inline_markup(item_categories_list, row_width=2)
    await message.answer("Here is categories", reply_markup=item_categories_markup)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
