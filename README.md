# 📚 Plataforma de Orientação Vocacional

## 📖 Sobre o Projeto

A plataforma tem como objetivo apoiar os alunos na escolha do curso ideal, proporcionando um ambiente informativo, interativo e colaborativo. Através do quiz vocacional e do fórum de discussão, os usuários podem obter informações valiosas para tomar decisões assertivas sobre sua carreira.

## 🎯 Missão

Apoiar os alunos na escolha do curso ideal, assegurando que a plataforma ofereça um ambiente informativo, interativo e colaborativo. Avaliar se o quiz e o fórum cumprem sua função de orientar os usuários de forma eficaz, proporcionando informações valiosas e relevantes para suas decisões.

## 🚀 Visão

Analisar se a plataforma tem potencial para se tornar uma referência em orientação vocacional, se incentiva ativamente a troca de informações sobre cursos e se o sistema é escalável para atender um número crescente de alunos no futuro.

## 🛠 Tecnologias Utilizadas

- Python
- Django
- Django REST Framework
- MySQL

## 📌 Requisitos

Antes de iniciar o projeto, certifique-se de ter os seguintes requisitos instalados em sua máquina:

- Python 3.x
- MySQL
- Docker

## 📦 Instalação

1. Clone este repositório:

   ```bash
   git clone https://github.com/alyssonAndre/forum
   cd seu-repositorio
   ```

2Instale as dependências do projeto:

   ```bash
   pip install -r requirements.txt
   ```

## 🎲 Configuração do Banco de Dados

1. Crie um banco de dados no MySQL:

   ```sql
   CREATE DATABASE nome_do_banco;
   ```

2. Configure suas credenciais no arquivo `.env`:

   ```env
   DB_NAME=nome_do_banco
   DB_USER=seu_usuario
   DB_PASSWORD=sua_senha
   DB_HOST=localhost
   DB_PORT=3306
   ```

## 🚀 Executando o Projeto

1. Realize as migrações do banco de dados:

   ```bash
   python manage.py migrate
   ```

2. Crie um superusuário para acessar o painel administrativo:

   ```bash
   python manage.py createsuperuser
   ```

3. Inicie o servidor de desenvolvimento:

   ```bash
   python manage.py runserver
   ```

4. Acesse a plataforma pelo navegador em:

   ```
   http://127.0.0.1:8000/
   ```
