import logging

import aiohttp
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from app import bot
from sqlalchemy.exc import SQLAlchemyError

from data import config, text
from db.models import Request
from kb import kb
from repo.request import RequestRepository

router = Router()

class Product(StatesGroup):
    article_number = State()
    waiting_for_subscribe = State()

@router.message(Command('start'))
async def start_handler(msg: Message):
    await msg.answer(
        text.greet.format(name=msg.from_user.full_name),
        reply_markup=kb.menu
    )

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
        repository = RequestRepository(Request)
        await repository.create(
            user_id=msg.from_user.id,
            request_time=msg.date,
            product_article=number,
            subscribed=False
        )
        await parse_info(msg, number)
        await state.set_state(Product.waiting_for_subscribe)
        await msg.answer(text.subscribe, reply_markup=kb.subscribe_menu)
    except ValueError:
        await msg.answer(
            "Некорректный формат артикула. Введите корректный артикул."
        )

async def parse_info(msg: Message, article_number: str):
    url = f"{config.URL}={article_number}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    product_info = data.get("data", {}).get("products", [])[0]
                    if product_info:
                        await send_product_info(msg, product_info)
                    else:
                        await msg.answer(
                            "Товар с таким артикулом не найден на WB"
                        )
    except Exception:
        await msg.answer(
            text="Произошла непредвиденная ошибка. Попробуйте еще раз."
        )

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

@router.callback_query(F.data == "subscribe")
async def subscribe_to_product(
    callback: types.CallbackQuery,
    state: FSMContext
):
    try:
        data = await state.get_data()
        article_number = data.get('article_number')
        user_id = callback.from_user.id
        requests_to_update = await RequestRepository(
            Request).get_requests_by_user_article(
                user_id, str(article_number))
        for request in requests_to_update:
            if not request.subscribed:
                await RequestRepository(
                    Request).update(request, subscribed=True)
                await callback.answer(
                    "Вы успешно подписаны на обновления по товару!"
                )
            else:
                await callback.answer(
                    "Подписка на данный артикул оформлена"
                )
    except ValueError as e:
        await callback.answer(f"Ошибка: {str(e)}")

    
@router.callback_query(F.data == "button2")
async def stop_subscription(callback: types.CallbackQuery,
):
    try:
        user_id = callback.from_user.id
        repository = RequestRepository(Request)
        requests_to_update  = await RequestRepository(
            Request).get_requests_by_user_id(user_id)
        if requests_to_update:
            for req in requests_to_update:
                await repository.update(req, subscribed=False)
                await callback.answer("Вы успешно отменили свои подписки")
        else:
            await callback.answer("У вас нет действующих подписок")
    except ValueError as e:
        await callback.answer(f"Ошибка: {str(e)}")

@router.callback_query(F.data == "button3")
async def get_last_n_requests_handler(
    callback: types.CallbackQuery,
    state: FSMContext
):
    try:
        repository = RequestRepository(Request)
        last_requests = await repository.get_last_n_requests(
            config.NUM)
        response = "\n".join(str(req) for req in last_requests)
        await callback.message.answer(
            f"Последние пять запросов в базу:\n{response}"
        )
    except SQLAlchemyError as sql_error:
        logging.error(f"SQLAlchemy ошибка: {sql_error}")
    except Exception as e:
        logging.error(f"Последние 5 запросов в БД отсутствуют: {e}")

async def check_and_send_info():
    """Schedule function"""
    repository = RequestRepository(Request)
    unique_user_articles = await repository.get_subscribed_article_numbers()
    for row in unique_user_articles:
        user_id, product_article = row
        try:
            response_message = await get_product_info(product_article)
            await bot.send_message(
                user_id, response_message
            )
        except Exception:
            logging.error(
                "Произошла непредвиденная ошибка. Попробуйте еще раз."
            )

async def get_product_info(product_article):
    url = f"{config.URL}={product_article}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                product_info = data.get("data", {}).get("products", [])[0]
                if product_info:
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
                    return response_message
    return "Информация о товаре недоступна или произошла ошибка."