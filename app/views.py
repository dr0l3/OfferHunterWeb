# coding=utf-8
__author__ = 'drole'

from flask import render_template, request, redirect, url_for, jsonify, session
from forms import EditForm, InsertForm, LoginForm
from app import app
import redis
import json

POOL = redis.ConnectionPool(host='redis', port=6379, db=0)


@app.route('/trylogin', methods=['POST'])
def trylogin():
    user = request.form['username']
    pw = request.form['pw']
    db = redis.StrictRedis(connection_pool=POOL)
    if db.hget('userRecords', user) == pw:
        print("success")
        session['user'] = user
        return jsonify({'status': 200,
                 'message': 'ok'})
    print("fail")
    return jsonify({'status': 406,
                    'message': 'bad login'})


@app.route('/insert', methods=['POST'])
def insert():
    print(request)
    db = redis.StrictRedis(connection_pool=POOL)
    #get the parameters
    name = request.form['nameOfList']
    itemString = request.form['itemString']
    itemBrand = request.form['itemBrand']
    itemPrice = request.form['itemPrice']
    itemPricePerUnit = request.form['itemPricePerUnit']
    #convert to dict
    offerline = {'itemString': itemString}
    if not itemBrand == "":
        offerline['itemBrand'] = itemBrand
    if not itemPrice == "":
        offerline['itemPricePerUnit'] = float(itemPrice)
    if not itemPricePerUnit == "":
        offerline['itemPricePerUnit'] = float(itemPricePerUnit)
    #send to server
    db.rpush(name,  offerline)
    return jsonify({'status': 200,
                    'message': 'ok',
                    'itemString': itemString,
                    'itemBrand': itemBrand,
                    'itemPrice': itemPrice,
                    'itemPricePerUnit': itemPricePerUnit})


@app.route('/update', methods=['POST'])
def update():
    print("LOL")
    print(request)
    print(request.form['itemString'])
    #connect to server
    db = redis.StrictRedis(connection_pool=POOL)
    #get the parameters
    name = request.form['nameOfList']
    indexOfLine = request.form['indexOfLine']
    itemString = request.form['itemString']
    itemBrand = request.form['itemBrand']
    itemPrice = request.form['itemPrice']
    itemPricePerUnit = request.form['itemPricePerUnit']
    #convert to dict
    offerline = {'itemString': itemString}
    if not itemBrand == "":
        offerline['itemBrand'] = itemBrand
    if not itemPrice == "":
        offerline['itemPricePerUnit'] = float(itemPrice)
    if not itemPricePerUnit == "":
        offerline['itemPricePerUnit'] = float(itemPricePerUnit)
    #send to server
    db.lset(name, indexOfLine, offerline)
    return jsonify({'status': 200,
                    'message': 'ok',
                    'itemString': itemString,
                    'itemBrand': itemBrand,
                    'itemPrice': itemPrice,
                    'itemPricePerUnit': itemPricePerUnit})


@app.route('/home', methods=['POST', 'GET'])
def home():
    user = session.get(u'user')
    if not user:
        redirect('/login')
    #get database access
    db = redis.StrictRedis(connection_pool=POOL)
    if request.method == 'POST':
        f = EditForm()
        offerline = {'itemString': f.itemString.data,
                     'itemBrand': f.itemBrand.data}
        if f.itemPrice.data is not None:
            offerline['itemPricePerUnit'] = int(f.itemPrice.data)
        if f.itemPricePerUnit.data is not None:
            offerline['itemPricePerUnit'] = int(f.itemPricePerUnit.data)
        db.set('stuff2', offerline)
    insertform = InsertForm(listId=user,
                            id='insert')
    #form = EditForm()
    updateforms = []
    #create object from the stuff we get
    searches = db.lrange(user, 0, -1)
    searches = [x.decode('unicode_escape') for x in searches]
    searches = [json.loads(x.replace("'", "\"").replace("u\"", "\"")) for x in searches]
    for idx, search in enumerate(searches):
        try:
            itemString = search['itemString'].encode('latin-1').decode('latin-1')
        except KeyError:
            itemString = ""
        try:
            itemBrand = search['itemBrand'].encode('latin-1').decode('latin-1')
        except KeyError:
            itemBrand = None
        try:
            itemPricePerUnit = search['itemPricePerUnit']
        except KeyError:
            itemPricePerUnit = None
        try:
            itemPrice = search['itemPrice']
        except KeyError:
            itemPrice = None
        form = EditForm(itemString=itemString,
                        itemBrand=itemBrand,
                        itemPricePerUnit=itemPricePerUnit,
                        itemPrice=itemPrice,
                        id=str(idx),
                        listId=user)
        updateforms.append(form)
    print("go render")
    return render_template("showOfferSpecs.html",
                           updateforms=updateforms,
                           insertform=insertform)


@app.route('/')
def login():
    loginform = LoginForm()
    return render_template('login.html', loginform=loginform)
