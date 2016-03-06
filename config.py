# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hello sunqi'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WHOOSH_BASE = os.path.join(basedir, 'search.db')
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379'
    BOOTSTRAP_SERVE_LOCAL = True
    REDIS_URL = "redis://localhost:6379/0"
    # SERVER_NAME = os.environ.get('SERVER_NAME') or 'dns.sunqi.me'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    def __init__(self):
        pass

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


config = {
    'default': DevelopmentConfig
}
