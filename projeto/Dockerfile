FROM python:3.11

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y netcat-openbsd

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000

CMD ["sh", "scripts/commands.sh"]
