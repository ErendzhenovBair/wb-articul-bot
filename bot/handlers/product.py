from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

import aiohttp, aiogram, asyncio, logging
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime

from data import config, text
from repo.request import RequestRepository
from db.models import Request
from kb import kb

router = Router()

scheduler = AsyncIOScheduler()

class Product(StatesGroup):
    article_number = State()

@router.message(Command('start'))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)

@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu)

@router.callback_query(F.data == "button1")
async def get_article_number(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("Введите артикул товара:")
    await state.set_state(Product.article_number)

@router.message(Product.article_number)
async def handle_article_number(msg: Message, state: FSMContext):
    try:
        number = msg.text
        if not number.isdigit() or len(number) > 20:
            raise ValueError("Неверный формат артикула товара")
        await state.update_data(article_number=number)
        async with AsyncSession() as session:
            repository = RequestRepository(Request)
            await repository.create(user_id=msg.from_user.id, request_time=msg.date, product_article=number)
        data = await state.get_data()
        number = data['article_number']
        await parse_info(msg, number)
        await msg.answer(text.subscribe, reply_markup=kb.subscribe_menu)
    except ValueError:
        await msg.answer("Некорректный формат артикула. Пожалуйста, введите корректный артикул.")


async def parse_info(msg: Message, article_number: str):
    url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={article_number}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    product_info = data.get("data", {}).get("products", [])[0]
                    if product_info:
                        await send_product_info(msg, product_info)
                    else:
                        await msg.answer("Товар с таким артикулом не найден на Wildberries")
                else:
                    await msg.answer(f"Ошибка при получении данных: {response.status}")
    except Exception as e:
        await msg.answer(f"Ошибка: {str(e)}")

async def send_product_info(msg: Message, product_info):
    product_name = product_info.get("name")
    article_number = product_info.get("id")
    product_price = str(product_info.get("priceU", 0))[:-2]
    product_rating = product_info.get("rating")
    volume = product_info.get("volume")
    response_message = (
         f"Название товара: {product_name}\n"
         f"Артикул: {article_number}\n"
         f"Цена: {product_price}\n"
         f"Рейтинг товара: {product_rating}\n"
         f"Количество товара на всех складах: {volume}"
    )
    await msg.answer(text=response_message)

async def parse_info_wrapper(msg: Message, article_number: str):
    await parse_info(msg, article_number)

@router.callback_query(F.data == "subscribe")
async def subscribe_to_product(msg: Message, state: FSMContext):
    try:
        data = await state.get_data()
        article_number = data.get('article_number')

        if not article_number:
            raise ValueError("Article number not found in the state.")
        user_id = msg.from_user.id
        schedule_jobs()
        await msg.answer("Вы успешно подписаны на обновления по товару!")
    except ValueError as e:
        await msg.answer(f"Ошибка: {str(e)}")

def schedule_jobs():
    scheduler.add_job(parse_info_wrapper, "interval", seconds=5, args=(router,))
    
@router.callback_query(F.data == "button2")
async def stop_subscription(msg: Message, state: FSMContext):
    data = await state.get_data()
    background_task = data.get("background_task")
    if background_task:
        background_task.cancel()

@router.callback_query(F.data == "button3")
async def get_last_n_requests_handler(callback: types.CallbackQuery, state: FSMContext):
    try:
        async with AsyncSession() as session:
            repository = RequestRepository(Request)
            last_requests = await repository.get_last_n_requests(config.NUM)
        response = "\n".join(str(req) for req in last_requests)
        await callback.message.answer(f"Последние пять запросов в базу:\n{response}")
    except SQLAlchemyError as sql_error:
        logging.error(f"SQLAlchemy error: {sql_error}")
    except Exception as e:
        logging.error(f"Error fetching last 5 requests: {e}")