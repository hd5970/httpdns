# coding=utf-8
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, IPAddress, NumberRange, Email


class AddNameServer(Form):
    domain = StringField(u'域名', validators=[DataRequired()])
    ip = StringField(u'IP', validators=[DataRequired()])
    submit = SubmitField(u'提交')
