import math

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from templates import text_templates as tt


def generate_inline_markup(
    button_titles: list,
    row_width: int,
    button_type: str,
    elements_on_page: int = 2,
    current_page: int = 1,
) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    row = []

    pagination_row = [
        types.InlineKeyboardButton(
            text="⬅️",
            callback_data=f"{current_page - 1 if current_page != 1 else current_page}_{'cat' if button_type == 'category' else 'item'}_previous_page_pagination",
        ),
        types.InlineKeyboardButton(
            text=f"{current_page}/{math.ceil(len(button_titles) / elements_on_page)}",
            callback_data="current_page",
        ),
        types.InlineKeyboardButton(
            text="➡️",
            callback_data=f"{current_page + 1 if current_page < math.ceil(len(button_titles) / elements_on_page) else current_page}_{'cat' if button_type == 'category' else 'item'}_next_page_pagination",
        ),
    ]

    start_index = (current_page - 1) * elements_on_page
    end_index = min(start_index + elements_on_page, len(button_titles))

    for button_title in button_titles[start_index:end_index]:
        button = types.InlineKeyboardButton(
            text=f"{button_title}",
            callback_data=f"{button_title}_cat_cb_data"
            if button_type == "category"
            else f"{button_title}_item_cb_data",
        )
        row.append(button)

        if len(row) == row_width:
            builder.row(*row)
            row.clear()

    if row:
        builder.row(*row)

    builder.row(*pagination_row)

    return builder


def profile_settings_inline_markup() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    profile_settings_buttons = [
        types.InlineKeyboardButton(
            text=tt.add_change_first_name_inline,
            callback_data="add_change_first_name_settings",
        ),
        types.InlineKeyboardButton(
            text=tt.add_change_last_name_inline,
            callback_data="add_change_last_name_settings",
        ),
        types.InlineKeyboardButton(
            text=tt.add_change_phone_number_inline,
            callback_data="add_change_phone_number_settings",
        ),
    ]

    first_row_buttons = profile_settings_buttons[:2]
    second_row_buttons = profile_settings_buttons[2:]

    builder.row(*first_row_buttons)
    builder.row(*second_row_buttons)
    return builder


def menu_inline_markup(row_width: int = 2) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    row = []
    for key, value in tt.menu_names_dict.items():
        button = types.InlineKeyboardButton(text=value, callback_data=f"{key}_menu")
        row.append(button)

        if len(row) == row_width:
            builder.row(*row)
            row.clear()

    if row:
        builder.row(*row)

    return builder


def generate_buttons_for_cart_item(item: dict) -> list[types.InlineKeyboardButton]:
    item_id, item_title = item.get("item_id"), item.get("title")

    row = [
        types.InlineKeyboardButton(
            text=f"📌 {item_title}",
            callback_data=f"{item_id}_cart_item_object"
        ),
        types.InlineKeyboardButton(
            text="➕",
            callback_data=f"{item_id}_increment_cart_item"
        ),

        types.InlineKeyboardButton(
            text="➖",
            callback_data=f"{item_id}_decrement_cart_item"
        ),

        types.InlineKeyboardButton(
            text="⛔ Delete",
            callback_data=f"{item_id}_delete_cart_item"
        )
    ]

    return row


def generate_full_markup_by_rows_for_cart(item_dicts_list: list[dict]) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    for item_dict in item_dicts_list:
        builder.row(generate_buttons_for_cart_item(item_dict)[0])
        builder.row(*(generate_buttons_for_cart_item(item_dict)[1:]))

    return builder


