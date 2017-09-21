from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from . import Base


class Database():
    ''' An interface to the database '''
    DB_PREFIX = 'sqlite:///'
    DB_DEBUG = 'db/debug.db'
    DB_PROD = 'db/db.db'

    def __init__(self, debugging=False):
        ''' Initializes the database session '''
        if debugging:
            self.engine = create_engine(self.DB_PREFIX + self.DB_DEBUG)
        else:
            self.engine = create_engine(self.DB_PREFIX + self.DB_PROD)
        Base.metadata.bind = self.engine
        self.session = sessionmaker(bind=self.engine)()

    def setup(self):
        ''' Creates the database tables and configures the initial roles '''
        Base.metadata.create_all(self.engine)

    def query(self, table):
        ''' Retrieves the database session '''
        return self.session.query(table)

    def add(self, obj):
        ''' Adds/updates a database record '''
        return self.session.add(obj)

    def commit(self):
        ''' Commits any pending database transactions '''
        return self.session.commit()
