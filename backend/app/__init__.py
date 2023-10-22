import os
import ssl
from celery import Celery


def make_celery():
    # return Celery(__name__, broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
    return Celery(__name__, broker=os.environ.get('REDIS_URI'), backend=os.environ.get('REDIS_URI'),
    broker_use_ssl = {
        'ssl_cert_reqs': ssl.CERT_NONE
     },
    redis_backend_use_ssl = {
        'ssl_cert_reqs': ssl.CERT_NONE
     },)


worker = make_celery()
