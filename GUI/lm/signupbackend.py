from sqlite3 import connect

class SignUpBackend:
    def __init__(self):
        pass

    def create_database(self):
        conn = connect("lm.db")
        conn.commit()
        conn.close()

    def create_users_table(self):
        conn = connect("lm.db")
        cursor = conn.cursor()
        sql_instruct = """CREATE TABLE users
        (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL);"""
        cursor.execute(sql_instruct)
        conn.commit()
        conn.close()

    def create_user(self, username, password):
        conn = connect("lm.db")
        cursor = conn.cursor()
        cursor.execute(f"""INSERT INTO users
        (username, password) VALUES
        ('{username}', '{password}');""")
        conn.commit()
        conn.close()

    def check_if_user_exists(self, username, password):
        conn = connect("lm.db")
        cursor = conn.cursor()
        cursor.execute(f"""SELECT * FROM users
        WHERE username = '{username}' AND password = '{password}';""")
        data = cursor.fetchall()
        conn.commit()
        conn.close()
        return data