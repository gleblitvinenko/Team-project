import os

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

from managers.item_category import ItemCategory
from managers.user import User
from templates.inline_buttons import share_phone_number_inline
from templates.inline_buttons import generate_inline_markup

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)

user_data = {}

user = User()


# ToDo: make Profile inline button prototype

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    if not user.user_exists(message.from_user.id):
        user.create_user(message.from_user.id)
        await message.answer(f"Welcome, {message.from_user.username}!")
    else:
        await message.answer(f"Welcome to the shop, {message.from_user.username}!")
    phone_number = user.check_field(message.from_user.id, "phone_number")
    if not phone_number:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(text=share_phone_number_inline, request_contact=True))

        await message.answer("Please share your phone number with me.", reply_markup=keyboard)
    else:
        profile_button = types.InlineKeyboardMarkup(row_width=1)
        profile_button.add(types.InlineKeyboardButton(text="Profile", callback_data="profile"))
        await message.answer("Here is your menu", reply_markup=profile_button)


@dp.message_handler(
    content_types=types.ContentType.CONTACT,
)
async def get_phone_number(message: types.Message):
    user.update_profile(message.from_user.id, phone_number=message.contact.phone_number)

    await message.answer("Thank you! Your phone number has been saved.", reply_markup=types.ReplyKeyboardRemove())
    await start(message)


@dp.callback_query_handler(lambda query: query.data.startswith("profile"))
async def profile_menu(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    data = callback_query.data

    if data == "profile":
        nested_markup = types.InlineKeyboardMarkup(row_width=1)

        first_name_button = types.InlineKeyboardButton(text="Add/Change First Name", callback_data="profile_first_name")
        last_name_button = types.InlineKeyboardButton(text="Add/Change Last Name", callback_data="profile_last_name")
        phone_number_button = types.InlineKeyboardButton(text="Add/Change Phone Number",
                                                         callback_data="profile_phone_number")
        exit_button = types.InlineKeyboardButton(text="Exit", callback_data="profile_exit")

        nested_markup.add(first_name_button, last_name_button, phone_number_button, exit_button)

        await bot.edit_message_text(
            chat_id=user_id,
            message_id=callback_query.message.message_id,
            text="Profile options:",
            reply_markup=nested_markup,
        )


@dp.message_handler(commands=["test_categories"])
async def test_categories(message: types.Message):
    """TEST FUNCTION"""
    item_categories_manager = ItemCategory()
    item_categories_list = item_categories_manager.get_titles()
    item_categories_markup = generate_inline_markup(item_categories_list, row_width=2)
    await message.answer("Here is categories", reply_markup=item_categories_markup)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
