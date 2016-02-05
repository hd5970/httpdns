from flask import Flask, render_template

from main.forms import AddNameServer
from . import admin


@admin.route('/', methods=['get', 'post'])
def admin():
    form = AddNameServer()
    return render_template('admin.html', form=form)
