FROM python:3.10-slim

COPY . /bot/

WORKDIR /bot

COPY requirements.txt .

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

CMD ["python", "bot/app.py"]