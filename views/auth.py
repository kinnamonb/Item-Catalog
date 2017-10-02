from .db_view import DatabaseView


class AuthView(DatabaseView):
    ''' Handles authentication requests '''
    methods = ['GET', 'POST']

    def dispatch_request(self):
        return 'Auth stuff'
