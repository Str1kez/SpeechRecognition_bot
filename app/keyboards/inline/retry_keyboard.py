from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .callbacks import get_recognition_callback


def retry_keyboard(id_: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Проверить готовность", callback_data=get_recognition_callback(id_))],
        ]
    )
