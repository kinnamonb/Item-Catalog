import random
import string
import os

from flask import Flask, render_template

from views.category import CategoryView
from views.auth import AuthView
from views.item import ItemView
from db.items import Items


app = Flask(__name__)
app.secret_key = ''.join(random.SystemRandom().choice(string.printable) for _ in range(32))

if not app.debug:
    import logging
    from logging import FileHandler
    file_handler = FileHandler(os.path.join(os.path.dirname(__file__), 'error.log'))
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)


# The root path
app.add_url_rule(
    '/',
    defaults={'c_path': None},
    view_func=CategoryView.as_view('landing'),
    methods=['GET']
)

# Creates a new category
app.add_url_rule(
    '/c/',
    defaults={'c_path': None},
    view_func=CategoryView.as_view('cat_new')
)

# Shows a category
app.add_url_rule(
    '/c/<c_path>/',
    view_func=CategoryView.as_view('cat_read'),
    methods=['GET']
)

# Updates a category
app.add_url_rule(
    '/c/<c_path>/update/',
    view_func=CategoryView.as_view('cat_update'),
    methods=['GET', 'POST']
)

# Deletes a category
app.add_url_rule(
    '/c/<c_path>/delete/',
    view_func=CategoryView.as_view('cat_delete'),
    methods=['GET', 'POST']
)

# Creates a new item
app.add_url_rule(
    '/c/<c_path>/i/',
    defaults={'i_path': None},
    view_func=ItemView.as_view('item_new'),
    methods=['GET', 'POST']
)

# Shows an item
app.add_url_rule(
    '/c/<c_path>/i/<i_path>/',
    view_func=ItemView.as_view('item_read'),
    methods=['GET']
)

# Shows an item (JSON)
app.add_url_rule(
    '/c/<c_path>/i/<i_path>/json',
    view_func=ItemView.as_view('item_json'),
    methods=['GET']
)

# Updates an item
app.add_url_rule(
    '/c/<c_path>/i/<i_path>/update/',
    view_func=ItemView.as_view('item_update'),
    methods=['GET', 'POST']
)

# Deletes an item
app.add_url_rule(
    '/c/<c_path>/i/<i_path>/delete/',
    view_func=ItemView.as_view('item_delete'),
    methods=['GET', 'POST']
)

# Login
app.add_url_rule(
    '/login/',
    view_func=AuthView.as_view('login'),
    methods=['GET', 'POST']
)

# Logout
app.add_url_rule(
    '/logout/',
    view_func=AuthView.as_view('logout'),
    methods=['GET', 'POST']
)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
