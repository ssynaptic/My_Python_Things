from sqlite3 import connect as sqlite_connect
from sqlite3 import Connection, Cursor

from typing import Any, Dict, Iterable, List, Tuple
from datetime import date

def create_default_tables() -> None:
    conn: Connection = sqlite_connect("database.sqlite3")
    cursor: Cursor = conn.cursor()
    query: str = """
        CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            fname VARCHAR(30), lname VARCHAR(30),
            username VARCHAR(30) NOT NULL, password VARCHAR(128) NOT NULL,
            account_type INTEGER NOT NULL);
    """
    cursor.execute(query)
#     query = """
#         CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#         author_id INTEGER NOT NULL,
#         FOREIGN KEY (author_id) REFERENCES authors (id),
#         title TEXT NOT NULL,
#         isbn TEXT NOT NULL,
#         publish_date VARCHAR(10) NOT NULL
#         );
#     """
    query = """
        CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        author_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        isbn TEXT NOT NULL,
        publish_date VARCHAR(10) NOT NULL,
        FOREIGN KEY (author_id) REFERENCES authors (id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
        );
    """
    cursor.execute(query)
    query = """
        CREATE TABLE IF NOT EXISTS authors (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            fname VARCHAR(50) NOT NULL,
            lname VARCHAR(50) NOT NULL,
            date_of_birth VARCHAR(10) NOT NULL,
            date_of_death VARCHAR(10),
            nationality VARCHAR(15) NOT NULL,
            biography VARCHAR(255));
    """
    cursor.execute(query)
    conn.commit()
    conn.close()

def create_usr_db(uname: str, passwd: str, account_type: int) -> None:
    tbs: bool = check_tables_exist(table_names=("authors", "books", "users"))
    if not tbs:
        print("[!] Tables not found, creating them.")
        create_default_tables()
    if check_user_exist(uname=uname, passwd=passwd):
        print("[-] Username and/or password already in use.")
        exit(1)
    try:
        conn: Connection = sqlite_connect("database.sqlite3")
        cursor: Cursor = conn.cursor()
        query = """
            INSERT INTO users (username, password, account_type)
            VALUES (?, ?, ?);
        """
        params = (uname, passwd, account_type)
        cursor.execute(query, params)
        conn.commit()
    except Exception as e:
        print("[-] Error: {e}")
    finally:
        conn.close()

def create_author_db(fname: str, lname: str, dt_of_bth: date,
                     nationality: str, dt_of_dth: date = None, 
                     biography: str = None) -> None:
    try:
        conn: Connection = sqlite_connect("database.sqlite3")
        cursor: Cursor = conn.cursor()
        
        sql_query: str = """INSERT INTO authors (fname, lname,
            date_of_birth, date_of_death, nationality, biography)
            VALUES (?, ?, ?, ?, ?, ?)"""
        params: Tuple[str] = (fname, lname, dt_of_bth,
                              dt_of_dth, nationality,
                              biography)
        cursor.execute(sql_query, params)
        conn.commit()
    except Exception as e:
        print("[-] An unexpected error has ocurred.")
    finally:
        conn.close()

def check_tables_exist(table_names: Tuple[str]):
    try:
        conn: Connection = sqlite_connect("database.sqlite3")
        cursor: Cursor = conn.cursor()

        # Dinamically build the query
        sql_query = "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name IN ("
        sql_query += ",".join(["?" for _ in table_names])
        sql_query += ")"

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
    # Return all the users and his passwords
    if all_users:
        try:
            conn: Connection = sqlite_connect("database.sqlite3")
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
            conn: Connection = sqlite_connect("database.sqlite3")
            cursor: Cursor = conn.cursor()
            query: str = "SELECT username, password FROM users WHERE username = ? "
            # Verify username and password for login authentication
            if all_credentials:
                query = query + "AND password  = ?;"
            # Check if any user already exists with the
            # username and/or password provided
            else:
                query = query + "OR password  = ?;"
            params: Tuple[str, str] = (uname, passwd)
            cursor.execute(query, params)
            result = cursor.fetchone()
            return True if result else False
        except Exception as e:
            print(f"[-] Error: {e}, try signing up")
            return False
        finally:
            conn.close()
def get_user_info(uname: str, passwd_hash: str):
    try:
        conn: Connection = sqlite_connect("database.sqlite3")
        cursor: Cursor = conn.cursor()
        query: str = """
            SELECT * FROM users WHERE
            username = ? AND password = ?;
        """
        params: Tuple[str] = (uname, passwd_hash)
        cursor.execute(query, params)
        result: Tuple[Any] = cursor.fetchone()
        if result:
            return result
        else:
            return False
    except Exception as e:
        print("[!] An unexpected error has ocurred.", e)
    finally:
        conn.close()
