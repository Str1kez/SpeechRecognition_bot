import os


async def on_startup(dispatcher):
    from pathlib import Path

    import app.handlers
    import app.middlewares
    from app.loader import root_dir
    from app.utils import on_startup_notify, set_default_commands

    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)

    Path(os.path.join(root_dir, "files")).mkdir(exist_ok=True)


if __name__ == "__main__":
    from aiogram import executor

    from app.loader import dp

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
