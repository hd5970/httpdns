# -*- coding: utf-8 -*-
import os

from celery import Celery
from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy

from config import config

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
celery = Celery(__name__, broker=os.environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379')


def create_app(config_name):
    app = Flask(__name__, static_url_path='/issue/static')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    # celery.conf.update(app.config)
    from main import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    return app
