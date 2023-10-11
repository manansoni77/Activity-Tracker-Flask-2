from celery import Celery


def make_celery():
    # return Celery(__name__, broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
    return Celery(__name__, broker='redis://red-ckjd28a12bvs739tgvg0:6379', backend='redis://red-ckjd28a12bvs739tgvg0:6379')


client = make_celery()
