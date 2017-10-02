import os

from flask import g, session
from flask.views import View

from db.db import Database
from db.categories import Categories
from db.users import Users


class DatabaseView(View):
    ''' Initializes the database global '''

    def __init__(self, *args, **kwargs):
        if os.environ.get('FLASK_DEBUG') == '1':
            g.db = Database(debugging=True)
        else:
            g.db = Database()

        if session.get('user_id'):
            g.user = g.db.query(Users).get(session['user_id'])

        g.categories = g.db.query(Categories).all()
