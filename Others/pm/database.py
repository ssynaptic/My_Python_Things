from os.path import (exists,
                     isdir,
                     join,
                     dirname)
from sqlite3 import connect
# from signal import (signal,
#                     SIGINT)

class Database:
    def __init__(self):
        pass
    def check_db_name(self, db_name):
        self.db_path = join(dirname(__file__), f"{db_name}.sqlite3")
        self.db_is_valid = False
        if exists(self.db_path) and isdir(self.db_path):
            self.db_is_valid = "is_valid"
        if exists(self.db_path) and not isdir(self.db_path):
            self.db_is_valid = "there_is_an_equal"
        if not exists(self.db_path) and not isdir(self.db_path):
            self.db_is_valid = "is_valid"

        return self.db_is_valid
#        if exists(self.db_path):
#            self.db_is_valid = False
#            if isdir(self.db_path):
#                self.db_is_valid = True
#            else:
#                self.db_is_valid = False
#                return self.db_is_valid
#        else:
#            self.db_is_valid = True
#            return self.db_is_valid

    def create_database(self, db_name):
        self.conn = connect(database=db_name + ".sqlite3",
                            timeout=1)
        self.cursor = self.conn.cursor()
        self.conn.commit()
        self.conn.close()

    def create_main_table(self, db_name):
        self.conn = connect(database=db_name + ".sqlite3",
                            timeout=1)
        self.cursor = self.conn.cursor()
        self.table_instruction = """CREATE TABLE 'passwords'
(id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT NOT NULL,
password TEXT NOT NULL);"""
        self.cursor.execute(self.table_instruction)
        self.conn.commit()
        self.conn.close()

    def create_record(self, db_name, username, password):
        self.conn = connect(database=db_name + ".sqlite3",
                            timeout=1)
        self.cursor = self.conn.cursor()
        self.record_instruction = """INSERT INTO passwords (username, password)
VALUES (\"{username}\", \"{password}\")"""
        self.cursor.execute(self.record_instruction)
        self.conn.commit()
        self.conn.close()

    def check_db_integrity(self, db_name):
        self.conn = connect(database=db_name + ".sqlite3",
                            timeout=1)
        self.cursor = self.conn.cursor()
        self.checking_instruction = """SELECT NAME FROM
sqlite_schema WHERE type = \"table\" AND name NOT LIKE
\"sqlite_%\";"""
        self.checking = self.cursor.execute(self.checking_instruction)
        #if self.checking_results:
        if len(self.checking) = 1 and len(self.checking)
        return self.checking_results.fetchall()