#!/usr/bin/env python3
# Christopher Foster

from os import environ
from bottle import redirect
from bottle import auth_basic
from bottle import static_file
from bottle import template, view
from bottle import request, response
from bottle import get, post, route, error
from bottle import run as startBottle
from bson.objectid import ObjectId
from pymongo import MongoClient
from datetime import datetime
from datetime import timedelta

port  = int(environ['MONGO_PORT'])
host  = environ['MONGO_HOST']
db    = environ['MONGO_DB']
user  = environ['MONGO_USER']
passw = environ['MONGO_PASS']

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

def get_timestring(seconds):
    return '%d:%02d' % (seconds / 60, seconds % 60)

def get_entry_comparison(record1, record2):
    time1 = get_seconds(record1['time'])
    if record2: time2 = get_seconds(record2['time'])
    else: time2 = time1
    return {
        'percentage' : (100 - ((time1 / time2) * 100)),
        'seconds'    : (time2 - time1)
    }

def get_three_months_ago(date):
    return date - timedelta(days=3*30) 

def round_to_date(time, leeway=5):
    if time.hour > leeway: return datetime(time.year, time.month, time.day)
    else: return datetime(time.year, time.month, time.day - 1)

def days_since_last_entry():
    last = records.find().sort('date', -1).limit(1)
    diff = datetime.now() - last[0]['date']
    return diff.days

def get_previous_entry(record):
    return records.find({
        'type'     : record['type'],
        'distance' : record['distance'],
        'date'     : {
            '$lt' : record['date']
        }
    }).sort('date', -1).limit(1)[0]

def get_best_entry(record):
    return records.find({
        'type'     : record['type'],
        'distance' : record['distance'],
        'date'     : {
            '$lt' : record['date']
        },
        '_id' : {
            '$ne' : record['_id']
        }
    }).sort('time', 1).limit(1)[0]

def create_average_entry(record):
    record_set = records.find({
        'type'     : record['type'],
        'distance' : record['distance'],
        'date'     : {
            '$lt' : record['date'],
            '$gt' : get_three_months_ago(record['date'])
        },
        '_id' : {
            '$ne' : record['_id']
        }
    })
    total_time = 0
    for record in record_set:
        total_time += get_seconds(record['time'])
    return {
        'type'     : record['type'],
        'distance' : record['distance'],
        'time'     : get_timestring(total_time / record_set.count())
    }

def ensure_auth(user, pas):
    if user != environ.get('AUTH_USER', 'TEST'): return False
    if pas != environ.get('AUTH_PASS', 'TEST'): return False
    return True
    

@get('/')
@view('create_record')
@auth_basic(ensure_auth)
def index():
    return {
        'days_since_last_entry' : days_since_last_entry()
    }

@post('/record')
@auth_basic(ensure_auth)
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
@auth_basic(ensure_auth)
def display_record(record):
    item = records.find_one(ObjectId(record))
    last = get_previous_entry(item)
    avrg = create_average_entry(item)
    best = get_best_entry(item)
    last_dif = get_entry_comparison(item, last)
    avrg_dif = get_entry_comparison(item, avrg)
    best_dif = get_entry_comparison(item, best)
    pace = calculate_pace(item['time'], item['distance'])
    return {
        'pace'       : pace,
        'time'       : item['time'],
        'distance'   : item['distance'],
        'type'       : item['type'],
        'date'       : item['date'],
        'previous' : {
            'percentage' : last_dif['percentage'],
            'seconds'    : last_dif['seconds']
        },
        'average' : {
            'percentage' : avrg_dif['percentage'],
            'seconds'    : avrg_dif['seconds']
        },
        'best' : {
            'percentage' : best_dif['percentage'],
            'seconds'    : best_dif['seconds']
        }
    }

@route('/static/<filename>')
@auth_basic(ensure_auth)
def server_static(filename):
    return static_file(filename, root='static')

@error(401)
def error401(error):
    response.headers['WWW-Authenticate'] = 'Basic realm="Login required"' 
    return 'You must authenticate'

startBottle(host='0.0.0.0', port=environ.get('PORT', 8080))
