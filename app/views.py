__author__ = 'drole'

from flask import render_template
from forms import EditForm
from app import app
import redis
import json


@app.route('/')
def index():
    form = EditForm()
    #get database access
    db = redis.StrictRedis(host='localhost', port=6379, db=0)
    #create object from the stuff we get
    searches = db.lrange('listone', 0, -1)
    searches = [json.loads(x.replace("'", "\"")) for x in searches]
    return render_template("index.html",
                           searches = searches,
                           form = form)
