from sqlite3 import connect as sqlite_connect
from sqlite3 import Connection, Cursor

from typing import Any, Dict, Iterable, List, Tuple

def create_default_tables() -> None:
    conn: Connection = sqlite_connect("db.sqlite3")
    cursor: Cursor = conn.cursor()
    query: str = """
        CREATE TABLE IF NOT EXISTS users ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            'fname' VARCHAR(30), 'lname' VARCHAR(30),
            'username' VARCHAR(30) NOT NULL, 'password' VARCHAR(128) NOT NULL,
            'is_staff' INTEGER NOT NULL);
    """
    cursor.execute(query)
    query = """
        CREATE TABLE IF NOT EXISTS 'books' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            'author' VARCHAR(50) NOT NULL, title VARCHAR (100) NOT NULL);
    """
    cursor.execute(query)
    conn.commit()
    conn.close()

def create_usr_db(uname: str, passwd: str, is_staff: int) -> None:
    tbs: bool = check_tables_exist(table_names=("users", "books"))
    if not tbs:
        print("[!] Tables not found, creating them.")
        create_default_tables()
    if check_user_exist(uname=uname, passwd=passwd):
        print("[-] Username and/or password already in use.")
        exit(1)
    try:
        conn: Connection = sqlite_connect("db.sqlite3")
        cursor: Cursor = conn.cursor()
        query = """
            INSERT INTO 'users' ('username', 'password', 'is_staff')
            VALUES (?, ?, ?);
        """
        params = (uname, passwd, is_staff)
        cursor.execute(query, params)
        conn.commit()
    except Exception as e:
        print("[-] Error: {e}")
    finally:
        conn.close()

def check_tables_exist(table_names: List[str]) -> bool:
    try:
        conn: Connection = sqlite_connect("db.sqlite3")
        cursor: Cursor = conn.cursor()

        sql_query = "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name IN (" + ",".join(["?" for _ in table_names]) + ")"
        
        cursor.execute(sql_query, table_names)
        result = cursor.fetchone()
   
        return result[0] == len(table_names)
    
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conn.close()

def check_user_exist(uname: str, passwd: str, all_credentials: bool = False,
                        all_users: bool = False) -> Dict[str, str] | bool:
    if all_users:
        try:
            conn: Connection = sqlite_connect("db.sqlite3")
            cursor: Cursor = conn.cursor()
            query: str = """
                SELECT username, password FROM users;
            """
            cursor.execute(query)
            result = {u: p for u, p in cursor.fetchall()}
            return result if result else False
        except Exception as e:
            print(f"[-] Error: {e}")
            return False
        finally:
            conn.close()
    else:
        try:
            conn: Connection = sqlite_connect("db.sqlite3")
            cursor: Cursor = conn.cursor()
            query: str = "SELECT username, password FROM users WHERE username = ? "
            if all_credentials:
                query = query + "AND password  = ?;"
            else:
                query = query + "OR password  = ?;"
            params: Tuple[str, str] = (uname, passwd)
            cursor.execute(query, params)
            result = cursor.fetchone()
            return True if result else False
        except Exception as e:
            print(f"[-] Error: {e}")
            return False
        finally:
            conn.close()
