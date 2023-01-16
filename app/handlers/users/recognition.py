import os

from aiogram.types import ContentTypes, Message
from app.data.config import ADMINS

from app.loader import dp, root_dir
from app.utils.file import save_file
from app.utils.recognition import perform_recognition


@dp.message_handler(content_types=ContentTypes.DOCUMENT)
async def error_in_extension(message: Message):
    await message.answer("Пришли mp3 пожалуйста")


@dp.message_handler(content_types=ContentTypes.AUDIO)
async def receive_audio(message: Message):
    if message.from_user.id not in ADMINS:
        await message.answer("Распознавание недоступно для тебя")
        # ADMINS.add(321259733)
        return
    if message.audio.file_name[-4:] != ".mp3":
        await message.answer("Пришли mp3 пожалуйста")
        return
    audio_file = await message.audio.get_file()
    path_to_file_locale = os.path.join(root_dir, "files", audio_file.file_id)
    await save_file(audio_file, path_to_file_locale)
    answer = await message.answer(f"Сохранил твой файл\nНачинаю распознавание")
    await perform_recognition(path_to_file_locale, answer, message.audio.duration)
