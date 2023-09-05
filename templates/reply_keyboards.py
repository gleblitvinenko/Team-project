from aiogram import types

from templates import text_templates as tt


def contact_markup() -> types.ReplyKeyboardMarkup:
    kb_buttons_list = [
        [
            types.KeyboardButton(
                text=tt.share_phone_number_button, request_contact=True
            )
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=kb_buttons_list)

    return keyboard
