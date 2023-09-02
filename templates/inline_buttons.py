from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def generate_inline_markup(
    button_titles: list, row_width: int, button_type: str
) -> InlineKeyboardBuilder:  # TODO pagination implementation
    builder = InlineKeyboardBuilder()
    row = []

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

    return builder


profile_inline = "📁 Profile"
item_categories_inline = "🗄️ Item categories"
faq_inline = "❓ FAQ"
add_change_first_name_inline = "✏️ Add/Change first name"
add_change_last_name_inline = "✏️ Add/Change last name"
add_change_phone_number_inline = "✏️ Add/Change phone number"
share_phone_number_inline = "Share phone number 📱"
