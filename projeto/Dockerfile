FROM python:3.11

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y netcat-openbsd

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000

CMD ["sh", "-c", "echo 'Aguardando MySQL iniciar...'; while ! nc -z db 3306; do sleep 0.1; done; echo 'Executando migrações...'; python manage.py makemigrations --noinput; python manage.py migrate --noinput; echo 'Django está rodando em http://0.0.0.0:8000/'; python manage.py runserver 0.0.0.0:8000"]
