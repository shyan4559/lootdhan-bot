# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy all files into container
COPY . /app

# Install required package
RUN pip install python-telegram-bot==20.3

# Run the bot
CMD ["python", "main.py"]
