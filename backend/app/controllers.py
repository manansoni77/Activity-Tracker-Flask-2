from flask_restful import marshal
from flask import request, current_app as app, make_response, jsonify
from app.cache import cache
from datetime import datetime, timedelta
from app.models import Credentials, User, Trackers, Logs, db, token_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc
from app.extra import *
from app.resources import *
from app import worker
import jwt


@app.template_filter()
def format_time(time):
    return datetime.strftime(time, format)


@app.template_filter()
def format_time_code(time):
    return datetime.strftime(time, code_time)


@app.route('/ping', methods=['GET'])
def ping():
    worker.send_task('sendMonthlyReport')
    return jsonify({'msg': 'Pong!'})


@app.route('/login', methods=['POST'])
def login():
    cache.clear()
    data = request.get_json()
    email_id = data['email_id']
    password = data['password']
    if bool(login_re(email_id)) or bool(password_re(password)):
        return make_response(jsonify({"message": 'Please use only a-z A-Z 0-9 or $'}), 203)
    check_cred = Credentials.query.filter_by(email_id=email_id).first()
    if check_cred:
        if check_password_hash(check_cred.password, password):
            check_cred.last_login = datetime.utcnow()
            db.session.commit()
            token = jwt.encode({'user_id': check_cred.user_id, 'exp': datetime.utcnow()+timedelta(hours=1)},
                               app.config['SECRET_KEY'], 'HS256')
            token = token.decode('utf-8')
            return make_response(jsonify({"message": 'Logged In!', "token": token}), 201)
        else:
            return make_response(jsonify({"message": 'Wrong Password!'}), 203)
    else:
        return make_response(jsonify({"message": 'User Does Not Exist!'}), 203)

@app.route('/signup', methods=['POST'])
def signup():
    cache.clear()
    data = request.get_json()
    first_name = data['first_name']
    last_name = data['last_name']
    if not first_name.isalpha() or not last_name.isalpha():
        return make_response(jsonify({"message": 'Please use only alphabets for names!'}), 203)
    email_id = data['email_id']
    password = data['password']
    if bool(login_re(email_id)) or bool(password_re(password)):
        return make_response(jsonify({"message": 'Please use only a-z A-Z 0-9 or $'}), 203)
    check_cred = Credentials.query.filter_by(email_id=email_id).first()
    if check_cred:
        return make_response(jsonify({"message": 'User with that login already exists!'}), 203)
    else:
        new_user = User(first_name=first_name,
                        last_name=last_name)
        db.session.add(new_user)
        db.session.commit()
        new_cred = Credentials(email_id=email_id, password=generate_password_hash(
            password, method='sha256'), last_login=datetime.utcnow(), user_id=new_user.user_id)
        db.session.add(new_cred)
        db.session.commit()
        job = worker.send_task('sendWelcomeMail', (f'{first_name} {last_name}', email_id))
        return make_response(jsonify({"message": "Signed up successfully"}), 201)

@app.route("/dashboard", methods=["GET"])
@token_required
@cache.memoize()
def dashboard(user_id):
    added_trackers = Trackers.query.filter_by(user_id=user_id).all()
    tracks = []
    for tracker in added_trackers:
        last_log = Logs.query.filter_by(
            track_id=tracker.track_id).order_by(desc(Logs.time)).first()
        if last_log:
            tracks.append({
                'track_id': tracker.track_id,
                'track_name': tracker.track_name,
                'time': last_log.time,
                'last_log': last_log.info, })
        else:
            tracks.append({
                'track_id': tracker.track_id,
                'track_name': tracker.track_name,
                'time': None,
                'last_log': 'No Log', })
    tracks = [marshal(track, tracker_with_log_resource_fields)
              for track in tracks]
    return jsonify(tracks)



@app.route('/get_track/<int:track_id>', methods=['GET'])
@token_required
@cache.memoize()
def get_track(user_id, track_id):
    return make_response(marshal(Trackers.query.filter_by(track_id=track_id).first(), tracker_resource_fields), 201)

@app.route('/get_track_type/<int:track_id>', methods=['GET'])
@token_required
@cache.memoize()
def get_track_type(user_id, track_id):
    tracker = Trackers.query.filter_by(track_id=track_id).first()
    return make_response(jsonify({'track_type': tracker.track_type, 'options': tracker.options}), 201)

@app.route('/get_trackdata/<int:track_id>', methods=['GET'])
@token_required
@cache.memoize()
def get_trackdata(user_id, track_id):
    track = marshal(Trackers.query.filter_by(track_id=track_id).first(), tracker_resource_fields)
    track_logs = Logs.query.filter_by(track_id=track_id).all()
    track_logs = [marshal(log, log_resource_fields) for log in track_logs]
    return make_response(jsonify({'track': track, 'logs': track_logs}), 201)


@app.route('/delete_tracker/<int:track_id>', methods=['POST'])
@token_required
def delete_tracker(user_id, track_id):
    cache.clear()
    Trackers.query.filter_by(track_id=track_id).delete()
    Logs.query.filter_by(track_id=track_id).delete()
    db.session.commit()
    return '', 201

@app.route('/update_tracker', methods=['POST', 'PUT', 'DELETE'])
@token_required
def update_tracker(user_id):
    data = request.get_json()
    if text_re(data['track_name']) or text_re(data['track_desc']):
        return make_response(jsonify({'message':'Please use only alphabets or numbers in track name and description!'}), 203)
    if request.method == 'POST':
        if Trackers.query.filter_by(track_name=data['track_name'], user_id=user_id).first():
            return make_response(jsonify({'message':'This track name is already in your list of trackers!'}), 203)
    elif request.method == 'PUT':
        if Trackers.query.filter(Trackers.track_id!=data['track_id']).filter_by(track_name=data['track_name']).first():
            return make_response(jsonify({'message':'This track name is already in your list of trackers!'}), 203)
    if data['track_type']=='num':
        if data['options'] == "":
            return make_response(jsonify({'message': 'Please don\'t leave options empty!'}), 203)
        if bool(options_re(data['options'])):
            return make_response(jsonify({'message': 'Please use only alphabets, numbers, !, ?'}), 203)
    elif data['track_type']=='mcq':
        opt_list = data['options'].split(',')
        if opt_list[0] == "":
            return make_response(jsonify({'message': 'Please don\'t leave options empty!'}), 203)
        for item in opt_list:
            if bool(options_re(item)):
                return make_response(jsonify({'message': 'Please use only alphabets, numbers, !, ? and make sure they are seperated using only comma'}), 203)
    elif data['track_type']=='time':
        data['options'] = ''
    elif data['track_type']=='bool':
        opt_list = data['options'].split(',')
        if opt_list[0] == "":
            return make_response(jsonify({'message': 'Please don\'t leave options empty!'}), 203)
        if len(opt_list)!=2:
            return make_response(jsonify({'message': 'Please enter only 2 comma seperated options'}), 203)
        for item in opt_list:
            if bool(options_re(item)):
                return make_response(jsonify({'message': 'Please use only alphabets, numbers, !, ? and make sure they are seperated using only comma'}), 203)
    cache.clear()
    if request.method == 'POST':
        try:
            new_tracker = Trackers(
                user_id=user_id, track_name=data['track_name'], track_desc=data['track_desc'], track_type=data['track_type'], options=data['options'])
            db.session.add(new_tracker)
            db.session.commit()
        except Exception as e:
            return make_response(jsonify({'message': 'Incorrect information'}), 203)
    if request.method == 'PUT':
        tracker = Trackers.query.filter_by(track_id=data['track_id']).first()
        tracker.track_name = data['track_name']
        tracker.track_desc = data['track_desc']
        if tracker.track_type != data['track_type']:
            tracker.track_type = data['track_type']
            Logs.query.filter_by(track_id=data['track_id']).delete()
        tracker.options = data['options']
        db.session.commit()
    return '', 201

@app.route('/get_log/<int:log_id>', methods=['GET'])
@token_required
@cache.memoize()
def get_log(user_id, log_id):
    return make_response(marshal(Logs.query.filter_by(log_id=log_id).first(), log_resource_fields), 201)

@app.route('/delete_log/<int:log_id>', methods=['POST'])
@token_required
def delete_log(user_id, log_id):
    cache.clear()
    Logs.query.filter_by(log_id=log_id).delete()
    db.session.commit()
    return '', 201

@app.route('/update_log', methods=['POST','PUT'])
@token_required
def update_log(user_id):
    cache.clear()
    data = request.get_json()
    if data['track_type'] == 'time':
        start = datetime.strptime(data['log_time'], code_time)
        end = datetime.strptime(data['log_info'], code_time)
        if end <= start:
            return make_response(jsonify({'message': 'Time duration is negative or zero!'}), 203)
        elif (end-start).days:
            return make_response(jsonify({'message': 'Time duration is more than one day!'}), 203)
        info = str(end-start)
        time = datetime.strptime(data['log_time'], code_time)
    else:
        info = data['log_info']
        time = datetime.strptime(data['log_time'], code_time)
    if data['track_type'] == 'num':
        if not info.isnumeric():
            return make_response(jsonify({'message': 'Info entered is not numeric!'}), 203)
    if request.method == 'POST':
        new_log = Logs(track_id=data['track_id'], info=info, time=time)
        db.session.add(new_log)
        db.session.commit()
        return '', 201
    if request.method == 'PUT':
        log = Logs.query.filter_by(log_id=data['log_id']).first()
        log.info = info
        log.time = time
        db.session.commit()
        return '', 201

@app.route('/getcsv/<int:track_id>',methods=['GET'])
@token_required
def getcsv(user_id, track_id):
    if request.method == 'GET':
        worker.send_task('sendTrackerReport', (user_id, track_id))
    return '', 201