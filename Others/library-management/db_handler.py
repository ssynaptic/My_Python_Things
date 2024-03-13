from sqlite3 import connect as sqlite_connect
from sqlite3 import Connection, Cursor

from typing import Any, Iterable, List

def list_tables() -> List[str]:
    conn: Connection = sqlite_connect("db.sqlite3")
    cursor: Cursor = conn.cursor()
    stmt: str  = "SELECT name FROM sqlite_schema WHERE  type ='table' AND name NOT LIKE 'sqlite_%';"
    cursor.execute(stmt)
    result: List[str] = cursor.fetchall()
    if result:
        return f"{result[0][0]}-{result[1][0]}"
    else:
        return "NO-TABLES"

def create_default_tables() -> None:
    conn: Connection = sqlite_connect("db.sqlite3")
    cursor: Cursor = conn.cursor()
    stmt: str = """
        CREATE TABLE IF NOT EXISTS users ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            'fname' VARCHAR(30), 'lname' VARCHAR(30),
            'username' VARCHAR(30) NOT NULL, 'password' VARCHAR(128) NOT NULL,
            'is_staff' INTEGER NOT NULL);
    """
    cursor.execute(stmt)
    stmt = """
        CREATE TABLE IF NOT EXISTS 'books' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            'author' VARCHAR(50) NOT NULL, title VARCHAR (100) NOT NULL);
    """
    cursor.execute(stmt)
    conn.commit()
    conn.close()

def write_record(table: str, data: Iterable[Any]) -> None:
    tables: str = list_tables()
    if not "users-books" in tables:
        print("[!] Tables not found, creating them.")
        create_default_tables()
    match table:
        case "users":
            conn: Connection = sqlite_connect("db.sqlite3")
            cursor: Cursor = conn.cursor()
            cursor.execute(f"""
                INSERT INTO 'users' ('username', 'password', 'is_staff')
                VALUES ('{data[0]}', '{data[1]}', '{str(data[2])}');
            """)
            conn.commit()
            conn.close()
        case "books":
            pass
def get_records(table: str, data: Iterable[Any]) -> None:
    match table:
        case "users":
            # breakpoint()
            conn: Connection = sqlite_connect("db.sqlite3")
            cursor: Cursor = conn.cursor()
            uname = data[0]
            passwd = data[1]
            cursor.execute(f"""
                SELECT username, password FROM users
                WHERE username = '{uname}' AND password = '{passwd}';
            """)
            data = cursor.fetchall()
            conn.close()
            return data
        case "books":
            pass
