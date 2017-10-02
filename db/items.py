from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Items(Base):
    ''' Database schema for Items '''
    __tablename__ = 'items'

    # Columns
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    path = Column(String(16), nullable=False)
    name = Column(String(250), nullable=False)
    notes = Column(Text)
    image = Column(Text)

    # Relationships
    user = relationship('Users', back_populates='items')
    category = relationship('Categories', back_populates='items')
