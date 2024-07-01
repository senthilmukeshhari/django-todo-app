# Packages

django==4.2.0
fonaawesomefree==6.5.1
Pillow==10.1.0

# Commands

django-admin startproject django_todo_app

cd ./django_todo_app

py ./manage.py startapp todo_app

pip freeze > requirements.txt

py ./manage.py runserver

py ./manage.py makemigrations

py ./manage.py migrate

py ./manage.py createsuperuser
