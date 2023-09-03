import asyncio
import os
from aiogram.filters import Command
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from managers.item import Item
from managers.item_category import ItemCategory
from managers.user import User
from templates.inline_buttons import generate_inline_markup
from templates import text_templates as tt

load_dotenv()

user_data = {}
user = User()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot=bot, storage=MemoryStorage())
router = Router()


async def check_get_phone_number(message: types.Message):
    phone_number = user.check_field(message.from_user.id, "phone_number")
    if not phone_number:
        kb = [
            [
                types.KeyboardButton(
                    text=tt.share_phone_number_inline, request_contact=True
                )
            ]
        ]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=kb)
        await message.answer(
            "Please share your phone number with me.", reply_markup=keyboard
        )



@router.message(Command("start"))
async def start(message: types.Message):
    if not user.user_exists(message.from_user.id):
        user.create_user(message.from_user.id)
        await message.answer(text=f"Welcome to the shop,{message.from_user.username}!")
    else:
        await message.answer(text=f"Welcome back,{message.from_user.username}!")
    await check_get_phone_number(message)


@router.message(F.contact)
async def set_phone_number(message: types.Message):
    user.update_profile(
        telegram_id=message.from_user.id, phone_number=message.contact.phone_number
    )
    await message.answer(
        text="Thank you! Your phone number has been saved.",
        reply_markup=types.ReplyKeyboardRemove(),
    )

    
@router.message(Command("test_profile"))
async def profile_inline_button(message: types.Message):
    await message.answer(
        text=tt.profile_inline,
        reply_markup=types.InlineKeyboardMarkup(
            row_width=10,
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=tt.add_change_first_name_inline,
                        callback_data="add_change_first_name_settings",
                    ),
                    types.InlineKeyboardButton(
                        text=tt.add_change_last_name_inline,
                        callback_data="add_change_last_name_settings",
                    ),
                ],
                [
                    types.InlineKeyboardButton(
                        text=tt.add_change_phone_number_inline,
                        callback_data="add_change_phone_number_settings",
                    ),
                ],
            ],
        ),
    )


@router.callback_query(F.data.endswith("_settings"))
async def profile_inline_nested_buttons(callback_query: types.CallbackQuery):
    if callback_query.data.endswith("_first_name_settings"):
        await callback_query.message.answer(
            text="Please enter your first name:",
            reply_markup=types.ForceReply(),
        )
    elif callback_query.data.endswith("_last_name_settings"):
        await callback_query.message.answer(
            text="Please enter your last name:",
            reply_markup=types.ForceReply(),
        )
    elif callback_query.data.endswith("_phone_number_settings"):
        await callback_query.message.answer(
            text="Please enter your phone number:",
            reply_markup=types.ForceReply(),
        )


@router.message(F.reply_to_message)
async def set_profile_field(message: types.Message):
    if message.reply_to_message.text == "Please enter your first name:":
        user.update_profile(message.from_user.id, first_name=message.text)
        await message.answer(
            "Thank you! Your first name has been saved.",
            reply_markup=types.ReplyKeyboardRemove(),
        )
    elif message.reply_to_message.text == "Please enter your last name:":
        user.update_profile(message.from_user.id, last_name=message.text)
        await message.answer(
            "Thank you! Your last name has been saved.",
            reply_markup=types.ReplyKeyboardRemove(),
        )
    elif message.reply_to_message.text == "Please enter your phone number:":
        user.update_profile(message.from_user.id, phone_number=message.text)
        await message.answer(
            "Thank you! Your phone number has been saved.",
            reply_markup=types.ReplyKeyboardRemove(),
        )


@router.message(Command("test_categories"))

async def test_categories(message: types.Message):
    """TEST FUNCTION"""
    item_categories_manager = ItemCategory()
    item_categories_list = item_categories_manager.get_titles()
    item_categories_markup = generate_inline_markup(
        item_categories_list, row_width=2, button_type="category"
    )
    await message.answer(
        "Here is categories", reply_markup=item_categories_markup.as_markup()
    )



@router.callback_query(F.data.endswith("_cb_data"))
async def show_items_based_on_category(callback_query: types.CallbackQuery):
    """HANDLER FOR ITEMS & ITEM CATEGORY BUTTONS"""
    item_manager = Item()
    if callback_query.data.endswith("_cat_cb_data"):
        category_title = callback_query.data.split("_", 1)[0]

        item_titles_list = item_manager.get_items_titles_list_by_category_title(
            category_title=category_title
        )
        items_markup = generate_inline_markup(
            button_titles=item_titles_list, row_width=2, button_type="item"
        )

        await callback_query.message.answer(
            text=f"{callback_query.data.split('_', 1)[0]} category items",

            reply_markup=items_markup.as_markup(),
        )
        
    elif callback_query.data.endswith("_item_cb_data"):
        item_title = callback_query.data.split("_", 1)[0]
        item_details_dict = item_manager.get_item_details_dict_by_item_title(
            item_title=item_title
        )

        await callback_query.message.answer(
            text=f"""
ℹ️ Item Title: {item_details_dict.get("title")}

🆔 ID: {item_details_dict.get("id")}

💰 Price: {item_details_dict.get("price")}
""",
        )


async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
