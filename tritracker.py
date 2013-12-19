#!/usr/bin/env python3
# Christopher Foster

from os import environ
from bottle import redirect
from bottle import static_file
from bottle import get, post, route
from bottle import request, template, view
from bottle import run as startBottle
from bson.objectid import ObjectId
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

def calculate_pace(time, distance):
	minutes = get_seconds(time) / 60
	kilometers = float(distance[:-2])
	return minutes / kilometers

def get_seconds(time_string):
	split = time_string.split(':')
	return float(split[0]) * 60 + float(split[1]) * 1

def get_entry_comparison(record1, record2):
	time1 = get_seconds(record1['time'])
	if record2: time2 = get_seconds(record2['time'])
	else: time2 = time1
	return {
		'percentage' : (100 - ((time1 / time2) * 100)),
		'seconds'    : (time2 - time1)
	}

def round_to_date(time, leeway=5):
	if time.hour > leeway: return datetime(time.year, time.month, time.day)
	else: return datetime(time.year, time.month, time.day - 1)

def days_since_last_entry():
	last = records.find().sort('date', -1).limit(1)
	diff = datetime.now() - last[0]['date']
	return diff.days

def get_previous_entry(record):
	return records.find_one({
		'type'     : record['type'],
		'distance' : record['distance'],
		'date'     : {
			'$lte' : record['date']
		}
	})

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
	record_id = records.insert(record)
	redirect('/record/' + str(record_id))

@get('/record/<record>')
@view('display_record')
def display_record(record):
	item = records.find_one(ObjectId(record))
	last = get_previous_entry(item)
	dif = get_entry_comparison(item, last)
	pace = calculate_pace(item['time'], item['distance'])
	return {
		'pace'       : pace,
		'time'       : item['time'],
		'distance'   : item['distance'],
		'type'       : item['type'],
		'date'       : item['date'],
		'percentage' : dif['percentage'],
		'seconds'    : dif['seconds']
	}

@route('/static/<filename>')
def server_static(filename):
	return static_file(filename, root='static')

startBottle(host='0.0.0.0', port=8080)
