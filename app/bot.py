import asyncio

from aiogram import Bot, Dispatcher

from app.config import BOT_TOKEN
from app.database import init_db
from app.handlers import router


async def main():
    await init_db()

    bot = Bot(token=BOT_TOKEN)

    dp = Dispatcher()
    dp.include_router(router)

    print("Football Lovers Bot is running...")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
