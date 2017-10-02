import string
import re

from sqlalchemy import Column, String
from sqlalchemy.ext.hybrid import hybrid_property
from flask import g


class PathPart():
    ''' Handles generating paths for the subclasses '''
    path_chars = string.ascii_lowercase + string.digits + '-'

    _path = Column(String(32))

    @hybrid_property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = self.generate_path(value)

    def generate_path(self, value):
        ''' Generates a path from the given value '''
        # Convert the value to a path
        p = value.lower().replace(' ', '-')
        regex = re.compile('[^{0}]'.format(self.path_chars))
        p = regex.sub('', p)[:16]
        # Get the object with the same path, if one exists
        c = g.db.query(type(self)).filter_by(path=value).first()
        # If it exists, append a number to the end of the path
        if c:
            path_count = g.db.query(type(self))\
                             .filter(path.like(p + '%'))\
                             .count()
            p = '{0}-{1}'.format(p, path_count)
        return p
