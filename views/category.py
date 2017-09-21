from flask.views import View


class CategoryView(View):
    ''' Handles Category requests '''
    methods = ['GET', 'POST']

    def dispatch_request(self, c_path):
        return 'Category stuff {0}'.format(c_path)
