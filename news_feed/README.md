
# My news feed
This simple app [news feed](https://gotoitfox.sytes.net/redoc/) is used to create news posts. You can like your favorite post or write comment.

## Technologies.
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://www.postgresql.org/)
[![Djoser](https://img.shields.io/badge/-Djoser-464646?style=flat&logo=Djoser&logoColor=56C0C0&color=008080)](https://github.com/sunscrapers/djoser)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=56C0C0&color=008080)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=56C0C0&color=008080)](https://gunicorn.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://hub.docker.com/)
[![AWS](https://img.shields.io/badge/-AWS-464646?style=flat&logo=amazonaws&logoColor=56C0C0&color=008080)](https://aws.amazon.com/?nc1=h_ls)

##### The full list of modules used in the project is available in [backend/requirements.txt](https://github.com/MrKalister/foodgram-project-react/blob/master/backend/requirements.txt)

## What can users do?
##### User access levels:
* Guest (unauthorized user)
* Authorized user
* Administrator

##### What unauthorized users can do:
* Create an account.
* View posts.
* View comments from a post.

##### What authorized users can do:
The authorized user has all the rights of an admin.
Also, he can:
* Get a token using your own username and password.
* Create/edit/delete your own posts
* Create/delete your own comments
* Add/delete like to some posts
* Delete comments to his posts.

##### Any actions are available to the administrator except put/patch, because it's not provided by the task.

##### More information is available in the API documentation at:
https://gotoitfox.sytes.net/redoc/ or https://gotoitfox.sytes.net/swagger/

The documentation is available at a similar address in the local development environment.

## Installing and running the project on a local machine.
You must have installed and run Docker. More information in [Instructions](https://docs.docker.com/).
#### 1. Clone a repository.
* Option 1. Use SSH:
```bash
git clone git@github.com:MrKalister/My_news_feed.git
```
* Option 2. Use HTTPS:
```bash
git clone https://github.com/MrKalister/My_news_feed.git
```
```bash
cd My_news_feed 
```
#### 2. Create and activate a virtual environment.
Command to install a virtual environment on Mac or Linux:
```bash
python3 -m venv venv && source env/bin/activate
```
Command for Windows:
```bash
python -m venv venv && . venv/Scripts/activate
```
#### 3. Go to the infra directory.
```bash
cd infra
```
#### 4. Create ".env" file and fill in the sample:
* DEBUG=False
* USE_SQLLITE=True # If you use local server and sqllite
* SECRET_KEY=12345 # secret key for Django project
* ALLOWED_HOSTS=localhost,127.0.0.1,backend
* TRUSTED=http://localhost,http://127.0.0.1 # don't forgot add your server ip/domain
* DB_ENGINE=django.db.backends.postgresql # database backend
* DB_NAME=postgres # name database
* POSTGRES_USER=postgres # login for connect to database
* POSTGRES_PASSWORD=12345 # password for connect to database
* DB_HOST=db # name container with database
* DB_PORT=5432 # login for connect to database

#### 5. Run docker-compose.
```bash
docker-compose up -d
```
#### 6. Open bash terminal in container backend.
```bash
docker-compose exec backend bash
```
#### 7. Сreate and apply migrations.
```bash
python manage.py makemigrations && python manage.py migrate
```
#### 8. Create admin.
```bash
python manage.py createsuperuser
```

## Installing and running the project on a remote server.
#### 1. Log in to a remote server:
```bash
ssh <username>@<ip_address>
```
#### 2. Install Docker and Docker-compose.
```bash
sudo apt install docker.io
sudo apt-get update
sudo apt-get install docker-compose-plugin
sudo apt install docker-compose
```
#### 3. Create ".env" file and fill in the sample:
* DEBUG=False
* USE_SQLLITE=True # If you use local server and sqllite
* SECRET_KEY=12345 # secret key for Django project
* ALLOWED_HOSTS=localhost,127.0.0.1,backend
* TRUSTED=http://localhost,http://127.0.0.1 # don't forgot add your server ip/domain
* DB_ENGINE=django.db.backends.postgresql # database backend
* DB_NAME=postgres # name database
* POSTGRES_USER=postgres # login for connect to database
* POSTGRES_PASSWORD=12345 # password for connect to database
* DB_HOST=db # name container with database
* DB_PORT=5432 # login for connect to database
#### 4. Сopy files from a folder to a remote server.
```bash
scp . -r <username>@<host>:/home/<username>/
```
#### The next steps(5-8) are similar to the installation "Installing and running the project on a local computer"

### Author

**Novikov Maxim** - [github](http://github.com/MrKalister)

*If you notice any inaccuracies, please email me - maxon.nowik@yandex.ru*
