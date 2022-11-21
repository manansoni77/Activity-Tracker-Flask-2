from datetime import datetime
from flask import render_template
import pandas
from mail.app import send_email
from app import client
from app.models import Credentials, User, Trackers, Logs
from app.resources import tracker_resource_fields, log_resource_fields
from app.plot import save_plot
from flask_restful import marshal
import pandas
import io


@client.task()
def send_welcome_email(username, email_id):
    message = render_template('welcome.html', username=username)
    send_email(email_id, 'Welcome to Todo App!', message)


@client.task()
def send_monthly_report():
    creds = Credentials.query.all()
    for cred in creds:
        user = User.query.filter_by(user_id=cred.user_id).first()
        username = f'{user.first_name} {user.last_name}'
        trackers = Trackers.query.filter_by(user_id=user.user_id).all()
        tracker_data = [marshal(x, tracker_resource_fields) for x in trackers]
        for i, tracker in enumerate(trackers):
            logs = Logs.query.filter_by(track_id=tracker.track_id).all()
            tracker_data[i]['logs'] = [marshal(x, log_resource_fields) for x in logs]
            tracker_data[i]['plot'] = save_plot(tracker, logs)
        message = render_template('monthly_report_message.html', username=username)
        report = render_template('monthly_report.html', username = username, tracker_data = tracker_data)
        report_name = f'{user.first_name}_{user.last_name}-monthly_report.html'
        report = io.BytesIO(bytes(report, 'utf-8'))
        send_email(cred.email_id, 'Monthly Report', message, [(report, report_name)])

@client.task()
def send_tracker_report(user_id, track_id):
    cred = Credentials.query.filter_by(user_id=user_id).first()
    user = User.query.filter_by(user_id=user_id).first()
    track = Trackers.query.filter_by(track_id=track_id).first()
    tracker_logs = Logs.query.filter_by(track_id=track_id).all()
    val = []
    time = []
    for log in tracker_logs:
        val.append(log.info)
        time.append(log.time)
    df = pandas.DataFrame({'time':time,'val':val})
    csvfile = io.BytesIO()
    df.to_csv(csvfile)
    csvfile_name = f'{user.first_name}_{user.last_name}-{track.track_name}.csv'
    username = f'{user.first_name} {user.last_name}'
    message = render_template('monthly_report_message.html', username=username, trackername=track.track_name)
    send_email(cred.email_id,f'{track.track_name} Logs Summary', message, [(csvfile, csvfile_name)])

@client.task()
def send_daily_reminder():
    creds = Credentials.query.all()
    today = datetime.utcnow().date()
    for cred in creds:
        if cred.last_login.date() == today:
            pass
        user = User.query.filter_by(user_id = cred.user_id).first()
        username = f'{user.first_name} {user.last_name}'
        message = render_template('daily_reminder.html', username=username)
        send_email(cred.email_id, 'Daily Reminder!', message)