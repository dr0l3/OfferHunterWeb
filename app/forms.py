__author__ = 'drole'


from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, DecimalField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length


class LoginForm(Form):
    userName = StringField(u'Username', validators=[DataRequired()])
    userpw = StringField(u'Password', validators=[DataRequired])
    submit = SubmitField(u'Login')


class InsertForm(Form):
    itemString = StringField(u'Name of the item', validators=[DataRequired()])
    itemBrand = StringField(u'Brand requirement if any')
    itemPricePerUnit = DecimalField(u'Price per unit')
    itemPrice = DecimalField(u'Price for a unit')
    id = HiddenField()
    listId = HiddenField()
    submit = SubmitField(u'Insert')


class EditForm(Form):
    itemString = StringField(u'Name of the item', validators=[DataRequired()])
    itemBrand = StringField(u'Brand requirement if any')
    itemPricePerUnit = DecimalField(u'Price per unit')
    itemPrice = DecimalField(u'Price for a unit')
    id = HiddenField()
    listId = HiddenField()
    submit = SubmitField(u'Update')
