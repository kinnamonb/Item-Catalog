from flask.views import View


class AuthView(View):
    ''' Handles authentication requests '''
    methods = ['GET', 'POST']

    def dispatch_request(self):
        return 'Auth stuff'
