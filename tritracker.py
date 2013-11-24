#!/usr/bin/env python3
# Christopher Foster

from os import environ
from bottle import redirect
from bottle import static_file
from bottle import get, post, route
from bottle import request, template, view
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

def round_to_date(time, leeway=5):
	if time.hour > leeway: return datetime(time.year, time.month, time.day)
	else: return datetime(time.year, time.month, time.day - 1)

def days_since_last_entry():
	last = records.find(timeout=False).sort('date', -1).limit(1)
	diff = datetime.now() - last[0]['date']
	return diff.days

@get('/')
@view('create_record')
def index():
	return {
		'days_since_last_entry' : days_since_last_entry()
	}

@post('/record')
def create_record():
	record = {
		'time'     : request.forms.get('time'),
		'distance' : request.forms.get('distance'),
		'type'     : request.forms.get('type'),
		'date'     : round_to_date(datetime.today()),
		'entry'    : datetime.today()
	}
	records.insert(record)
	redirect('/')

@route('/static/<filename>')
def server_static(filename):
	return static_file(filename, root='static')

startBottle(host='0.0.0.0', port=8080)
