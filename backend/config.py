import os

SECRET_KEY = 'this is a secret key'

# CELERY_BROKER_URL = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_BROKER_URL = os.environ.get('REDIS_URI')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URI')

MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'manansoni.soni77@gmail.com'
MAIL_PASSWORD = 'Mananrox77'
