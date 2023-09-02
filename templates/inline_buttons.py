import math

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def generate_inline_markup(
    button_titles: list,
    row_width: int,
    button_type: str,
    elements_on_page: int = 2,
    current_page: int = 1,
) -> InlineKeyboardBuilder:  # TODO pagination implementation
    builder = InlineKeyboardBuilder()
    row = []

    pagination_row = [
        types.InlineKeyboardButton(text="⬅️", callback_data="previous_page"),
        types.InlineKeyboardButton(
            text=f"{current_page}/{math.ceil(len(button_titles) / elements_on_page)}",
            callback_data="current_page",
        ),
        types.InlineKeyboardButton(text="➡️", callback_data="next_page"),
    ]

    for button_title in button_titles:
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


profile_inline = "📁 Profile"
item_categories_inline = "🗄️ Item categories"
faq_inline = "❓ FAQ"
add_change_first_name_inline = "✏️ Add/Change first name"
add_change_last_name_inline = "✏️ Add/Change last name"
add_change_phone_number_inline = "✏️ Add/Change phone number"
share_phone_number_inline = "Share phone number 📱"
