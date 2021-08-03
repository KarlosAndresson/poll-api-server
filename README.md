# Poll API server demo

### This server accepts REST API calls and manipulates objects (Polls, Questions, Options, Answers)

![alt text](db_diagram.jpg)

## Requirements:
- Python == 3.8
- Django == 2.2
- DRF == *
- psycopg2 <= 2.8
- Pipenv
- Postgres


## For server start:
1. Clone this project:
`git clone https://.....git`
2. Open created folder
3. Run `mkdir .venv`
4. Run `pipenv shell`
5. Run `pipenv update`
6. Make new secret key: 
`python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
or
`python3 -c 'import secrets; print(secrets.token_urlsafe())'`
7. Add following environment variables and change secret key: 
`export DJANGO_SETTINGS_MODULE=polls.settings;export F_SECRET_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx";export F_ALLOWED_HOSTS=localhost,127.0.0.1;export F_DEBUG=True;export F_DB_HOST=127.0.0.1;export F_DB_PORT=5432;export F_DB_NAME=test;export F_DB_USER=test;export F_DB_PASSWORD=test;`
8. Make migrations:
`python3 manage.py makemigrations`
9. Run migrations:
`python3 manage.py migrate`
10. Create superuser:
`python3 manage.py createsuperuser`
11. Start server with command:
`python3 manage.py runserver`
12. Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/)