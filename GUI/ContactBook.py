import tkinter as tk
from tkinter import ttk
from os.path import join, dirname, isfile
from tkinter.colorchooser import askcolor
from tkinter.messagebox import showinfo, showerror
from sqlite3 import connect
from PIL import ImageTk, Image
from customtkinter import CTkEntry, CTkButton, CTkComboBox
from string import ascii_uppercase, ascii_lowercase, punctuation
from re import findall


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

    def create_contact(self, name, number):
        def error(): return showerror(title="Error", message="You Must Provide The Number")
        while True:
            if not number.get():
                error()
                break
            chars = ascii_lowercase + ascii_uppercase + punctuation
            checks = 0
            for char in number.get():
                if char in chars:
                    checks += 1
            if checks >= 1:
                error()
                break
            else:
                conn = connect("contacts.db")
                cursor = conn.cursor()
                instruction = (f"""INSERT INTO PEOPLE (name, number)
                VALUES (\"{name.get()}\", \"{number.get()}\")""")
                cursor.execute(instruction)
                conn.commit()
                conn.close()
                showinfo(title="Success", message="Contact Succesfully Created")
                break
        app.show_contacts()

    def callback(self, event=None):
        contacts = self.get_contacts()
        contact_selected = int(
            findall(r"(\d)\s+-\s+.*", app.contacts_menu.get())[0])
        app.entry_name.delete(0, "end")
        app.entry_number.delete(0, "end")
        for c in contacts:
            if c[0] == contact_selected:
                app.entry_name.insert(0, c[1])
                app.entry_number.insert(0, c[2])

    def update_contact(self):
        while True:
            contact_selected = int(
                findall(r"(\d)\s+-\s+.*", app.contacts_menu.get())[0])
            name = app.entry_name.get()
            number = app.entry_number.get()
            def error(): return showerror(title="Error", message="You Must Provide The Number")
            chars = ascii_lowercase + ascii_uppercase + punctuation
            checks = 0
            if not app.entry_number.get():
                error()
                break
            for char in number:
                if char in chars:
                    checks += 1
            if checks >= 1:
                error()
                break
            else:
                instruction = (f"""UPDATE PEOPLE SET name=\"{app.entry_name.get()}\",
                number={app.entry_number.get()} WHERE id={int(contact_selected)}""")
                conn = connect("contacts.db")
                cursor = conn.cursor()
                cursor.execute(instruction)
                conn.commit()
                conn.close()
                showinfo(title="Success",
                         message="The Contact Has Been Successfully Updated")
                break
        app.show_contacts()

    def delete_contact(self):
        contact = int(findall(r"(\d)\s+-\s+.*", app.delete_menu.get())[0])
#        showinfo(message=contact)
        instruction = (f"DELETE FROM PEOPLE WHERE id={contact}")
        conn = connect("contacts.db")
        cursor = conn.cursor()
        cursor.execute(instruction)
        conn.commit()
        conn.close()
        showinfo(title="Success",
                 message="The Contact Has Been Successfully Deleted")
        app.show_contacts()


class App(tk.Tk):
    def __init__(self):
        self.contact_labels = []
        self.database = Database()
        if not isfile(join(dirname(__file__), "contacts.db")):
            self.database.create_database()
            self.database.create_table()
        super().__init__()
        self.geometry("500x264")
        self.title("Contact Book")
        self.update()
        self.center_window(self, 500, 264)
        self.resizable(0, 0)

        self.config(bg="white", bd=0)

        self.images_folder = join(dirname(__file__), "img")

        self.menu_bar = tk.Menu()

        self.menu_edit = tk.Menu(self.menu_bar, tearoff=False)

        self.color_image = tk.PhotoImage(
            file=join(self.images_folder, "color.png"))

        self.menu_edit.add_command(label="Color",
                                   accelerator="Ctrl+C", command=self.change_color,
                                   image=self.color_image, compound=tk.LEFT)

        self.bind_all("<Control-c>", self.change_color)

        self.menu_bar.add_cascade(menu=self.menu_edit, label="Edit")

        self.config(menu=self.menu_bar)

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Section.TFrame", background="red",
                             borderwidth=2, relief="solid", width=80, height=346)
        self.section_buttons = ttk.Frame(self,
                                         style="Section.TFrame", width=90,
                                         height=260).place(x=2, y=2)

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
                                         style="Update.TButton", command=self.update_contact).place(x=17, y=74)

        self.style.configure("Delete.TButton", background="white",
                             borderwidth=2, relief="solid", padding=6)

        self.delete_contact_image = ImageTk.PhotoImage(Image.open(join(self.images_folder,
                                                                       "delete_contact.png")).resize((42, 42)))

        self.delete_contact = ttk.Button(self, image=self.delete_contact_image,
                                         style="Delete.TButton", command=self.delete_contact).place(x=17, y=140)
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
        for label in self.contact_labels:
            label.destroy()
        if contacts:
            y = 2
            for i in contacts:
                label = ttk.Label(self, text=f"ID : {i[0]} | Name : {i[1]} | Number : {i[2]}",
                                  style="Items.TLabel", width=46)
                label.place(x=96, y=y)
                self.contact_labels.append(label)
                y += 40

    def add_contact(self):
        window = tk.Toplevel()
        window.geometry("300x160")
        window.update()
        self.center_window(window, 300, 200)
        window.resizable(0, 0)
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
                                  anchor="center",
                                  command=lambda: self.database.create_contact(name, number)).pack(padx=10, pady=4)

    def update_contact(self):
        window = tk.Toplevel()
        window.geometry("320x170")
        window.update()
        self.center_window(window, 320, 170)
        window.resizable(0, 0)
        window.title("Update Contact")

        self.style.configure("Indications.TLabel", background="white",
                             foreground="black", borderwidth=2, relief="solid",
                             anchor="center", padding=5)

        indication1 = ttk.Label(window, text="Select A Contact ->",
                                style="Indications.TLabel", width=18).place(x=7, y=7)

        self.combobox_option = tk.StringVar()

        contacts = [i[:2] for i in self.database.get_contacts()]
        contacts = [f"{str(x)} - {str(y)}" for x, y in contacts]
        self.style.configure("MenuContacts.TCombobox", background="white",
                             foreground="black", padding=5, arrowsize=20)
        self.contacts_menu = ttk.Combobox(window,  state="readonly",
                                          values=contacts, justify="left", style="MenuContacts.TCombobox",
                                          width=14)
        if contacts:
            self.contacts_menu.current(0)
        if not contacts:
            self.contacts_menu.set("No Contact")
        self.contacts_menu.place(x=170, y=7)
        self.contacts_menu.bind("<<ComboboxSelected>>",
                                self.database.callback)

        self.entry_name = CTkEntry(window, width=190, height=30,
                                   corner_radius=10, fg_color="white", text_color="black",
                                   placeholder_text_color="gray", placeholder_text="NAME",
                                   font=("Hack", 12), justify="center")
        self.entry_name.place(x=7, y=45)

        self.entry_number = CTkEntry(window, width=180, height=30,
                                     corner_radius=10, fg_color="white", text_color="black",
                                     placeholder_text_color="gray", placeholder_text="NUMBER",
                                     font=("Hack", 12), justify="center")
        self.entry_number.place(x=70, y=80)

        update = CTkButton(window, width=180, height=40,
                           corner_radius=5, border_width=2, border_spacing=2,
                           fg_color="#98F394", hover_color="#0BF000", border_color="red", text_color="black",
                           text="Update", font=("Verdana", 10), state="normal",
                           command=self.database.update_contact, anchor="center")
        update.place(x=70, y=115)

    def delete_contact(self):
        window = tk.Toplevel()
        window.geometry("300x200")
        window.resizable(0, 0)
        window.update()
        self.center_window(window, 300, 200)
        window.title("Delete Contact")

        contacts = [i[:2] for i in self.database.get_contacts()]
        contacts = [f"{str(x)} - {str(y)}" for x, y in contacts]
        self.delete_menu = ttk.Combobox(window, state="readonly", values=contacts,
                                        justify="center", style="MenuContacts.TCombobox", width=14)
        self.delete_menu.place(x=75, y=4)

        if contacts:
            self.delete_menu.current(0)
        if not contacts:
            self.delete_menu.set("No Contact")

        delete = CTkButton(window, width=180, height=40, corner_radius=5,
                           border_width=2, border_spacing=2, fg_color="#E69696", hover_color="#0BF000",
                           border_color="red", text_color="black", text="Delete", font=("Verdana", 10),
                           state="normal", command=self.database.delete_contact)
        delete.place(x=50, y=50)


if __name__ == "__main__":
    app = App()
    app.mainloop()
