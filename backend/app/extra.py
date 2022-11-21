import random
from datetime import datetime, timedelta
import re


def ran_color():
    colors = ['mediumpurple', 'lightcoral', 'lemonchiffon',
              'lightskyblue', 'palegreen', 'peachpuff', 'paleturquoise']
    t = random.choice(colors)
    return t


def to_timedelta(time):
    tmp = datetime.strptime(time, "%H:%M:%S")
    return timedelta(hours=tmp.hour, minutes=tmp.minute)


code_time = '%Y-%m-%dT%H:%M'
format = "%d-%m-%Y %H:%M:%S"


login_re = re.compile(r'[^a-zA-Z0-9@.]').search
password_re = re.compile(r'[^a-zA-Z0-9$]').search
options_re = re.compile(r'[^a-zA-Z0-9 !?]').search
text_re = re.compile(r'[^a-zA-Z0-9 !?]').search
