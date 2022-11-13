from aiogram.types import File

from app.loader import bot, root_dir


async def save_file(file: File, path: str):
    await bot.download_file(file_path=file.file_path, destination=path)
