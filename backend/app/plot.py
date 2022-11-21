import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as plticker
import pandas as pd
import random
from datetime import datetime, timedelta
import io
import base64

def ran_color():
    colors = ['mediumpurple','lightcoral','lemonchiffon','lightskyblue','palegreen','peachpuff','paleturquoise']
    t = random.choice(colors)
    return t

def to_timedelta(time):
    tmp = datetime.strptime(time,"%H:%M:%S")
    return timedelta(hours=tmp.hour,minutes=tmp.minute)



def save_plot(track, logs):
    val = []
    time = []
    if len(logs) == 0:
        return False
    for log in logs:
        val.append(log.info)
        time.append(log.time.date())
    fig, ax = plt.subplots(figsize=(5,5))
    df = pd.DataFrame({'time':time,'val':val})
    df = df.sort_values(['time'])
    print(df)
    if track.track_type == 'num':
        df['val'] = df['val'].astype(int)
        plot_df = df.groupby(['time']).sum()
        ax.set_title(f'{track.track_name} Graph')
        ax.set_ylabel(f'{track.options}')
        ax.set_xlabel('Date')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        ax.bar(plot_df.index,plot_df['val'],color=ran_color())
    elif track.track_type == 'time':
        df['val'] = df.apply(lambda row : to_timedelta(row['val']),axis=1)
        plot_df = df.groupby(['time']).sum()
        plot_df['val'] = plot_df['val'].astype('timedelta64[m]')
        ax.set_title(f'{track.track_name} Graph')
        ax.set_ylabel('Time Duration (Minutes)')
        ax.set_xlabel('Date')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        ax.bar(plot_df.index,plot_df['val'],color=ran_color())
    elif track.track_type == 'mcq' or track.track_type == 'bool':
        freq = df['val'].value_counts()
        labels = []
        data = []
        for l,d in freq.iteritems():
            labels.append(l)
            data.append(d)
        ax.pie(data,labels=labels)
    elif track.track_type == 'bool':
        labels = track.options.split(',')
        freq = {key: 0 for key in labels}
        for i in df['val']:
            freq[i]+=1
        data = []
        for label in labels:
            data.append(freq[label])
        ax.set_ylabel('Count')
        ax.yaxis.set_major_locator(plticker.MultipleLocator(base=1))
        ax.bar(labels,data,color=ran_color())
    buffer = io.BytesIO()
    fig.savefig(buffer, format='jpg')
    buffer.seek(0)
    converted_string = base64.b64encode(buffer.read())
    return converted_string.decode('utf-8')