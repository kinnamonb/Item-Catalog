import random
import string

from flask import render_template, request, redirect, url_for, g, session, jsonify

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
        g.state = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
        # Create a new item
        if path == url_for('item_new', c_path=c_path) and method == 'GET':
            if g.get('user') is not None:
                session['state'] = g.state  # CSRF protection
                item = Items()
                return render_template('item_form.html', item=item)
        elif path == url_for('item_new', c_path=c_path) and method == 'POST':
            if g.get('user') is not None and request.args.get('state') == session['state']:
                return self.save_form(category)
        # View an item
        elif path == url_for('item_read', c_path=c_path, i_path=i_path) and method == 'GET':
            item = g.db.query(Items).filter_by(category=category, path=i_path).first()
            if item is not None:
                return render_template('item_read.html', item=item)
        # View an item (JSON)
        elif path == url_for('item_json', c_path=c_path, i_path=i_path) and method == 'GET':
            item = g.db.query(Items).filter_by(category=category, path=i_path).first()
            return jsonify(item=item.serialize)
        # Update an item
        elif path == url_for('item_update', c_path=c_path, i_path=i_path) and method == 'GET':
            item = g.db.query(Items).filter_by(category=category, path=i_path).first()
            if g.get('user') and g.user == item.user:
                session['state'] = g.state  # CSRF protection
                return render_template('item_form.html', item=item)
        elif path == url_for('item_update', c_path=c_path, i_path=i_path) and method == 'POST':
            item = g.db.query(Items).filter_by(category=category, path=i_path).first()
            if g.get('user') and g.user == item.user and request.args.get('state') == session['state']:
                return self.save_form(category, item)
        # Delete an item
        elif path == url_for('item_delete', c_path=c_path, i_path=i_path) and method == 'GET':
            item = g.db.query(Items).filter_by(category=category, path=i_path).first()
            if g.get('user') and g.user == item.user:
                session['state'] = g.state  # CSRF protection
                return render_template('item_confirm.html', item=item)
        elif path == url_for('item_delete', c_path=c_path, i_path=i_path) and method == 'POST':
            item = g.db.query(Items).filter_by(category=category, path=i_path).first()
            if g.get('user') and g.user == item.user and request.args.get('state') == session['state']:
                return self.delete_item(item)
        return render_template('404.html')

    def save_form(self, category, item=None):
        ''' Creates or updates an Item '''
        # Get the form data
        data = request.form.to_dict()
        # If no item was given, make one
        if item is None:
            item = Items(**data)
            item.user = g.user
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
