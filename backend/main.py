import os
from flask import Flask
from flask_cors import CORS
from app.models import db, DB_NAME
from app.cache import cache
from app.celery import make_celery
from app import client

current_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, template_folder='./mail/templates')
app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + \
    os.path.join(current_dir, DB_NAME)

CORS(app, resources={r'/*': {'origins': '*'}})
cache.init_app(app)
db.init_app(app)

if not os.path.exists(os.path.join(current_dir, DB_NAME)):
    db.create_all(app=app)
    print(db.create_all(app=app))


# make_celery(app)
app.app_context().push()
make_celery(client, app)

from app.controllers import *

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        debug=True,
        port=5000
    )
