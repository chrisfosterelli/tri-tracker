#!/usr/bin/env python3
# Christopher Foster

from os import environ
from bottle import get, post
from bottle import request, template
from bottle import run as startBottle
from pymongo import MongoClient
from datetime import datetime

port  = int(environ['mongo_port'])
host  = environ['mongo_host']
db    = environ['mongo_db']
user  = environ['mongo_user']
passw = environ['mongo_pass']

client   = MongoClient(host, port)
database = client[db]

database.authenticate(user, passw)
records = database.records

def round_to_day(time, leeway=5):
	if time.hour > leeway: return datetime(time.year, time.month, time.day)
	else: return datetime(time.year, time.month, time.day - 1)

@get('/')
def index():
	return template('create_record');

@post('/record')
def create_record():
	record = {
		'time'     : request.forms.get('time'),
		'distance' : request.forms.get('distance'),
		'type'     : request.forms.get('type'),
		'date'     : round_to_day(datetime.today()),
		'entry'    : datetime.today()
	}
	records.insert(record)
	return 'ok'

startBottle(host='0.0.0.0', port=8080)
