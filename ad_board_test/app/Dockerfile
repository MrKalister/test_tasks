FROM python:3.10-slim
LABEL author='Novikov Maxim' version=1 email='maxon.nowik@yandex.ru'

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Update system
RUN apt-get update && \
  apt-get install -y -q libpq-dev python3-dev build-essential && \
  apt-get clean

# Install dependencies
RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
