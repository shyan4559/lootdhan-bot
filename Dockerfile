FROM python:3.10

WORKDIR /app
COPY . /app

RUN pip install python-telegram-bot==20.3

# Tell Render to not expect an open port
ENV RENDER=true

CMD ["python", "main.py"]
