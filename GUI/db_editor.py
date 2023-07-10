import tkinter as tk
from tkinter import ttk
from customtkinter import (CTk, CTkLabel, 
                           CTkButton, CTkToplevel, 
                           CTkImage,
                           CTkScrollbar)
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
    def create_database(self):
        self.withdraw()
        self.window = CTkToplevel(fg_color="#444444")
        # self.window.resizable(0, 0)
        self.window.title("Create Database")
        self.window.attributes("-zoomed", True)
        self.window.protocol("WM_DELETE_WINDOW", self.quit)

        menu_bar = tk.Menu(activebackground="#d0e0e3",
                           activeborderwidth=0,
                           activeforeground="#000000")

        edit_menu = tk.Menu(menu_bar, tearoff=False,
                            activebackground="#d0e0e3",
                            activeborderwidth=0,
                            activeforeground="#000000")

        self.color_img = ImageTk.PhotoImage(Image.open(join(self.img_folder, "color.png")))
        edit_menu.add_command(label="Color", accelerator="Ctrl+C",
                              command=lambda: self.change_color(self.window),
                              image=self.color_img,
                              compound=tk.LEFT)
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
        compound="right").place(x=75, y=5)

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
        self.treeview["show"] = "headings"
        self.treeview.pack(anchor="w", padx=5, pady=80)

    def create_column(self):
        self.not_repeat = False
        while not self.not_repeat:
            columns = askstring(title="Columns", prompt="Enter the columns separated by a space")
            if columns is None:
                # El diálogo fue cerrado sin ingresar ningún valor
                return

            column_names = columns.split()
            for name in column_names:
                if any(char in punctuation for char in name):
                    showerror(title="Error", message="Please only use spaces to separate column names.")
                    self.not_repeat = True
                    break
            else:
                # No se encontraron signos de puntuación en los nombres de columna
                self.not_repeat = True
                # Continuar con el resto de la lógica para agregar las columnas al Treeview
                self.treeview["columns"] = column_names
                self.treeview["show"] = "headings"
                # print(self.treeview["show"])
                # for column_name in column_names:
                #     self.treeview.heading(column_name, text=column_name)

                # MODIFICACION DE PRUEBA
                
                # for i in column_names:
                #     self.treeview.column(f"{i}", width=100, minwidth=0, stretch=False)
                #     self.treeview.heading(f"{i}", text=i)
                
                self.scrollbar = ttk.Scrollbar(self.window, orient="horizontal", command=self.treeview.xview)
                self.treeview.configure(xscrollcommand=self.scrollbar.set)
                self.scrollbar.pack(side="bottom", fill="x")
                for i in column_names:
                    self.treeview.column(i, width=200, minwidth=200, stretch=False)
                    self.window.update()
                    self.treeview.heading(i, text=i)
                # MODIFICACION DE PRUEBA

                self.window.update()
if __name__ == "__main__":
    app = App()
    app.mainloop()
