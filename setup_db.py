#!/usr/bin/env python
''' Configures the database '''

import sys
import os

from db.db import Database

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        try:
            os.remove(Database.DB_DEBUG)
        except:
            print('Debug database not found.')
        db = Database(debugging=True)
        db.setup()
    else:
        db = Database()
        db.setup()
