from flask_restful import fields

tracker_resource_fields = {
    'track_id': fields.Integer,
    'user_id': fields.Integer,
    'track_name': fields.String,
    'track_desc': fields.String,
    'track_type': fields.String,
    'options': fields.String,
}

log_resource_fields = {
    'log_id': fields.Integer,
    'track_id': fields.Integer,
    'time': fields.DateTime,
    'info': fields.String,
}

tracker_with_log_resource_fields = {
    'track_id': fields.Integer,
    'track_name': fields.String,
    'time': fields.DateTime,
    'last_log': fields.String,
}