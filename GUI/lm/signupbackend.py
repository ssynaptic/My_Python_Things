from sqlite3 import connect
from os.path import (exists,
                     join,
                     isdir,
                     expanduser)
from getpass import getuser

class SignUpBackend:
    def __init__(self):
        pass

    def create_database(self):
        home = self.get_home_path()
        conn = connect(join(home, ".lm.db"))
        conn.commit()
        conn.close()

    def create_users_table(self):
        home = self.get_home_path()
        conn = connect(join(home, ".lm.db"))
        cursor = conn.cursor()
        sql_instruct = """CREATE TABLE users
        (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL);"""
        cursor.execute(sql_instruct)
        conn.commit()
        conn.close()

    def create_user(self, username, password):
        home = self.get_home_path()
        conn = connect(join(home, ".lm.db"))
        cursor = conn.cursor()
        cursor.execute(f"""INSERT INTO users
        (username, password) VALUES
        ('{username}', '{password}');""")
        conn.commit()
        conn.close()

    def check_if_db_exists(self):
        home_path = self.get_home_path()
        db_path = join(home_path, ".lm.db")
        if exists(db_path) and isdir(db_path):
            db_is_valid = "is_invalid"
        if exists(db_path) and not isdir(db_path):
            db_is_valid = "there_is_an_equal"
        if not exists(db_path) and not isdir(db_path):
            db_is_valid = "is_valid"
        return db_is_valid

    def check_db_integrity(self):
        home_path = self.get_home_path()
        db_path = join(home_path, ".lm.db")
        conn = connect(database=db_path,
                       timeout=1)
        cursor = conn.cursor()
        check_instruct = """SELECT NAME FROM
sqlite_schema WHERE type = 'table' AND name NOT LIKE
\"sqlite_%\";"""
        cursor.execute(check_instruct)
        checking = cursor.fetchall()
        if len(checking) == 1 and len(checking[0]) == 1 and checking[0][0] == "users":
            return "is_valid"
        else:
            return "is_invalid"

    def check_if_user_exists(self, username, password):
        home = self.get_home_path()
        conn = connect(join(home, ".lm.db"))
        cursor = conn.cursor()
        cursor.execute(f"""SELECT * FROM users
        WHERE username = '{username}' AND password = '{password}';""")
        data = cursor.fetchall()
        conn.commit()
        conn.close()
        return data

    def get_home_path(self):
        current_user = getuser()
        home_path = expanduser(f"~{current_user}")
        return home_path