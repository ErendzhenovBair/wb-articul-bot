FROM python:3.10-slim

COPY requirements.txt .

COPY . /bot/

WORKDIR /bot

RUN pip install -r requirements.txt

ENTRYPOINT python app.py