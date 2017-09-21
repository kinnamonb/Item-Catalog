from flask.views import View


class ItemView(View):
    ''' Handles Item requests '''
    methods = ['GET', 'POST']

    def dispatch_request(self, c_path, i_path):
        return 'Item stuff {0}'.format(i_path)
