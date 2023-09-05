import math

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


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
  