FROM python:3.10

WORKDIR /app
COPY . /app

RUN pip install python-telegram-bot==20.3

ENV RENDER=true  # This tells Render to not look for a web port

CMD ["python", "main.py"]
