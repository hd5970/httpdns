# coding=utf-8
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, IPAddress

from app.models import get_all_provinces


class AddNameServer(Form):
    domain = StringField(u'域名', validators=[DataRequired()])
    ip = StringField(u'IP', validators=[DataRequired(), IPAddress()])
    provinces = SelectField(u'省份')
    priority = IntegerField(u'权重')
    submit = SubmitField(u'提交')

    @classmethod
    def set_provinces(cls):
        form = cls()
        form.provinces.choices = get_all_provinces(choices=True)
        return form


class CurrentDomain(Form):
    @classmethod
    def append_field(cls, name, field):
        setattr(cls, name, field)


def data_to_form(domain):
    class_name = 'Form%d' % domain.id
    form = type(class_name, (CurrentDomain,), {})
    for ip in domain.ips:
        name = 'ip_%s' % ip.id
        form.append_field(name, StringField('ip%s' % ip.ip, validators=[DataRequired(), IPAddress()]))
        province_name = 'province_%s' % ip.id
        choices = get_all_provinces(choices=True, default=ip.province_name)
        form.append_field(province_name, SelectField(u'province', choices=choices))
    form.append_field('submit', SubmitField(u'提交'))
    return form()
