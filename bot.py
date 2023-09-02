import asyncio
import os

from aiogram.filters import Command

from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from managers.item import Item
from managers.item_category import ItemCategory
from managers.user import User
from templates.inline_buttons import generate_inline_markup, share_phone_number_inline

load_dotenv()

user = User()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot=bot, storage=MemoryStorage())


# ToDo: make Profile inline button prototype


async def check_get_phone_number(message: types.Message):
    phone_number = user.check_field(message.from_user.id, "phone_number")
    if not phone_number:
        kb = [
            [types.KeyboardButton(text=share_phone_number_inline, request_contact=True)]
        ]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=kb)
        await message.answer(
            "Please share your phone number with me.", reply_markup=keyboard
        )


@dp.message(Command("start"))
async def start(message: types.Message):
    if not user.user_exists(message.from_user.id):
        user.create_user(message.from_user.id)
        await message.answer(f"Welcome to the shop, {message.from_user.username}!")
    else:
        await message.answer(f"Welcome back, {message.from_user.username}!")
    await check_get_phone_number(message)


@dp.message(F.contact)
async def set_phone_number(message: types.Message):
    user.update_profile(message.from_user.id, phone_number=message.contact.phone_number)
    await message.answer(
        "Thank you! Your phone number has been saved.",
        reply_markup=types.ReplyKeyboardRemove(),
    )


async def main():
    # await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
# @dp.message_handler(commands=["start"])
# async def start(message: types.Message):
#     markup = types.InlineKeyboardMarkup(row_width=1)
#     profile_button = types.InlineKeyboardButton(text="Profile", callback_data="profile")
#     markup.add(profile_button)
#     if not user.user_exists(message.from_user.id):
#         user.create_user(message.from_user.id)
#     phone_number = user.check_field(message.from_user.id, "phone_number")
#     if not phone_number:
#         keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         keyboard.add(
#             types.KeyboardButton(text=share_phone_number_inline, request_contact=True)
#         )
#
#         await message.answer(
#             "Please share your phone number with me.", reply_markup=keyboard
#         )
#     else:
#         await message.answer(
#             f"Welcome, {message.from_user.username}!", reply_markup=markup
#         )
#

# @dp.message_handler(
#     content_types=types.ContentType.CONTACT,
# )
# async def get_phone_number(message: types.Message):
#     user.update_profile(message.from_user.id, phone_number=message.contact.phone_number)
#
#     await message.answer(
#         "Thank you! Your phone number has been saved.",
#         reply_markup=types.ReplyKeyboardRemove(),
#     )


# @dp.message_handler(commands=["test_categories"])
# async def test_categories(message: types.Message):
#     """TEST FUNCTION"""
#     item_categories_manager = ItemCategory()
#     item_categories_list = item_categories_manager.get_titles()
#     item_categories_markup = generate_inline_markup(
#         item_categories_list, row_width=2, button_type="category"
#     )
#     await message.answer("Here is categories", reply_markup=item_categories_markup)
#
#
# @dp.callback_query_handler(lambda query: "_cb_data" in query.data)
# async def show_items_based_on_category(callback_query: types.CallbackQuery):
#     """HANDLER FOR ITEMS & ITEM CATEGORY BUTTONS"""
#     item_manager = Item()
#     if callback_query.data.endswith("_cat_cb_data"):
#         category_title = callback_query.data.split("_", 1)[0]
#
#         item_titles_list = item_manager.get_items_titles_list_by_category_title(
#             category_title=category_title
#         )
#         items_markup = generate_inline_markup(
#             button_titles=item_titles_list, row_width=2, button_type="item"
#         )
#         await bot.send_message(
#             callback_query.from_user.id,
#             text=f"{callback_query.data.split('_', 1)[0]} category items",
#             reply_markup=items_markup,
#         )
#     elif callback_query.data.endswith("_item_cb_data"):
#         item_title = callback_query.data.split("_", 1)[0]
#         item_details_dict = item_manager.get_item_details_dict_by_item_title(
#             item_title=item_title
#         )
#         await bot.send_message(
#             callback_query.from_user.id,
#             text=f"""
# ℹ️ Item Title: {item_details_dict.get("title")}
#
# 🆔 ID: {item_details_dict.get("id")}
#
# 💰 Price: {item_details_dict.get("price")}
# """,
#         )


# executor.start_polling(dp, skip_updates=True)
