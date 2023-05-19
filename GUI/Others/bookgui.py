import tkinter as tk
from tkinter import ttk
from os.path import join, dirname, isfile
from tkinter.colorchooser import askcolor
from tkinter.messagebox import showinfo, showerror
from sqlite3 import connect
from PIL import ImageTk, Image
from customtkinter import CTkEntry, CTkButton

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
    def get_contacts(self):
    	conn = connect("contacts.db")
    	cursor = conn.cursor()
    	cursor.execute("""SELECT *
    	FROM PEOPLE""")
    	return cursor.fetchall()
    	conn.commit()
    	conn.close()

    def create_contact(self, name=None, number=None):
        error = lambda : showerror(title="Error", message="You Must Provide The Two Required Fields")
        if not str(name.get()):
            error()
        if not str(number.get()):
            error()
        conn = connect("contacts.db")
        cursor = conn.cursor()
        instruction = (f"""INSERT INTO PEOPLE (name, number)
                           VALUES (\"{name.get()}\", \"{number.get()}\")""")
        cursor.execute(instruction)
        conn.commit()
        conn.close()

        showinfo(title="Succes", message="Contact Succesfully Created")
class App(tk.Tk):
    def __init__(self):
        self.database = Database()
        if not isfile(join(dirname(__file__), "contacts.db")):
            self.database.create_database()
            self.database.create_table()
        super().__init__()
        self.geometry("500x400")
        self.title("Contact Book")
        self.update()
        self.center_window(self, 500, 400)
        self.resizable(False, False)

        self.config(bg="white", bd=0)

        self.images_folder = join(dirname(__file__), "img")
        
        self.menu_bar = tk.Menu()

        self.menu_edit =  tk.Menu(self.menu_bar, tearoff=False)

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
        style="Section.TFrame", width=90, 
        height=395).place(x=2, y=2)

        self.style.configure("Add.TButton", background="white",
        borderwidth=2, relief="solid", padding=2)

        self.add_contact_image = ImageTk.PhotoImage(Image.open(join(self.images_folder, 
        "add_contact.png")).resize((50, 50)))

        self.add_button = ttk.Button(self, image=self.add_contact_image, 
        style="Add.TButton", command=self.add_contact).place(x=17, y=8)

        self.style.configure("Update.TButton", background="white",
        borderwidth=2, relief="solid", padding=10)

        self.update_contact_image = ImageTk.PhotoImage(Image.open(join(self.images_folder, 
        "update_contact.png")).resize((34, 34)))

        self.update_contact = ttk.Button(self, image=self.update_contact_image,
        style="Update.TButton").place(x=17, y=74)

        self.style.configure("Delete.TButton", background="white", 
        borderwidth=2, relief="solid", padding=6)

        self.delete_contact_image = ImageTk.PhotoImage(Image.open(join(self.images_folder, 
        "delete_contact.png")).resize((42, 42)))

        self.delete_contact = ttk.Button(self, image=self.delete_contact_image,
        style="Delete.TButton").place(x=17, y=140)
        
        self.show_contacts()

    def center_window(self, window=None, width=None, height=None):
        window.geometry(f"{width}x{height}")
        window.update()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = int((screen_width / 2) - (window.winfo_width() / 2))
        y = int((screen_height / 2) - (window.winfo_height() / 2) - 30)

        window.geometry(f"{width}x{height}+{x}+{y}")

    def change_color(self, event=None):
        color = askcolor(title="Background Color")    
        self.config(bg=color[1])
        
    def show_contacts(self):
    	contacts = self.database.get_contacts()
    	style = ttk.Style()
    	self.style.configure("Items.TLabel", background="white",
    	foreground="black", borderwidth=2, relief="solid",
    	padding=6)
    	if contacts:
    		y = 2
    		for i in contacts:
    		    show = ttk.Label(self, text=f"ID : {i[0]} | Name : {i[1]} | Number : {i[2]}",
    			style="Items.TLabel", width=46).place(x=96, y=y)
    		    y += 40
    		    
    def add_contact(self):
        window = tk.Toplevel()
        window.geometry("300x160")
        window.update()
        self.center_window(window, 300, 200)
        window.resizable(False, False)
        window.title("Add Contact")

        self.style.configure("Indications.TLabel", background="white", 
        foreground="black", borderwidth=2, relief="solid", anchor="center")

        indication1 = ttk.Label(window, text="Name", style="Indications.TLabel",
        width=10).pack(padx=20, pady=5)
        
        name = CTkEntry(window, placeholder_text="Ex: Elliot Alderson", 
        width=140, height=25, border_width=2, corner_radius=10, 
        justify="center", font=("Hack", 12), text_color="red")

        name.pack(padx=10, pady=4)
        
        indication2 = ttk.Label(window, text="Number", style="Indications.TLabel",
        width=10).pack(padx=20, pady=5)
        
        number = CTkEntry(window, placeholder_text="Ex: +16785736408", width=140, height=25,
        border_width=2, corner_radius=10, justify="center", font=("Hack", 12),
        text_color="red")

        number.pack(padx=10, pady=4)

        create_button = CTkButton(window, text="Create Contact", font=("Hack", 12),
        width=90, height=25, corner_radius=10, border_width=2, fg_color="white", 
        hover_color="#F0EAE9", border_color="red", text_color="black", 
        anchor="center", command=lambda : self.database.create_contact(name, 
        number)).pack(padx=10, pady=4)
if __name__ == ("__main__"):
    app = App()
    app.mainloop()
