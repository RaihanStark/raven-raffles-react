# Raven Raffles

![Raven Raffles 2.0 Introduction](https://pbs.twimg.com/media/ES5lQj4X0AEU6LJ?format=jpg&name=large)

## Technology:

- Python
- Javascript
- React
- Flask
- SQLAlchemy
- and others..

## Directory

| Name          | Directory             |
| ------------- | --------------------- |
| React Server  | /                     |
| Python Server | /api/run.py           |
| Celery Server | /api/celery_worker.py |

## Deployment

| Server        | Port |
| ------------- | ---- |
| React Server  | 8080 |
| Python Server | 3000 |
| Celery Server | 6379 |

## How to Use

### Run Flask Server

flask run --host=0.0.0.0 --port=5000

### Run Celery Worker

celery worker -A celery_worker.celery --loglevel=info --pool=solo

### Run Celery Base

celery beat -A celery_worker.celery --loglevel=info
