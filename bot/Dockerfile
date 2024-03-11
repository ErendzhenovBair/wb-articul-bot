FROM python:3.10-slim

WORKDIR /bot

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

CMD ["python", "app.py"]