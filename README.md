Generate requirements.txt for Django ERP project.

poetry export -f requirements.txt --without-hashes > requirements.txt

poetry run django-admin startproject config .

poetry run python manage.py runserver

poetry run python manage.py startapp <appName>