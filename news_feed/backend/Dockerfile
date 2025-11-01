FROM python:3.9-slim
LABEL author='Novikov Maxim' version=1 email='maxon.nowik@yandex.ru'

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

RUN python manage.py collectstatic --no-input

CMD ["gunicorn", "config.wsgi:application", "--bind", "0:8000" ] 