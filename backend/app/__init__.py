from celery import Celery

def make_celery():
    return Celery(__name__, broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

client = make_celery()