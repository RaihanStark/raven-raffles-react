## How to use it

### Run Flask Server 
set FLASK_APP=run.py
set FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000

### Run Celery Worker
celery worker -A celery_worker.celery --loglevel=info --pool=solo

### Run Celery Base
celery beat -A celery_worker.celery --loglevel=info

## Docker execution
> Start the app in Docker

```bash
$ sudo docker-compose pull && sudo docker-compose build && sudo docker-compose up -d
```

Visit `http://localhost:5000` in your browser. The app should be up & running.

<br />

