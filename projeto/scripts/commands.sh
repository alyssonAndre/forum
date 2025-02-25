#!/bin/sh

clear

echo "Aguardando MySQL iniciar..."
while ! nc -z db 3306; do
  sleep 0.1
done

echo "Executando migrações..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput


echo "Django está rodando em http://127.0.0.1:8000"
python manage.py runserver 0.0.0.0:8000
