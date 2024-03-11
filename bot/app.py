import asyncio
import logging

import aioschedule
from aiogram import Bot, Dispatcher

from data import config
from db.engine import init_db
from handlers import product

bot =  Bot(token=config.BOT_TOKEN)

async def scheduler():
    aioschedule.every(5).minutes.do(product.check_and_send_info)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    dp = Dispatcher(bot=bot)
    dp.include_routers(product.router)
    asyncio.create_task(scheduler())
    try:
        await init_db()
    except ConnectionRefusedError:
        logging.error("Failed to connect to db")
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())