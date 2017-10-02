import random
import string
import httplib2
import requests

from flask import render_template, request, redirect, url_for, g, session, json, flash
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from .db_view import DatabaseView
from db.users import Users


class AuthView(DatabaseView):
    ''' Handles authentication requests '''
    methods = ['GET', 'POST']

    def dispatch_request(self):
        ''' Handles authentication requests '''
        path = request.path
        method = request.method
        if session.get('user_id'):
            g.user = g.db.query(Users).get(session['user_id'])
        # Handle logins
        if path == url_for('login') and method == 'GET':
            return render_template('login.html')
        elif path == url_for('login') and method == 'POST':
            return self.handle_login()
        # Handle logouts
        elif path == url_for('logout') and method == 'GET':
            return render_template('logout.html')
        elif path == url_for('logout') and method == 'POST':
            return self.handle_logout()
        return render_template('layout.html')

    def handle_login(self):
        ''' Handles login requests '''
        provider = request.args.get('provider')
        if provider == 'google':
            return self.gconnect()
        elif provider == 'facebook':
            return self.fbconnect()

    def handle_logout(self):
        ''' Handles logout requests '''
        if g.get('user'):
            print(g.user.email)
            if g.user.provider == 'google':
                return self.gdisconnect()
            elif g.user.provider == 'facebook':
                return self.fbdisconnect()
        return redirect(url_for('landing'))

    def gconnect(self):
        ''' Ensures that google authenticated our website user and stores their
        credentials and information in a temporary session.
        '''
        # Get the OAuth2 code and try to retrieve credentials with it
        code = request.data
        try:
            oauth_flow = flow_from_clientsecrets(
                'google_cs.json',
                scope=''
            )
            oauth_flow.redirect_uri = 'postmessage'
            credentials = oauth_flow.step2_exchange(code)
        except FlowExchangeError:
            return self.invalid_response(
                'Failed to upgrade the authorization code',
                status_code=401
            )
        # Check the access token
        access_token = credentials.access_token
        url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={0}'.format(access_token))
        h = httplib2.Http()
        result = json.loads(h.request(url, 'get')[1])
        if result.get('error') is not None:
            return self.invalid_response(
                result.get('error'),
                status_code=500
            )
        # Get the users Google ID and check it against the access token user id
        google_id = credentials.id_token['sub']
        if result['user_id'] != google_id:
            return self.invalid_response(
                'The IDs do not match.',
                status_code=401
            )
        # Get the user's data
        userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        params = {'access_token': credentials.access_token, 'alt': 'json'}
        answer = requests.get(userinfo_url, params=params)
        data = answer.json()
        # Try to use the currently logged in user
        user = g.get('user')
        # If no user is logged in, see if a user exists
        if user is None:
            user = g.db.query(Users).filter_by(email=data['email']).first()
        # If no user exists, create one
        if user is None:
            user = Users(name=data['name'], email=data['email'], provider='google')
            g.db.add(user)
            g.db.commit()
        else:
            user.provider = 'google'
            g.db.add(user)
            g.db.commit()
        # Store the user data in the session
        session['user_id'] = user.id
        session['access_token'] = access_token
        # Notify the user and redirect to the home page
        flash('Successfully logged in as {0}'.format(user.name), "success")
        return redirect(url_for('landing'))

    def gdisconnect(self):
        ''' Disconnect from Google '''
        # Check to make sure there is a connected user
        access_token = session.get('access_token')
        if access_token is None:
            return 'No access token found'
        # Attempt to disconnect
        url = ("https://accounts.google.com/o/oauth2/revoke?token={0}".format(access_token))
        h = httplib2.Http()
        result = h.request(url, 'GET')[0]
        # Verify the result of the request
        if result['status'] == '200':
            # Erase the user's session data
            del session['user_id']
            return redirect(url_for('landing'))
        else:   # There's been a problem disconnecting
            return 'Problem disconnecting'

    def fbconnect(self):
        ''' Connects to Facebook '''
        data = request.get_json()
        if data.get('id'):
            del data['id']
        # Get the user or create a new one
        user = g.db.query(Users).filter_by(email=data['email']).first()
        if user is None:
            user = Users(**data)
            user.provider = 'facebook'
            g.db.add(user)
            g.db.commit()
        else:
            user.provider = 'facebook'
            g.db.add(user)
            g.db.commit()
        # Store the user data in the session
        session['user_id'] = user.id
        return redirect(url_for('landing'))

    def fbdisconnect(self):
        ''' Disconnects from Facebook '''
        if session.get('user_id'):
            del session['user_id']
        return redirect(url_for('landing'))
