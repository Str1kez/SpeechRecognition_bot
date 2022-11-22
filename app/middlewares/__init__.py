from .throttling import ThrottlingMiddleware
from app.loader import dp


if __name__ == "app.middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
