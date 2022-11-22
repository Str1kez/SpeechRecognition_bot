import asyncio
import os
from uuid import uuid4

import aioboto3
import aiohttp
from aiogram.types import Message

from app.data.config import AWS_KEY_ID, AWS_SECRET_KEY, BUCKET_NAME, RECOGNITION_API_KEY, RECOGNITION_URL, STORAGE_URL
from app.keyboards.inline import retry_keyboard
from app.loader import bot


async def __get_data(path_to_file: str, message: Message, duration: int) -> str:
    session = aioboto3.Session()
    async with session.client(
        "s3",
        region_name="ru-central1",
        endpoint_url=STORAGE_URL,
        aws_access_key_id=AWS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_KEY,
    ) as s3:
        with open(path_to_file, "rb") as f:
            name = str(uuid4()) + ".mp3"
            await s3.upload_fileobj(f, BUCKET_NAME, name)

    await message.edit_text("Загрузил файл в облако")
    os.remove(path_to_file)

    header = {"Authorization": f"Api-Key {RECOGNITION_API_KEY}"}
    object_url = STORAGE_URL + "/" + BUCKET_NAME + "/" + name
    data = {
        "config": {
            "specification": {
                "languageCode": "ru-RU",
                "model": "general",
                "profanityFilter": False,
                "audioEncoding": "MP3",
            }
        },
        "audio": {"uri": object_url},
    }
    await message.edit_text("Отдал на распознавание")
    async with aiohttp.ClientSession() as session:
        async with session.post(url=RECOGNITION_URL, headers=header, json=data) as recognition_request:
            operation_id = (await recognition_request.json()).get("id")
    await message.edit_text(f"Ожидаем распознавания ~{duration // 5} сек")
    await asyncio.sleep(duration // 5)
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=f"https://operation.api.cloud.yandex.net/operations/{operation_id}", headers=header
        ) as recognition_response:
            response_data = await recognition_response.json()
    if response_data.get("done"):
        return " ".join(chunk["alternatives"][0]["text"] for chunk in response_data["response"]["chunks"])
    else:
        await message.edit_text(
            f"Распознавние еще не готово\n{operation_id=}", reply_markup=retry_keyboard(operation_id)
        )


async def partial_send_message(message: str, chat_id: int):
    while len(message) > 4090:
        await bot.send_message(chat_id, message[:4090])
        message = message[4090:]
    await bot.send_message(chat_id, message)


async def perform_recognition(path_to_file: str, message: Message, duration: int):
    data = await __get_data(path_to_file, message, duration)
    if data:
        await partial_send_message(data, message.chat.id)
