from flask import render_template, request, redirect, url_for, g

from .db_view import DatabaseView
from db.items import Items
from db.categories import Categories


class ItemView(DatabaseView):
    ''' Handles Item requests '''
    methods = ['GET', 'POST']

    def dispatch_request(self, c_path, i_path):
        ''' Handles all Item requests '''
        path = request.path
        method = request.method
        category = g.db.query(Categories).filter_by(path=c_path).first()
        # Create a new item
        if path == '/c/{0}/i/'.format(c_path) and method == 'GET':
            item = Items()
            return render_template('item_form.html', item=item)
        elif path == '/c/{0}/i/'.format(c_path) and method == 'POST':
            return self.save_form(category)
        # View an item
        elif path == '/c/{0}/i/{1}/'.format(c_path, i_path) and method == 'GET':
            item = g.db.query(Items).filter_by(category=category, path=i_path).first()
            return render_template('item_read.html', item=item)
        # Update an item
        elif path == '/c/{0}/i/{1}/update/'.format(c_path, i_path) and method == 'GET':
            item = g.db.query(Items).filter_by(category=category, path=i_path).first()
            return render_template('item_form.html', item=item)
        elif path == '/c/{0}/i/{1}/update/'.format(c_path, i_path) and method == 'POST':
            item = g.db.query(Items).filter_by(category=category, path=i_path).first()
            return self.save_form(category, item)
        # Delete an item
        elif path == '/c/{0}/i/{1}/delete/'.format(c_path, i_path) and method == 'GET':
            item = g.db.query(Items).filter_by(category=category, path=i_path).first()
            return render_template('item_confirm.html', item=item)
        elif path == '/c/{0}/i/{1}/delete/'.format(c_path, i_path) and method == 'POST':
            item = g.db.query(Items).filter_by(category=category, path=i_path).first()
            return self.delete_item(item)

    def save_form(self, category, item=None):
        ''' Creates or updates an Item '''
        # Get the form data
        data = request.form.to_dict()
        # If no item was given, make one
        if item is None:
            item = Items(**data)
        # Otherwise update the item
        else:
            item.update(data)
        item.category_id = category.id
        # Check for errors
        if len(item.errors) > 0:
            # Rerender the form
            return render_template('item_form.html', item=item)
        else:
            # Update the database
            g.db.add(item)
            g.db.commit()
            # Redirect to the item
            return redirect(url_for('item_read', c_path=category.path, i_path=item.path))

    def delete_item(self, item):
        g.db.delete(item)
        g.db.commit()
        return redirect(url_for('landing'))
