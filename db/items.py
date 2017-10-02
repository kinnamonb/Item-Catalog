from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from . import Base
from .path_part import PathPart
from .updatable import Updatable


class Items(Base, PathPart, Updatable):
    ''' Database schema for Items '''
    __tablename__ = 'items'
    errors = {}

    # Columns
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    notes = Column(Text)
    image = Column(Text)

    # Relationships
    user = relationship('Users', back_populates='items')
    category = relationship('Categories', back_populates='items')

    def __init__(self, **kwargs):
        super(Items, self).__init__(**kwargs)
        self.notes = ''
        self.image = ''
