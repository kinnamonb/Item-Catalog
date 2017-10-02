from flask import render_template, request, redirect, url_for, g

from .db_view import DatabaseView
from db.categories import Categories
from db.items import Items


class CategoryView(DatabaseView):
    ''' Handles Category requests '''
    methods = ['GET', 'POST']

    def dispatch_request(self, c_path):
        ''' Handles all Category requests '''
        path = request.path
        method = request.method
        # Landing
        if path == '/':
            items = g.db.query(Items).limit(10).all()
            return render_template('cat_list.html', items=items)
        # Create a new category
        elif path == '/c/' and method == 'GET':
            category = Categories()
            return render_template('cat_form.html', category=category)
        elif path == '/c/' and method == 'POST':
            return self.save_form()
        # View a category
        elif path == '/c/{0}/'.format(c_path) and method == 'GET':
            category = g.db.query(Categories).filter_by(path=c_path).first()
            return render_template('cat_list.html', category=category, items=category.items)
        # Update a category
        elif path == '/c/{0}/update/'.format(c_path) and method == 'GET':
            category = g.db.query(Categories).filter_by(path=c_path).first()
            return render_template('cat_form.html', category=category)
        elif path == '/c/{0}/update/'.format(c_path) and method == 'POST':
            category = g.db.query(Categories).filter_by(path=c_path).first()
            return self.save_form(category)
        # Delete a category
        elif path == '/c/{0}/delete/'.format(c_path) and method == 'GET':
            category = g.db.query(Categories).filter_by(path=c_path).first()
            return render_template('cat_confirm.html', category=category)
        elif path == '/c/{0}/delete/'.format(c_path) and method == 'POST':
            category = g.db.query(Categories).filter_by(path=c_path).first()
            return self.delete_cat(category)
        # Should never get here, but just in case
        return render_template('category.html')

    def save_form(self, category=None):
        ''' Creates or updates a Categories object based upon form data '''
        # Get the form data as a dictionary
        data = request.form.to_dict()
        # If no category was given, make a new one
        if category is None:
            category = Categories(**data)
        # If a category was given, update it
        else:
            category.update(data)
        # Check the category object for errors
        if len(category.errors) > 0:
            # Rerender the form with the data and the error messages
            return render_template('cat_form.html', category=category)
        else:
            # Update the database
            g.db.add(category)
            g.db.commit()
            # Redirect to the category
            return redirect(url_for('cat_read', c_path=category.path))

    def delete_cat(self, category):
        g.db.delete(category)
        g.db.commit()
        return redirect(url_for('landing'))
