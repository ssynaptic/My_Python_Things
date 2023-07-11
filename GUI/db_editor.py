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
from os.path import join, dirname
from PIL import ImageTk, Image
from string import punctuation

class Database:
    def __init__(self):
        pass
    def show_selection(self):
        text = app.treeview.item(app.my_id, option="text")
        showinfo(message=text)
class App(CTk):
    def __init__(self):
        super().__init__()
        self.database = Database()
        self.img_folder = join(dirname(__file__), "img")
        self.title("Database Editor")
        self.geometry("300x170")
        self.resizable(0, 0)
        self.configure(fg_color="#2f2f2f")

        CTkButton(self, width=200, height=40, corner_radius=10,
                  border_width=2, border_spacing=2, fg_color="#5b5b5b",
                  hover_color="#444444", border_color="#6aa84f",
                  text_color="#ffffff", text_color_disabled="#eeeeee",
                  text="Create Database", font=("Fira Code Regular", 12),
                  command=self.create_database).pack(pady=15)
        CTkButton(self, width=200, height=40, corner_radius=10,
                  border_width=2, border_spacing=2, fg_color="#5b5b5b",
                  hover_color="#444444", border_color="#6aa84f",
                  text_color="#ffffff", text_color_disabled="#eeeeee",
                  text="Edit Database", font=("Fira Code Regular", 12)).pack(pady=20)
        self.center_window(self, 300, 170)
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
    def verify_entry(self):
        self.not_repeat = False
        while not self.not_repeat:
            if not self.entry.get():
                showerror(title="Error", message="You must enter a name for the column")
                return
            if len(self.columns) > 20:
                showerror(title="Error", message="The column limit has been reached")
                return
            if any(char in punctuation for char in self.entry.get()):
                showerror(title="Error", message="Please only use spaces to separate column names")
                self.not_repeat = True
            else:
                self.not_repeat = True
                self.columns.append(self.entry.get())
                self.treeview["columns"] = self.columns
                self.treeview["show"] = "headings"
                self.window.update()

                    # MODIFICACION DE PRUEBA
                self.scrollbar = ttk.Scrollbar(self.window, orient="horizontal", command=self.treeview.xview)
                self.window.update()
                x = self.window.winfo_width()
                y = self.window.winfo_height()
                self.scrollbar.place(x=5, y=y-14, height=12, width=x-10)
                self.treeview.configure(xscrollcommand=self.scrollbar.set)
                for i in self.columns:
                    self.treeview.column(i, width=200, minwidth=200, stretch=False)
                    self.window.update()
                    self.treeview.heading(i, text=i)
    def destroy_table(self):
        self.treeview["columns"] = []
        self.columns.clear()
        self.window.update()
    def create_database(self):
        self.withdraw()
        self.window = CTkToplevel(fg_color="#444444")
        self.window.geometry(f"600x500+50+100")
        self.window.update()
        self.window.resizable(0, 0)
        self.window.title("Create Database")
        self.window.protocol("WM_DELETE_WINDOW", self.quit_app)
        self.window.update()

        menu_bar = tk.Menu(activebackground="#d0e0e3",
                           activeborderwidth=0,
                           activeforeground="#000000")

        edit_menu = tk.Menu(menu_bar, tearoff=False,
                            activebackground="#d0e0e3",
                            activeborderwidth=0,
                            activeforeground="#000000")

        self.color_img = ImageTk.PhotoImage(Image.open(join(self.img_folder, "color.png")))
        self.table_name_img = ImageTk.PhotoImage(Image.open(join(self.img_folder, "db_name.png")))
        edit_menu.add_command(label="Color", accelerator="Ctrl+C",
                              command=lambda: self.change_color(self.window),
                              image=self.color_img,
                              compound=tk.LEFT)
        # edit_menu.add_command(label="Table Name", accelerator="Ctrl+t", 
        #                       image=)
        self.window.bind_all(sequence="<Control-c>", func=lambda event: self.change_color(self.window))

        menu_bar.add_cascade(menu=edit_menu, label="Edit")

        self.window.config(menu=menu_bar)

        self.save_image = ImageTk.PhotoImage(Image.open(join(self.img_folder, "diskette_save.png")).resize((50, 50)))
        CTkButton(self.window, width=60, height=60, corner_radius=0, border_width=2,
                  fg_color="#ffffff", hover_color="#bcbcbc", border_color="#000000",
                  text="", text_color_disabled="#ffffff", image=self.save_image,
                  compound="right").place(x=5, y=5)
        
        self.delete_table_img = ImageTk.PhotoImage(Image.open(join(self.img_folder, "broken_table.png")).resize((60, 50)))
        CTkButton(self.window, width=60, height=60, corner_radius=0, border_width=2,
        fg_color="#ffffff", hover_color="#bcbcbc", border_color="#000000",
        text="", text_color_disabled="#ffffff", image=self.delete_table_img,
        compound="right", command=self.destroy_table).place(x=75, y=5)

        self.add_column_img = ImageTk.PhotoImage(Image.open(join(self.img_folder, "add_column.png")).resize((45, 50)))
        CTkButton(self.window, width=60, height=60, corner_radius=0, border_width=2,
        fg_color="#ffffff", hover_color="#bcbcbc", border_color="#000000",
        text="", text_color_disabled="#ffffff", image=self.add_column_img,
        compound="right", command=self.create_column).place(x=152, y=5)

        self.delete_column_img = ImageTk.PhotoImage(Image.open(join(self.img_folder, "delete_column.png")).resize((50, 50)))
        CTkButton(self.window, width=60, height=60, corner_radius=0, border_width=2,
        fg_color="#ffffff", hover_color="#bcbcbc", border_color="#000000",
        text="", text_color_disabled="#ffffff", image=self.delete_column_img,
        compound="right").place(x=220, y=5)

        self.treeview = ttk.Treeview(self.window, cursor="hand2", selectmode="browse")
        self.treeview["show"] = "tree headings"
        self.treeview.pack(anchor="w", padx=5, pady=80)

        self.columns = []

    def create_column(self):
        # self.not_repeat = False
        # while not self.not_repeat:
            #    MODIFICACION DE PRUEBA
            subwindow = CTkToplevel(fg_color="#2a2d29")
            subwindow.resizable(0, 0)
            subwindow.geometry("400x300")
            
            values = ("NULL", "INTEGER", "REAL", "TEXT", "BLOB")
            
            self.box_value = tk.StringVar()
            # self.type_menu = CTkComboBox(subwindow, width=158, height=30, corner_radius=0, border_width=2, fg_color="#f7fcf7",
            #                         border_color="#000000", button_color="#404736", button_hover_color="#33aa29",
            #                         dropdown_fg_color="#fafcf7", dropdown_hover_color="#6b9b28", 
            #                         dropdown_text_color="#000000", text_color="#000000", font=("Ubuntu Mono", 12),
            #                         dropdown_font=("Ubuntu Mono", 12), values=values, hover=True, state="readonly",
            #                         justify="center", textvariable=self.box_value)
            self.style = ttk.Style()
            self.style.configure("TypeMenu.TCombobox", background="#ffffff", foreground="#000000", borderwidth=2,
                                 relief="solid", anchor="center", padding=5)
            self.type_menu = ttk.Combobox(subwindow, state="readonly", values=values, justify="center",
                                          style="TypeMenu.TCombobox", width=15)
            self.type_menu.current(0)
            self.type_menu.pack(pady=10)
            self.entry = CTkEntry(subwindow, width=200, height=20, corner_radius=10, fg_color="#ffffff",
                            text_color="#000000", placeholder_text="COLUMN NAME", font=("Fira Code Retina", 15),
                            justify="center")
            self.entry.pack(pady=17)

            add = CTkButton(subwindow, width=200, height=40, corner_radius=5, border_width=2, border_spacing=5,
                            fg_color="#1e4713", hover_color="#45992e", command=self.verify_entry).pack(pady=25)
            # column = entry.get()
            # MODIFICACION DE PRUEBA
            # if entry.get() is None:
            #     return

            # # for name in column_names:
            # #     if any(char in punctuation for char in name):
            # #         showerror(title="Error", message="Please only use spaces to separate column names.")
            # #         self.not_repeat = True
            # #         break
            # if any(char in punctuation for char in entry.get()):
            #     showerror(title="Error", message="Please only use spaces to separate column names")
            #     self.not_repeat = True
            #     break
            # else:
            #     self.not_repeat = True
            #     self.columns.append(entry.get())
            #     self.treeview["columns"] = self.columns
            #     self.treeview["show"] = "headings"
            #     self.window.update()

            #     # MODIFICACION DE PRUEBA
            #     self.scrollbar = ttk.Scrollbar(self.window, orient="horizontal", command=self.treeview.xview)
            #     self.window.update()
            #     x = self.window.winfo_width()
            #     self.scrollbar.place(x=5, y=290, height=10, width=x-10)
            #     self.treeview.configure(xscrollcommand=self.scrollbar.set)
            #     for i in self.columns:
            #         self.treeview.column(i, width=200, minwidth=200, stretch=False)
            #         self.window.update()
            #         self.treeview.heading(i, text=i)
                # MODIFICACION DE PRUEBA

#                 self.window.update()
#                 showinfo(title="Success", message="""You have already created the columns 
# of your table, to insert records you must 
# save the database and then edit it in the 
# \"Edit database\" window""")
if __name__ == "__main__":
    app = App()
    app.mainloop()
