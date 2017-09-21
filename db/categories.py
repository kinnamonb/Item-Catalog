from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Categories(Base):
    ''' Database schema for categories '''
    __tablename__ == 'categories'

    # Columns
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    path = Column(String(16), nullable=False)
    name = Column(String(250), nullable=False)

    # Relationships
    user = relationship('Users', back_populates('categories'))
    items = relationship('Items', back_populates('category'))
