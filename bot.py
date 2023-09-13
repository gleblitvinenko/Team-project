import asyncio
import os

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from aiogram.filters import Command
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.fsm.storage.memory import MemoryStorage

from dotenv import load_dotenv

from managers.cart import Cart
from managers.item import Item
from managers.item_category import ItemCategory
from managers.user import User

from templates import text_templates as tt
from templates.inline_buttons import (
    generate_inline_markup,
    profile_settings_inline_markup,
    menu_inline_markup,
    generate_full_markup_by_rows_for_cart,
    create_item_info_buttons,
)
from templates.reply_keyboards import contact_markup

load_dotenv()

user, cart_manager, item_manager, item_categories_manager = (
    User(),
    Cart(),
    Item(),
    ItemCategory(),
)
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot=bot, storage=MemoryStorage())
router = Router()


class ItemStates(StatesGroup):
    pass


class ProfileStates(StatesGroup):
    choosing_first_name = State()
    choosing_last_name = State()
    choosing_phone_number = State()


async def check_get_phone_number(message: types.Message):
    phone_number = user.check_field(message.from_user.id, "phone_number")
    if not phone_number:
        await message.answer(
            "Please share your phone number with me.", reply_markup=contact_markup()
        )
    else:
        await message.answer(
            text="Here is your menu", reply_markup=menu_inline_markup().as_markup()
        )


@router.message(Command("start"))
async def start(message: types.Message):
    if not user.user_exists(message.from_user.id):
        user.create_user(message.from_user.id)
        await message.answer(
            text=f"Welcome to the shop, {message.from_user.first_name}!"
        )
    else:
        await message.answer(text=f"Welcome back, {message.from_user.first_name}!")
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
    await message.answer(
        text="Here is your menu", reply_markup=menu_inline_markup().as_markup()
    )


@router.callback_query(F.data == "profile_menu")
async def profile_inline_button(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        text=tt.show_profile_info(callback_query.from_user.id),
        reply_markup=profile_settings_inline_markup().as_markup(),
    )


@router.callback_query(F.data == "cart_menu")
async def show_cart(callback_query: types.CallbackQuery):
    """
    HANDLER THAT PROVIDES OPENING CART - 🛒 Cart
    """
    user_cart_data = cart_manager.get_items_and_quantities_from_cart_by_telegram_id(
        callback_query.from_user.id
    )
    user_cart_text = tt.get_cart_text(user_cart_data)
    await callback_query.message.edit_text(
        text=user_cart_text,
        reply_markup=generate_full_markup_by_rows_for_cart(user_cart_data).as_markup(),
    )


@router.callback_query(F.data.endswith("_delete_cart_item"))
async def delete_item_from_cart(callback_query: types.CallbackQuery):
    """
    HANDLER THAT PROVIDES DELETING ITEMS FROM CART
    """
    item_id, telegram_id = (
        int(callback_query.data.split("_")[0]),
        callback_query.from_user.id,
    )
    cart_manager.delete_item_from_cart(telegram_id=telegram_id, item_id=item_id)
    await show_cart(callback_query)


@router.callback_query(F.data.endswith("cart_item"))
async def increase_cart_item_quantity(callback_query: types.CallbackQuery):
    item_id, operation = (
        int(callback_query.data.split("_")[0]),
        callback_query.data.split("_")[1],
    )
    cart_manager.update_item_quantity(
        telegram_id=callback_query.from_user.id, item_id=item_id, operation=operation
    )
    await show_cart(callback_query)


@router.callback_query(F.data.endswith("_settings"))
async def profile_inline_nested_buttons(
    callback_query: types.CallbackQuery, state: FSMContext
):
    if callback_query.data.endswith("_first_name_settings"):
        await callback_query.message.edit_text(
            text="Please enter your first name:",
        )
        await state.set_state(ProfileStates.choosing_first_name)

    elif callback_query.data.endswith("_last_name_settings"):
        await callback_query.message.edit_text(
            text="Please enter your last name:",
        )
        await state.set_state(ProfileStates.choosing_last_name)

    elif callback_query.data.endswith("_phone_number_settings"):
        await callback_query.message.edit_text(
            text="Please enter your phone number:",
        )
        await state.set_state(ProfileStates.choosing_phone_number)


@router.message(ProfileStates.choosing_first_name)
async def handle_inputted_first_name(message: types.Message):
    user.update_profile(message.from_user.id, first_name=message.text.capitalize())
    await message.answer(
        "Thank you! Your first name has been successfully saved.",
    )
    await message.answer(
        text=tt.show_profile_info(message.from_user.id),
        reply_markup=profile_settings_inline_markup().as_markup(),
    )


@router.message(ProfileStates.choosing_last_name)
async def handle_inputted_last_name(message: types.Message):
    user.update_profile(message.from_user.id, last_name=message.text.capitalize())
    await message.answer(
        "Thank you! Your last name has been successfully saved.",
    )
    await message.answer(
        text=tt.show_profile_info(message.from_user.id),
        reply_markup=profile_settings_inline_markup().as_markup(),
    )


@router.message(ProfileStates.choosing_phone_number)
async def handle_inputted_phone_number(message: types.Message):
    user.update_profile(message.from_user.id, phone_number=message.text)
    await message.answer(
        "Thank you! Your phone number has been successfully saved.",
    )
    await message.answer(
        text=tt.show_profile_info(message.from_user.id),
        reply_markup=profile_settings_inline_markup().as_markup(),
    )


@router.callback_query(F.data == "item_categories_menu")
async def show_categories(
    callback_query: types.CallbackQuery, page: int = 1, new_message: bool = True
):
    """HANDLER MENU BUTTON - 🏷️ Item categories"""
    item_categories_list = item_categories_manager.get_titles()
    item_categories_markup = generate_inline_markup(
        item_categories_list, row_width=2, button_type="category", current_page=page
    )
    if new_message:
        await callback_query.message.edit_text(
            "Here is categories", reply_markup=item_categories_markup.as_markup()
        )
    else:
        await callback_query.message.edit_text(
            text="Here is categories",
            reply_markup=item_categories_markup.as_markup(),
        )


@router.callback_query(F.data.endswith("_cat_cb_data"))
async def show_items_based_on_category(
    callback_query: types.CallbackQuery,
    state: FSMContext,
    page: int = 1,
):
    """HANDLER ITEM CATEGORY BUTTONS"""
    category_title = callback_query.data.split("_", 1)[0]

    await state.update_data(category_title=category_title)

    item_titles_list = item_manager.get_items_titles_list_by_category_title(
        category_title=category_title
    )
    items_markup = generate_inline_markup(
        button_titles=item_titles_list,
        row_width=2,
        button_type="item",
        current_page=page,
    )
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=f"{category_title} category items",
        reply_markup=items_markup.as_markup(),
    )


@router.callback_query(F.data.endswith("_item_cb_data"))
async def show_item_details(callback_query: types.CallbackQuery):
    """HANDLER FOR ITEMS BUTTONS"""
    item_title = callback_query.data.split("_", 1)[0]
    item_details_dict = item_manager.get_item_details_dict_by_item_title(
        item_title=item_title
    )

    item_id = item_details_dict.get("id")
    await callback_query.message.edit_text(
        text=tt.item_detail_info(**item_details_dict),
        reply_markup=create_item_info_buttons(item_id=item_id),
    )


@router.callback_query(F.data.endswith("_add_item_to_cart"))
async def add_item_to_cart(callback_query: types.CallbackQuery):
    item_id, item_quantity, telegram_id = (
        int(callback_query.data.split("_")[0]),
        1,
        callback_query.from_user.id,
    )
    cart_manager.add_item_and_quantity_to_user_cart(
        item_id=item_id, item_quantity=item_quantity, telegram_id=telegram_id
    )


async def click_item_pagination(
    callback_query: types.CallbackQuery, state: FSMContext, page: int
):
    state_dict = await state.get_data()
    category_title = state_dict.get("category_title")
    item_titles_list = item_manager.get_items_titles_list_by_category_title(
        category_title=category_title
    )
    items_markup = generate_inline_markup(
        button_titles=item_titles_list,
        row_width=2,
        button_type="item",
        current_page=page,
    )
    await callback_query.message.edit_text(
        text=f"{category_title} category items",
        reply_markup=items_markup.as_markup(),
    )


@router.callback_query(F.data.endswith("_pagination"))
async def interact_with_pagination_buttons(
    callback_query: types.CallbackQuery, state: FSMContext
):
    data_parts = callback_query.data.split("_")
    current_page = int(data_parts[0])
    action = data_parts[2]

    if action == "previous" and "cat" in callback_query.data:
        await show_categories(
            callback_query=callback_query, page=current_page, new_message=False
        )
    elif action == "next" and "cat" in callback_query.data:
        await show_categories(
            callback_query=callback_query, page=current_page, new_message=False
        )
    elif action == "previous" and "item" in callback_query.data:
        await click_item_pagination(callback_query, page=current_page, state=state)
    elif action == "next" and "item" in callback_query.data:
        await click_item_pagination(callback_query, page=current_page, state=state)


async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
