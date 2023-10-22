import os
from flask import Flask
from flask_cors import CORS
from app.models import db, inspect
from app.cache import cache
from app.celery import make_celery
from app import worker

current_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, template_folder='./mail/templates')
app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + \
#     os.path.join(current_dir, DB_NAME)

CORS(app, resources={r'/*': {'origins': '*'}})
cache.init_app(app)
db.init_app(app)
app.app_context().push()

# create database
inspector = inspect(db.engine)
if not inspector.has_table('user'):
    db.create_all(app=app)
# if not os.path.exists(os.path.join(current_dir, DB_NAME)):
#     db.create_all(app=app)

# make_celery(app)
make_celery(worker, app)

from app.controllers import *

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        debug=True,
        port=5000
    )
