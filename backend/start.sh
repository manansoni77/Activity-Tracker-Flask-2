redis-server
celery -A main.client worker --loglevel=info 
celery -A main.client beat
gunicorn main:app