from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from . import Base
from .path_part import PathPart


class Categories(Base, PathPart):
    ''' Database schema for categories '''
    __tablename__ = 'categories'
    errors = {}

    # Columns
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    _name = Column(String(250), nullable=False)

    # Relationships
    user = relationship('Users', back_populates='categories')
    items = relationship('Items', back_populates='category')

    def update(self, data):
        ''' Updates the ORM object (self) with the given data

        data - A dict of values to update
        '''
        for key, value in data.iteritems():
            setattr(self, key, value)

    @hybrid_property
    def name(self):
        ''' Retrieves the name of the category '''
        if self._name is not None:
            return self._name
        else:
            return ''

    @name.setter
    def name(self, value):
        ''' Verifies and sets the category name and path '''
        # A name is required
        if value is None or value == '':
            self.errors['name'] = 'A name is required.'
        # A name can only be 250 characters
        elif len(value) > 250:
            self.errors['name'] = 'That name is too long (250 max).'
        # Everything looks good with the name
        else:
            # Delete any associated errors
            if self.errors.get('name'):
                del self.errors['name']
            # Set the name and the path
            self._name = value
            self.path = value
