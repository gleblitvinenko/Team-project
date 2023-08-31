from aiogram import types


def generate_inline_markup(
    button_titles: list, row_width: int
) -> types.InlineKeyboardMarkup:  # TODO pagination implementation
    markup = types.InlineKeyboardMarkup(row_width=row_width)
    row = []

    for button_title in button_titles:
        button = types.InlineKeyboardButton(
            f"{button_title}", callback_data=f"{button_title}_cb_data"
        )
        row.append(button)

        if len(row) == row_width:
            markup.row(*row)
            row.clear()

    if row:
        markup.row(*row)

    return markup
