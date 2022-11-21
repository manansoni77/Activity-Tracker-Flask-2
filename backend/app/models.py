from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask import request, current_app as app, make_response, jsonify
from functools import wraps
import jwt

db = SQLAlchemy()
DB_NAME = 'database.sqlite3'


class Credentials(db.Model):
    __tablename__ = 'credentials'
    email_id = db.Column(db.String, primary_key=True,
                         nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id"), nullable=False, unique=True)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True,
                        nullable=False, unique=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)


class Trackers(db.Model):
    __tablename__ = 'trackers'
    track_id = db.Column(db.Integer, primary_key=True,
                         nullable=False, unique=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id"), nullable=False)
    track_name = db.Column(db.String, nullable=False)
    track_desc = db.Column(db.String, nullable=False)
    track_type = db.Column(db.String, db.CheckConstraint(
        "track_type in ('num','mcq','time','bool')"), nullable=False)
    options = db.Column(db.String, nullable=False)


class Logs(db.Model):
    __tablename__ = 'logs'
    log_id = db.Column(db.Integer, nullable=False, primary_key=True)
    track_id = db.Column(db.Integer, db.ForeignKey(
        "trackers.track_id"), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    info = db.Column(db.String, nullable=False)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return make_response(jsonify({"message": "A valid token is missing!"}), 401)
        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except Exception as e:
            return make_response(jsonify({"message": "Invalid token!"}), 401)
        return f(data['user_id'], *args, **kwargs)
    return decorator
