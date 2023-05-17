from sqlite3 import connect
from os.path import dirname, join, isfile
from string import ascii_lowercase, ascii_uppercase

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
            number TEXT (15)
        );""")
        conn.commit()
        conn.close()
    def create_contact(self):
        data = {"name": None, "number": None}
        for i in data.keys():
            data[i] = input(f"Enter The {i}: ")
        conn = connect("contacts.db")
        cursor = conn.cursor()
        instruction = (f"""INSERT INTO PEOPLE 
(name, number) VALUES
('{data["name"]}', '{data["number"]}')""")
        cursor.execute(instruction)
        conn.commit()
        conn.close()
    def see_contacts(self):
        conn = connect("contacts.db")
        cursor = conn.cursor()
        cursor.execute("""SELECT id, name, number 
FROM PEOPLE""")
        for i in cursor.fetchall():
            print(f"{i[0]} - {i[1]}: {i[2]}")
        conn.commit()
        conn.close()
    def update_contact(self):
        self.see_contacts()
        contact = int(input("Select A Contact Entering His ID Number: "))
        conn = connect("contacts.db")
        cursor = conn.cursor()
        cursor.execute(f"""SELECT id FROM PEOPLE 
        WHERE id={contact};""")
        if cursor.fetchall():
            menu = ("""Select An Option
1- Name
2- Number\n""")
            election = int(input(menu))
            match election:
                case 1:
                    arg = input("Enter The Name: ")
                    instruction = (f"""UPDATE PEOPLE 
                    SET name="{arg}" WHERE id={contact}""")
                    cursor.execute(instruction)
                case 2:
                    arg = input("Enter The Number: ")
                    instruction = (f"""UPDATE PEOPLE
                    SET number="{arg}" WHERE id={contact}""")
                    cursor.execute(instruction)
                case _:
                    print("Enter A Valid Option")
        conn.commit()
        conn.close()
if __name__ == ("__main__"):
    app = App()
    if not isfile(join(dirname(__file__), "contacts.db")):
        app.create_db()
        app.create_table()
    while True:
        menu = ("""Select An Option:
1- Create Contact
2- See Contacts
3- Update Contact
4- Delete Contact
5- Exit\n""")
        print(menu)
        election = int(input("Your Option: "))
        match election:
            case 1:
                app.create_contact()
            case 2:
                app.see_contacts()
            case 3:
                app.update_contact()
            case 5:
                exit(0)
            case _:
                print("Please Select A Valid Option\n")
