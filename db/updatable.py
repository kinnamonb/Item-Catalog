class Updatable():
    ''' Adds the ability to update itself based upon a given dictioanry '''

    def update(self, data):
        ''' Updates the ORM object (self) with the given data

        data - A dict of values to update
        '''
        for key, value in data.iteritems():
            setattr(self, key, value)
