To run this project -> 

1) Run redis, mailhog, celery (worker, beat, flower) in order
2) Run main.py
3) Run frontend in respective folder
4) You can then interact with project at localhost:8080
5) Here you can signup or login and will then be redirected to dashboard
6) In the dashboard, press the 'add tracker' button to add a tracker. 
7) To add logs, press the Log button in the table of trackers
8) To see details about the tracker, press the name of the tracker
9) A graph will be displayed and details of the logs



REDIS
redis-server restart
redis-server
redis-server stop
redis-cli

MAILHOG
~/go/bin/MailHog

CELERY
celery -A main.client worker --loglevel=info 

FLOWER
celery -A main.client flower --address=localhost --port=5566

BEAT
celery -A main.client beat

NPM
npm run serve 
npm run build