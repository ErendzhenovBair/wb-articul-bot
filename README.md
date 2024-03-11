# Телеграм-бот - wb-articul-bot

### Описание проекта: Телеграм-бот для получения и отслеживания информации о товарах на маркетплейсе Wildberries 

Телеграм бот wb-articul-bot, сделанный в качестве тестового задания на вакансию Python Разработчика. Этот бот разработан на базе библиотеки aiogram 3 и предоставляет пользователям удобный способ отслеживать информацию об товаре по артикулу, в том числе артикул, цена, рейтинг товара, количество товара на всех складах.
Кроме того, возможно оформить подписку на отслеживание информации о товаре по артикулу и получить информацию из базы данных о последних n запросах в базу данных.

### Функциональность:

- Запрос информации о товаре: Пользователи могут выбирать торговые пары из предоставленного списка. Предусмотрена возможность изменять и добавлять избранные торговые пары.
- Ввод количества токенов: Бот предлагает ввести количество токенов, которое вы хотели бы отслеживать.
- Получение общей стоимости: Бот рассчитывает общую стоимость указанного количества токенов на основе текущей цены каждого токена в паре. Информация запрашивается с биржи Бинанс на текущий момент.
- Отображение результатов: Результаты подсчетов предоставляются в виде ответного сообщения с указанием общей стоимости токенов в USDT (долларах США).

### Технологии

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![aiogram](https://img.shields.io/badge/-aiogram-464646?style=flat-square&logo=telegram)](https://github.com/aiogram/aiogram)
[![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-464646?style=flat-square&logo=sqlalchemy)](https://www.sqlalchemy.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=postgresql)](https://www.postgresql.org/)
[![aioschedule](https://img.shields.io/badge/-aioschedule-464646?style=flat-square&logo=python)](https://github.com/ChadSikorra/aioschedule)
[![aioschedule](https://img.shields.io/badge/-aioschedule-464646?style=flat-square&logo=python)](https://github.com/ChadSikorra/aioschedule)

- Python 3.10.12
- aiogram 3.4.1
- SQLAlchemy 2.0.28
- PostgreSQL 14.11
- aiohttp 3.9.3
- aioschedule 0.5.2

### Запуск проекта локально 

Клонируем себе репозиторий:

```bash
git clone [https://github.com/ErendzhenovBair/.git](https://github.com/ErendzhenovBair/wb-articul-bot.git)
```
Cоздаем и активируем виртуальное окружение:
Команда для установки виртуального окружения на Mac или Linux:

```bash
   python3 -m venv venv
   source venv/bin/activate
```

Команда для Windows:

```bash
   python -m venv venv
   source venv/Scripts/activate
```

Устанавливаем зависимости из файла requirements.txt:

```bash
   pip install -r requirements.txt
```

- Запустить проет:

```bash
   python app.py
```

- Выбор торговой пары осуществляется в ответ на команду /start в боте

- Количество токенов для расчета возможно представить в виде целого или дробного числа.

### Заполнение env

Для проекта wb-articul-bot секреты подключаются из файла .env. 
Создайте файл .env и заполните его своими данными. Перечень данных указан в корневой директории проекта в файле .env.example .env.
Проект доступен в телеграме по адресу @wildberries_articul_bot

### Ruff Линтер

Настройки линтера лежат в файле pyproject

Чтобы проверить все файлы в репозитории из корневой дириктории необходимо вызвать

```bash
ruff .
```

Чтобы сразу исправить ошибки импортов необходимо вызвать

```bash
ruff . --fix
```

### Автор проекта

Автор этого проекта - Эрендженов Баир. 
Если у вас есть вопросы, предложения или просто поделитесь своим мнением о проекте, не стесняйтесь обращаться ко мне.
- Электронная почта: erendzhenovbair1990@yandex.ru
- Telegram: @BairErendzhenov
