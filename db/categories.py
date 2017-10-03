from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from . import Base
from .path_part import PathPart
from .updatable import Updatable


class Categories(Base, PathPart, Updatable):
    ''' Database schema for categories '''
    __tablename__ = 'categories'
    errors = {}

    # Columns
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    # Relationships
    user = relationship('Users', back_populates='categories')
    items = relationship('Items', back_populates='category')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }
