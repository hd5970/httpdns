#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager, Shell

from app import create_app, db
from app.implement import reload_redis
from app.models import Province

app = create_app('default')
# with app.app_context():
#     reload_redis()
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def profile(length=25, profile_dir=None):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()


@manager.command
def deploy():
    """Run deployment tasks."""
    db.drop_all()
    db.create_all()
    Province.insert_provinces()


if __name__ == '__main__':
    with app.app_context():
        reload_redis()
    manager.run()
