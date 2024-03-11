from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

menu = [
    [InlineKeyboardButton(
        text='🔎 Получить информацию по товару',
        callback_data="button1"
    )],
    [InlineKeyboardButton(
        text='🚫 Остановить уведомления',
        callback_data="button2"
    )],
    [InlineKeyboardButton(
        text='💽 Получить информацию из БД',
        callback_data="button3"
    )]
]
    
menu = InlineKeyboardMarkup(inline_keyboard=menu)

exit_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]],
    resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="◀️ Выйти в меню",
                callback_data="menu"
            )
        ]
    ]
)

subscribe_menu = [[InlineKeyboardButton(
    text='Подписаться', callback_data="subscribe")]]
subscribe_menu = InlineKeyboardMarkup(inline_keyboard=subscribe_menu)
