import os

from flask import g
from flask.views import View

from db.db import Database
from db.categories import Categories


class DatabaseView(View):
    ''' Initializes the database global '''

    def __init__(self, *args, **kwargs):
        if os.environ.get('FLASK_DEBUG') == '1':
            g.db = Database(debugging=True)
        else:
            g.db = Database()

        g.categories = g.db.query(Categories).all()
