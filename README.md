# Northstar Lead Generation

A Django lead-generation application with SQLite persistence, served by Gunicorn on port 8000.

## Configuration

Set these environment variables before running:

- `DJANGO_SECRET_KEY`: a private Django secret key.
- `DJANGO_DEBUG`: `True` for local development or `False` in deployment.

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver 8000
```

Run tests and system checks with `python manage.py test` and `python manage.py check`.

## Deployment

Run migrations and static collection, then start Gunicorn on port 8000:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn northstar.wsgi:application --bind 0.0.0.0:8000
```
