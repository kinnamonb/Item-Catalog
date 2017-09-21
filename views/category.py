from flask.views import View


class CategoryView(View):
    ''' Handles /, /c/, and /c/<c_path>/ requests '''
    methods = ['GET', 'POST']

    def dispatch_request(self, c_path):
        return 'Category stuff {0}'.format(c_path)
