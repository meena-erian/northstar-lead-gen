# Northstar Lead Generation

A Django lead-generation application with SQLite persistence, served by Gunicorn on port 8000.

[![Deploy with Portacode](https://img.shields.io/badge/Deploy%20with-Portacode-635BFF?style=for-the-badge)](https://portacode.com/dashboard/?portafile=https%3A%2F%2Fraw.githubusercontent.com%2Fmeena-erian%2Fnorthstar-lead-gen%2Fmain%2Fportafile.yaml)

The deploy button opens Portacode and loads the repository's `portafile.yaml`. You will be asked to sign in if needed and provide the required deployment inputs.

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

The Portacode deployment recipe is in [`portafile.yaml`](portafile.yaml).
