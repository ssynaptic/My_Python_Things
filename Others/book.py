from sqlite3 import connect
from os.path import dirname, join, isfile

class App:
    def __init__(self):
        print("Welcome To The Contact Book\n")
    def create_db(self):
        conn = connect("contacts.db")
        conn.commit()
        conn.close()
    def create_table(self):
        conn = connect("contacts.db")
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE PEOPLE (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT (15),
            last_name TEXT (15),
            number TEXT (15)
        );""")
        conn.commit()
        conn.close()
    def create_contact(self):
        data = {"name": None, "lname": None,
        "number": None}
        for i in data.keys():
            data[i] = input(f"Enter The {i}: ")
        conn = connect("contacts.db")
        cursor = conn.cursor()
        cursor.execute(f"""INSERT INTO 
        PEOPLE (name, last_name, number) 
        VALUES ('{data["name"]}',
        '{data["lname"]}', '{data["number"]}')""")
        conn.close()
if __name__ == ("__main__"):
    app = App()
    if not isfile(join(dirname(__file__), "contacts.db")):
        app.create_db()
        app.create_table()
    while True:
        menu = ("""Select An Option:
1- Create Contact
2- See Contact
3- Update Contact
4- Delete Contact
5- Exit\n""")
        print(menu)
        election = int(input("Your Option: "))
        match election:
            case 1:
                app.create_contact()
            case _:
                print("Invalid Option")
