import tkinter as tk
from tkinter import ttk
from customtkinter import (CTk, CTkLabel,
                           CTkButton, CTkToplevel,
                           CTkImage, CTkComboBox,
                           CTkEntry)
from tkinter.colorchooser import askcolor
from tkinter.simpledialog import askstring
from tkinter.messagebox import (showinfo,
                                showerror)
from tkinter.filedialog import asksaveasfile
from os.path import join, dirname
from PIL import ImageTk, Image
from string import punctuation, digits
from sqlite3 import connect


class Database:
    def __init__(self):
        pass
    def save_database(self):
        columns = app.columns.keys()
        types = app.columns.values()
        if not app.db_name:
            showerror(title="Database Error",
                      message="You must especify a name for the database")
            return
        else:
            db_name = f"{app.db_name}.db"      
        table_name = app.table_name
        conn = connect(db_name)
        cursor = conn.cursor()
        instruction = f"""CREATE TABLE {table_name} (rowid INTEGER 
        PRIMARY KEY AUTOINCREMENT);"""
        cursor.execute(instruction)
        for column, type in zip(columns, types):
            i = f"ALTER TABLE {table_name} ADD COLUMN {column} {type};"
            cursor.execute(i)
        conn.commit()
        conn.close()
class App(CTk):
    column_window_open = False
    table_name = "default_name"

    def __init__(self):
        super().__init__()
        self.database = Database()
        self.img_folder = join(dirname(__file__), "img")
        self.title("Database Editor")
        # self.create_database()
        self.geometry("300x20")
        self.resizable(0, 0)
        self.configure(fg_color="#2f2f2f")

        CTkButton(self, width=250, height=40, corner_radius=10,
                  border_width=2, border_spacing=2, fg_color="#5b5b5b",
                  hover_color="#444444", border_color="#6aa84f",
                  text_color="#ffffff", text_color_disabled="#eeeeee",
                  text="Create Or Edit Database", font=("Fira Code Regular", 12),
                  command=self.main).pack(pady=26)
        self.center_window(self, 300, 100)

    def center_window(self, window, width, height):
        window.update()
        swidth = window.winfo_screenwidth()
        sheight = window.winfo_screenheight()

        wwidth = window.winfo_width()
        wheight = window.winfo_height()

        x = ((swidth // 2) - (wwidth // 2))
        y = ((sheight // 2) - (wheight // 2))

        window.geometry(f"{width}x{height}+{x}+{y}")

    def change_color(self, window):
        color = askcolor(initialcolor="#da5d5d",
                         title="Background Color")[1]
        window.config(background=color)

    def quit_app(self):
        self.destroy()

    def add_column_table(self):
        self.not_repeat = False
        while not self.not_repeat:
            if not self.entry.get():
                showerror(title="Error",
                          message="You must enter a name for the column")
                return
            if len(self.columns) > 30:
                showerror(title="Error",
                          message="The column limit has been reached")
                return
            if any(char in punctuation for char in self.entry.get()):
                showerror(title="Error", 
                          message="Can not use special characters in the name")
                self.not_repeat = True
            else:
                self.not_repeat = True
                name = self.entry.get()
                type = self.type_menu.get()

                self.columns.update({name: type})
                self.treeview["columns"] = list(self.columns.keys())
                self.treeview["show"] = "headings"
                self.mainwindow.update()

                self.scrollbar = ttk.Scrollbar(
                    self.mainwindow, orient="horizontal", command=self.treeview.xview)
                self.mainwindow.update()
                x = self.mainwindow.winfo_width()
                y = self.mainwindow.winfo_height()
                self.scrollbar.place(x=5, y=y-14, height=12, width=x-10)
                self.treeview.configure(xscrollcommand=self.scrollbar.set)
                for i in self.columns:
                    self.treeview.column(
                        i, width=200, minwidth=200, stretch=False)
                    self.mainwindow.update()
                    self.treeview.heading(i, text=i)

    def delete_column_table(self):
        if self.delete_menu.get() == "No Columns":
            showerror(title="Error", message="No columns to remove")
            return
        else:
            key = self.delete_menu.get()
            del self.columns[key]
            self.treeview["columns"] = list(self.columns.keys())
            self.treeview["show"] = "headings"
            self.mainwindow.update()

    def destroy_table(self):
        self.treeview["columns"] = []
        self.treeview["show"] = "tree headings"
        self.columns.clear()
        self.mainwindow.update()

    def column_window_closed(self):
        self.column_window_open = False
        self.subwindow.destroy()
        self.mainwindow.focus_set()

    def main(self):
        self.withdraw()
        self.mainwindow = CTkToplevel(fg_color="#444444")
        # self.mainwindow.wm_iconbitmap()
        # self.icon = ImageTk.PhotoImage(file=join(self.img_folder, "icon1.png"))
        # self.mainwindow.iconphoto(False, self.icon)
        self.mainwindow.geometry(f"494x500+50+100")
        self.mainwindow.update()
        self.mainwindow.resizable(0, 0)
        self.mainwindow.title("Create Or Edit Database")
        self.mainwindow.protocol("WM_DELETE_WINDOW", self.quit_app)
        self.mainwindow.update()

        menu_bar = tk.Menu(activebackground="#d0e0e3",
                           activeborderwidth=0,
                           activeforeground="#000000")

        edit_menu = tk.Menu(menu_bar, tearoff=False,
                            activebackground="#d0e0e3",
                            activeborderwidth=0,
                            activeforeground="#000000")

        self.color_img = ImageTk.PhotoImage(
            Image.open(join(self.img_folder, "color.png")))
        self.table_name_img = ImageTk.PhotoImage(
            Image.open(join(self.img_folder, "db_name.png")))
        edit_menu.add_command(label="Color", accelerator="Ctrl+C",
                              command=lambda: self.change_color(self.mainwindow),
                              image=self.color_img,
                              compound=tk.LEFT)
        edit_menu.add_command(label="Table Name", accelerator="Ctrl+N",
                              command=self.set_table_name,
                              image=self.table_name_img,
                              compound=tk.LEFT)
        self.mainwindow.bind_all(sequence="<Control-c>",
                             func=lambda event: self.change_color(self.mainwindow))
        self.mainwindow.bind_all(sequence="<Control-n>",
                             func=lambda event: self.set_table_name())
        menu_bar.add_cascade(menu=edit_menu, label="Edit")

        self.mainwindow.config(menu=menu_bar)

        self.save_image = CTkImage(Image.open(
            join(self.img_folder, "diskette_save.png")), size=(50, 50))
        CTkButton(self.mainwindow, width=60, height=60, corner_radius=0, border_width=2,
                  fg_color="#ffffff", hover_color="#bcbcbc", border_color="#000000",
                  text="", text_color_disabled="#ffffff", image=self.save_image,
                  compound="right", command=self.save_db).place(x=5, y=5)

        self.delete_table_img = CTkImage(Image.open(
            join(self.img_folder, "broken_table.png")), size=(60, 50))
        CTkButton(self.mainwindow, width=60, height=60, corner_radius=0, border_width=2,
                  fg_color="#ffffff", hover_color="#bcbcbc", border_color="#000000",
                  text="", text_color_disabled="#ffffff", image=self.delete_table_img,
                  compound="right", command=self.destroy_table).place(x=75, y=5)

        self.add_column_img = CTkImage(Image.open(
            join(self.img_folder, "add_column.png")), size=(50, 50))
        CTkButton(self.mainwindow, width=60, height=60, corner_radius=0, border_width=2,
                  fg_color="#ffffff", hover_color="#bcbcbc", border_color="#000000",
                  text="", text_color_disabled="#ffffff", image=self.add_column_img,
                  compound="right", command=self.create_columns).place(x=152, y=5)

        self.delete_column_img = CTkImage(Image.open(
            join(self.img_folder, "delete_column.png")), size=(50, 50))
        CTkButton(self.mainwindow, width=60, height=60, corner_radius=0, border_width=2,
                  fg_color="#ffffff", hover_color="#bcbcbc", border_color="#000000",
                  text="", text_color_disabled="#ffffff", image=self.delete_column_img,
                  compound="right", command=self.delete_columns).place(x=220, y=5)

        self.name_label = CTkLabel(self.mainwindow, width=200, height=50, corner_radius=5,
                                   fg_color="#ffffff", font=("Fira Code Semibold", 15), text_color="#000000",
                                   text_color_disabled="#ffffff", text=self.table_name, anchor="center")
        self.name_label.place(x=285, y=10)

        # self.style.configure("Treeview.Treeview")
        self.treeview = ttk.Treeview(self.mainwindow, cursor="hand2", selectmode="browse", padding=6, height=500)
        # self.treeview.configure(rowhe)
        self.treeview["show"] = "tree headings"
        self.treeview.pack(anchor="w", padx=5, pady=80)

        self.columns = {}
        self.center_window(self.mainwindow, 490, 320)
        self.mainwindow.update()
    def create_columns(self):
        if self.column_window_open:
            showinfo(title="Information",
                     message="There is already an active column creation window")
            return
        self.column_window_open = True
        self.subwindow = CTkToplevel(fg_color="#2a2d29")
        self.subwindow.resizable(0, 0)
        self.subwindow.geometry("400x300")

        self.subwindow.protocol("WM_DELETE_WINDOW", self.column_window_closed)

        values = ("NULL", "INTEGER", "REAL", "TEXT", "BLOB")

        self.type_value = tk.StringVar()
        self.style = ttk.Style()
        self.style.configure("Menu.TCombobox", background="#ffffff", foreground="#000000", borderwidth=2,
                             relief="solid", anchor="center", padding=5)
        self.type_menu = ttk.Combobox(self.subwindow, state="readonly", values=values, justify="center",
                                      style="Menu.TCombobox", width=15)
        self.type_menu.current(0)
        self.type_menu.pack(pady=10)
        self.entry = CTkEntry(self.subwindow, width=200, height=20, corner_radius=10, fg_color="#ffffff",
                              text_color="#000000", placeholder_text="COLUMN NAME", font=("Fira Code Retina", 15),
                              justify="center")
        self.entry.pack(pady=17)

        add = CTkButton(self.subwindow, width=200, height=40, corner_radius=5, border_width=2, border_spacing=5,
                        fg_color="#1e4713", hover_color="#45992e", command=self.add_column_table,
                        text="Add Column").pack(pady=25)

    def delete_columns(self):
        subwindow = CTkToplevel(fg_color="#2a2d29")
        subwindow.block_update_dimensions_event()
        subwindow.resizable(0, 0)
        subwindow.geometry("400x300")

        values = list(self.columns.keys())

        self.delete_value = tk.StringVar()
        self.style = ttk.Style()
        self.delete_menu = ttk.Combobox(subwindow, state="readonly", values=values, justify="center",
                                        style="Menu.TCombobox", width=20)
        self.delete_menu.pack(pady=10)
        if len(values) == 0:
            self.delete_menu.set("No Columns")
        else:
            self.delete_menu.current(0)

        delete = CTkButton(subwindow, width=200, height=40, corner_radius=5, border_width=2, border_spacing=5,
                           fg_color="#1e4713", hover_color="#45992e", text="Delete Column",
                           command=self.delete_column_table).pack(pady=25)

    def set_table_name(self):
        string = askstring(title="Table Name",
                           prompt="The name for the table")
        if string:
            if any(char in punctuation for char in string):
                showerror(title="Error", message="Can not use special characters on the name")
                return
            else:
                self.table_name = string
        self.name_label.configure(text=self.table_name)
        self.mainwindow.update()

    def save_db(self):
        self.db_name = askstring(title="DB Name", 
                               prompt="Enter the name of the database")
        if self.db_name:
            if any(char in punctuation for char in self.db_name):
                showerror(title="Database Error", message="Cannot use punctuation characters")
                return
            else:
                self.database.save_database()
        else:
            showinfo(title="Database Error", message="You must provide a name")
            return
if __name__ == "__main__":
    app = App()
    app.mainloop()
