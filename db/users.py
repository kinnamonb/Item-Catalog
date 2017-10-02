from sqlalchemy import Column, Integer, Text, String, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Users(Base):
    ''' Database schema for users '''
    __tablename__ = 'users'

    # Columns
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    email = Column(String(250))
    provider = Column(String(250))

    # Relationships
    items = relationship('Items', back_populates='user')
    categories = relationship('Categories', back_populates='user')
