__author__ = 'drole'

#!flask/bin/python

from app import app
app.debug = True
app.run(host='0.0.0.0')