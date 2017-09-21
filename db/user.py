from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Users(Base):
    ''' Database schema for users '''
    __tablename__ = 'users'

    # Columns
    id = Column(Integer, primary_key=True)
    name = Column(Text)
