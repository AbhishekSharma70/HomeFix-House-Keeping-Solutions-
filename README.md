Set up your twilio account and append the credentials in the config.py file 
For Frontend run the following commands - 
1.npm install
2.npm run serve
For backend run the following commands in different terminals-
1.pip3 install flask redis celery
2.flask run --port 8000
3.celery -A tasks worker --loglevel=info
4.redis-server




