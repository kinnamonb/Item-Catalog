from .db_view import DatabaseView


class ItemView(DatabaseView):
    ''' Handles Item requests '''
    methods = ['GET', 'POST']

    def dispatch_request(self, c_path, i_path):
        return 'Item stuff {0}'.format(i_path)
