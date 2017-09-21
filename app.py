from flask import Flask

from views.category import CategoryView


app = Flask(__name__)


# The root path
app.add_url_rule(
    '/',
    defaults={'c_path': None},
    view_func=CategoryView.as_view('landing'),
    methods=['GET']
)

# Shows all of the categories or creates a new one
app.add_url_rule(
    '/c/',
    defaults={'c_path': None},
    view_func=CategoryView.as_view('categories'),
    methods=['GET', 'POST']
)

# Shows or updates a single category
app.add_url_rule(
    '/c/<c_path>',
    view_func=CategoryView.as_view('category'),
    methods=['GET', 'POST']
)

# Deletes a single category
app.add_url_rule(
    '/c/<c_path>/delete/',
    view_func=CategoryView.as_view('cat_delete'),
    methods=['GET', 'POST']
)
