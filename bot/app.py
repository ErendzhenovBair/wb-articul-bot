import asyncio
import logging

from aiogram import Bot, Dispatcher
from sqlalchemy.engine import URL 

from data import config
from db.engine import init_db
from handlers import product


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    bot =  Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_routers(product.router)
    await bot.delete_webhook(drop_pending_updates=True)
    product.scheduler.start()
    try:
        await init_db()
    except ConnectionRefusedError:
        logging.error("Failed to connect to db")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())