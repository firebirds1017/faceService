#!/usr/bin/env python

# start script#######

import os
from app import create_app
from flask_script import Manager, Shell


app = create_app(os.getenv('FLASK_ENV') or 'default')
manage = Manager(app)


def make_shell_context():
    return dict(app=app)


manage.add_command("shell", Shell(make_context=make_shell_context))


if __name__ == "__main__":
    manage.run()
