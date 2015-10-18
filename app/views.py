# coding=utf-8
__author__ = 'drole'

from flask import render_template, request, redirect, url_for, jsonify
from forms import EditForm
from app import app
import redis
import json

POOL = redis.ConnectionPool(host='localhost', port=6379, db=0)


@app.route('/submit', methods=['POST', 'GET'])
def submit():
    return render_template('submit.html')


@app.route('/test', methods=['POST', 'GET'])
def test():
    db = redis.StrictRedis(connection_pool=POOL)
    db.set('lol', 'looool')
    if request.method == 'POST':
        f = EditForm()
        offerline = {'itemString': f.itemString.data,
                     'itemBrand': f.itemBrand.data}
        if f.itemPrice.data is not None:
            offerline['itemPricePerUnit'] = int(f.itemPrice.data)
        if f.itemPricePerUnit.data is not None:
            offerline['itemPricePerUnit'] = int(f.itemPricePerUnit.data)
        print("validate")
        print(offerline)
        db.set('stuff2', offerline)
        return redirect(url_for('test'))
    else:
        print("novalidate")
        forms = []
        form = EditForm(itemString='LOL', itemPricePerUnit=25)
        iS = 'pære'.decode('utf-8')
        form2 = EditForm(itemString=iS, itemPricePerUnit=2)
        forms.append(form)
        forms.append(form2)
        return render_template('showOfferSpecs.html',
                               forms=forms)


@app.route('/update', methods=['POST'])
def update():
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
    offerline = {'itemString': itemString,
                 'itemBrand': itemBrand}
    if itemPrice is not None:
        offerline['itemPricePerUnit'] = int(itemPrice)
    if itemPricePerUnit is not None:
        offerline['itemPricePerUnit'] = int(itemPricePerUnit)
    #send to server
    db.lset(name, indexOfLine, offerline)
    return jsonify({'status': 200,
                    'message': 'ok',
                    'itemString': itemString,
                    'itemBrand': itemBrand,
                    'itemPrice': itemPrice,
                    'itemPricePerUnit': itemPricePerUnit})


@app.route('/', methods=['POST', 'GET'])
def index():
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
    #form = EditForm()
    forms = []
    #create object from the stuff we get
    searches = db.lrange('listone', 0, -1)
    searches = [x.decode('unicode_escape') for x in searches]
    searches = [json.loads(x.replace("'", "\"")) for x in searches]
    for idx, search in enumerate(searches):
        form = EditForm(itemString=search['itemString'].encode('latin-1').decode('utf-8'),
                        itemPricePerUnit=search['itemPricePerUnit'],
                        id=idx)
        forms.append(form)
    return render_template("showOfferSpecs.html",
                           forms=forms)
