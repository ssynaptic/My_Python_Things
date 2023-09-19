from os.path import (exists,
                     isdir,
                     join,
                     dirname)
from sqlite3 import (connect,
                     OperationalError)
from time import sleep

class Database:
    def __init__(self):
        pass
    def check_db_name(self, db_name):
        db_path = join(dirname(__file__), db_name)
        db_is_valid = False
        if exists(db_path) and isdir(db_path):
            db_is_valid = "is_invalid"
        if exists(db_path) and not isdir(db_path):
            db_is_valid = "there_is_an_equal"
        if not exists(db_path) and not isdir(db_path):
            db_is_valid = "is_valid"

        return db_is_valid

    def create_database(self, db_name):
            conn = connect(database=db_name,
                           timeout=1)
            conn.commit()
            conn.close()

    # def delete_database(self, db_name):
    #     db_path = join(dirname(__file__), db_name)
    #     if exists(db_path) and isdir(db_path):
    #         remove(db_path)

    def create_main_table(self, db_name):
        conn = connect(database=db_name,
                       timeout=1)
        cursor = conn.cursor()
        table_instruction = """CREATE TABLE 'passwords'
(id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT NOT NULL,
password TEXT NOT NULL);"""
        cursor.execute(table_instruction)
        conn.commit()
        conn.close()

    def create_record(self, db_name, username, password):
        conn = connect(database=db_name,
                       timeout=1)
        cursor = conn.cursor()
        record_instruction = f"""INSERT INTO passwords (username, password)
VALUES ('{username}', '{password}')"""
        cursor.execute(record_instruction)
        conn.commit()
        conn.close()

    def delete_record(self, db_name, record_id):
        conn = connect(database=db_name,
                       timeout=1)
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM passwords WHERE id = {record_id}")
        conn.commit()
        conn.close()

    def get_data_from_db(self, db_name):
        conn = connect(database=db_name,
                       timeout=1)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM passwords;")
        data = cursor.fetchall()
        conn.commit()
        conn.close()
        return data

    def get_ids_from_db(self, db_name):
        conn = connect(database=db_name,
                       timeout=1)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM passwords;")
        data = cursor.fetchall()
        conn.commit()
        conn.close()
        return data

    def check_db_integrity(self, db_name):
        #self.conn = connect(database=db_name + ".sqlite3",
        #                    timeout=1)
        conn = connect(database=db_name,
                       timeout=1)
        cursor = conn.cursor()
        checking_instruction = """SELECT NAME FROM
sqlite_schema WHERE type = \"table\" AND name NOT LIKE
\"sqlite_%\";"""
        checking = cursor.execute(checking_instruction).fetchall()
        #if self.checking_results:
        if len(checking) == 1 and len(checking[0]) == 1 and checking[0][0] == "passwords":
            # return self.checking_results.fetchall()
            return "is_valid"
        else:
            return "is_invalid"