from flask.views import View


class AuthView(View):
    ''' Handles /, /c/, and /c/<c_path>/ requests '''
    methods = ['GET', 'POST']

    def dispatch_request(self):
        return 'Auth stuff'
