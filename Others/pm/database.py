from os.path import (exists,
                     isdir,
                     join,
                     dirname)
from sqlite3 import connect

class Database:
    def __init__(self):
        pass
    def check_db_name(self, db_name):
        self.db_path = join(dirname(__file__), f"{db_name}.sqlite3")
        self.db_is_valid = False
        if exists(self.db_path):
            self.db_is_valid = False
            if isdir(self.db_path):
                self.db_is_valid = True
            else:
                self.db_is_valid = False
                return False
        else:
            return True
    
    def create_database(self, db_name):
        self.conn = connect(database=f"{db_name}.sqlite3",
                            timeout=5)
        self.cursor = self.conn.cursor()
        self.conn.commit()
        self.conn.close()