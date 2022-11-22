from aiogram.utils.callback_data import CallbackData


recognition_callback = CallbackData("get", "id")


def get_recognition_callback(id_: str):
    return recognition_callback.new(id_)
