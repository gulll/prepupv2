import os
import MySQLdb
import traceback
from config import prepup_data

class PreLocal(object):

    def __init__(self):
        prepup = prepup_data()
        self.database = prepup.dbName
        self.host = prepup.host
        self.user = prepup.user
        self.password = prepup.password


    def connect(self):
        print self.host,self.user,self.password, self.database
        db = MySQLdb.connect(self.host,self.user,self.password, self.database)
        cursor = db.cursor()
        return db, cursor

    def execute_query(self, _sql, _type):
        _db, _cursor = self.connect()
        try:
            # print(_sql.format(*args))
            # cursor.execute(_sql.format(*args))
            _cursor.execute(_sql)
            if _type.upper() == 'SELECT':
                return self.get_data(_db, _cursor)
            elif _type.upper().upper() == 'UPDATE':
                return self.update_data(_db, _cursor)
            elif _type.upper().upper() == 'INSERT':
                return self.update_data(_db, _cursor)
        except Exception as e:
            traceback.print_exc()
            return e.message
        _db.close()

    def get_data(self, db, cursor):
        results = cursor.fetchall()
        return results

    def update_data(self, db, cursor):
        try:
            db.commit()
            return 1
        except:
            db.rollback()
            return 0

