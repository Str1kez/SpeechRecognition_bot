from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from app.loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = (
        "Отправь файл формата <b>.mp3</b> и получи текст",
        "Среднее время ожидания <b>Длительность / 5</b>",
        "Если я не успел распознать, можешь нажать на появившуюся кнопку повтора",
        "<b>Пожалуйста, не спамь её чаще чем раз в 10 секунд</b> 😔",
    )

    await message.answer("\n".join(text))
