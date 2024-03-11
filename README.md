# Telegram-бот wb-articul-bot

### Описание проекта: Telegram-бот для получения и отслеживания информации о товарах на маркетплейсе Wildberries 

wb-articul-bot - это Telegram-бот, разработанный в рамках тестового задания для вакансии Python Разработчика. Он разработан на основе библиотеки aiogram 3 и предоставляет пользователям удобный способ отслеживать информацию о товаре по его артикулу из карточки на маркетплейсе Wildberries. Бот предоставляет следующую информацию: артикул, цена, рейтинг товара, количество товара на всех складах.

Кроме того, пользователи могут подписаться на отслеживание информации о товаре по артикулу и получать данные из базы данных о последних n запросах.

### Функциональность:

- **Запрос информации о товаре**: Пользователи могутзапрашивать информацию о товаре, отправив в бот артикул товара из карточки товара на Wildberries.
- **Подписка на отслеживание товара**: Пользователи могут оформить подписку на отслеживание информации о товаре по артикулу.
- **Отмена подписки на отслеживание товара**: Пользователи могут отменить все подписки на отслеживание информации о товарах.
- **История запросов в базу данных**: Пользователи могут получить информацию из базы данных о последних n запросах. Это может быть полезно для отслеживания изменений цен или других параметров товара.

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
### Запуск проекта с использованием Docker

В корневой директорию апустите контейнеры при помощи команды
    ```bash
    docker-compose up -d # Для win
    sudo docker-compose up -d # Для linux
    ```

### Заполнение env

Для проекта wb-articul-bot секреты подключаются из файла .env. 
Создайте файл .env и заполните его своими данными. Перечень данных указан в корневой директории проекта в файле .env.example .env.
Проект доступен в телеграме по адресу @wildberries_articul_bot

### Ruff Линтер

Настройки линтера лежат в файле pyproject

Чтобы проверить все файлы в репозитории из корневой дириктории необходимо вызвать

```bash
ruff . / ruff check bot
```

Чтобы сразу исправить ошибки импортов необходимо вызвать

```bash
ruff . --fix
```

## Prehook commit

Настройки pre-commit лежат в файл .pre-commit-config
Чтобы применить pre-commit необходимо сделать следующее:

1. Вызвать команду инициализации

```bash
pre-commit init
```

2. Вызвать команду установки

```bash
pre-commit install
```
Теперь при попытке пуша коммита сперва сработает скрипты проверки описанные в .pre-commit-config, в данном случае пока только проверка на PEP8.

### Автор проекта

Автор этого проекта - Эрендженов Баир. 
Если у вас есть вопросы, предложения или просто поделитесь своим мнением о проекте, не стесняйтесь обращаться ко мне.
- Электронная почта: erendzhenovbair1990@yandex.ru
- Telegram: @BairErendzhenov
