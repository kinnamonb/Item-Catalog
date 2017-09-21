#!/usr/bin/env python
''' Configures the database '''

import sys

from db.db import Database

if sys.argv[1] == 'debug':
    db = Database(debugging=True)
    db.setup()
else:
    db = Database()
    db.setup()
