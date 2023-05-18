import tkinter as tk
from tkinter import ttk
from os.path import join, dirname, isfile
from tkinter.colorchooser import askcolor
from sqlite3 import connect
from PIL import ImageTk, Image

class Database:
    def __init__(self):
        pass
    def create_database(self):
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
        )""")
class App(tk.Tk):
    def __init__(self):
        self.database = Database()
        if not isfile(join(dirname(__file__), "contacts.db")):
            self.database.create_database()
            self.database.create_table()
        super().__init__()
        self.title("Contact Book")
        self.geometry("400x350+200+150")
        self.resizable(False, False)
        self.config(bg="spring green", bd=0)

        self.menu_bar = tk.Menu()

        self.menu_edit =  tk.Menu(self.menu_bar, tearoff=False)

        self.images_folder = join(dirname(__file__), "img")

        self.color_image  = tk.PhotoImage(file=join(self.images_folder, "color.png"))
        
        self.menu_edit.add_command(label="Color", 
        accelerator="Ctrl+C", command=self.change_color,
        image=self.color_image, compound=tk.LEFT)

        self.bind_all("<Control-c>", self.change_color)

        self.menu_bar.add_cascade(menu=self.menu_edit, label="Edit")

        self.config(menu=self.menu_bar)

        self.style = ttk.Style()
        self.style.configure("Section.TFrame", background="red",
        borderwidth=2, relief="solid", width=80, height=346)
        self.section_buttons = ttk.Frame(self, 
        style="Section.TFrame", width=80, 
        height=346).place(x=2, y=2)

        self.style.configure("Add.TButton", background="white",
        borderwidth=2, relief="solid", padding=2)

        self.add_contact_image = ImageTk.PhotoImage(Image.open(join(self.images_folder, 
        "add_contact.png")).resize((50, 50)))

        self.add_button = ttk.Button(self, image=self.add_contact_image, 
        style="Add.TButton").place(x=12, y=8)

        self.style.configure("Update.TButton", background="white",
        borderwidth=2, relief="solid", padding=10)

        self.update_contact_image = ImageTk.PhotoImage(Image.open(join(self.images_folder, 
        "update_contact.png")).resize((34, 34)))

        self.update_contact = ttk.Button(self, image=self.update_contact_image,
        style="Update.TButton").place(x=12, y=74)

        self.style.configure("Delete.TButton", background="white", 
        borderwidth=2, relief="solid", padding=6)

        self.delete_contact_image = ImageTk.PhotoImage(Image.open(join(self.images_folder, 
        "delete_contact.png")).resize((42, 42)))

        self.delete_contact = ttk.Button(self, image=self.delete_contact_image,
        style="Delete.TButton").place(x=12, y=140)

    def change_color(self, event=None):
        color = askcolor(title="Background Color")    
        self.config(bg=color[1])

if __name__ == ("__main__"):
    app = App()
    app.mainloop()
