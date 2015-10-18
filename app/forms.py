__author__ = 'drole'


from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Length

class EditForm(Form):
    offerItemString = StringField('offer-item-string2', validators=[DataRequired()])
    itemBrand = StringField('offer-item-brand')
    itemPricePerUnit = DecimalField('offer-item-pricePerUnit')
    itemPrice = DecimalField('offer-item-price')