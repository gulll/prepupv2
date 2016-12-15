import os
import MySQLdb
import traceback

class PreLocal(object):

    def __init__(self):
        self.database = os.environ.get("DB_NAME", None)
        self.host = os.environ.get("DB_HOST", None)
        self.user = os.environ.get("DB_USER", None)
        self.password = os.environ.get("DB_PASSWORD", None)


    def connect(self):
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

