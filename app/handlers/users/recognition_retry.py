import aiohttp
from aiogram.types import CallbackQuery

from app.data.config import RECOGNITION_API_KEY
from app.keyboards.inline import recognition_callback
from app.loader import dp
from app.utils.misc import rate_limit
from app.utils.recognition import partial_send_message


@rate_limit(10)
@dp.callback_query_handler(recognition_callback.filter())
async def recognition_retry(call: CallbackQuery, callback_data: dict):
    operation_id = callback_data.get("id")
    header = {"Authorization": f"Api-Key {RECOGNITION_API_KEY}"}
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=f"https://operation.api.cloud.yandex.net/operations/{operation_id}", headers=header
        ) as recognition_response:
            response_data = await recognition_response.json()
    if response_data.get("done"):
        await call.message.delete()
        await partial_send_message(
            " ".join(chunk["alternatives"][0]["text"] for chunk in response_data["response"]["chunks"]),
            call.message.chat.id,
        )
    await call.answer()
