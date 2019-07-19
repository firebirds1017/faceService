#!/usr/bin/env python

# start script#######

import os
from app import create_app

app = create_app(os.getenv('FLASK_ENV') or 'default')
"""
init app
"""
app.app_context().push()
if __name__ == "__main__":
    app.run()
