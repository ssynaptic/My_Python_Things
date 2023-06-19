import tkinter as tk
from customtkinter import (CTk, CTkLabel, 
                           CTkButton, CTkToplevel, 
                           CTkImage)
from tkinter.colorchooser import askcolor
from tkinter.messagebox import showinfo
from os.path import join, dirname
from PIL import ImageTk, Image
class App(CTk):
    def __init__(self):
        super().__init__()
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
        window = CTkToplevel(fg_color="#444444")
        window.title("Create Database")
        window.attributes("-zoomed", True)
        window.protocol("WM_DELETE_WINDOW", self.quit)

        menu_bar = tk.Menu(activebackground="#d0e0e3",
                           activeborderwidth=0,
                           activeforeground="#000000")

        edit_menu = tk.Menu(menu_bar, tearoff=False,
                            activebackground="#d0e0e3",
                            activeborderwidth=0,
                            activeforeground="#000000")

        self.color_img = ImageTk.PhotoImage(Image.open(join(self.img_folder, "color.png")))
        edit_menu.add_command(label="Color", accelerator="Ctrl+C",
                              command=lambda: self.change_color(window),
                              image=self.color_img,
                              compound=tk.LEFT)
        window.bind_all(sequence="<Control-c>", func=lambda event: self.change_color(window))

        menu_bar.add_cascade(menu=edit_menu, label="Edit")

        window.config(menu=menu_bar)

        self.save_image = ImageTk.PhotoImage(Image.open(join(self.img_folder, "diskette_save.png")).resize((50, 50)))
        CTkButton(window, width=60, height=60, corner_radius=10, border_width=2, border_spacing=0,
                  fg_color="#ffffff", hover_color="#bcbcbc", border_color="#000000",
                  text="", text_color_disabled="#ffffff", image=self.save_image,
                  compound="right").place(x=5, y=5)
        
        self.delete_table_img = ImageTk.PhotoImage(Image.open(join(self.img_folder, "broken_table.png")).resize((60, 50)))
        self.save_image = ImageTk.PhotoImage(Image.open(join(self.img_folder, "diskette_save.png")).resize((50, 50)))
        CTkButton(window, width=60, height=60, corner_radius=10, border_width=2, border_spacing=0,
        fg_color="#ffffff", hover_color="#bcbcbc", border_color="#000000",
        text="", text_color_disabled="#ffffff", image=self.delete_table_img,
        compound="right").place(x=80, y=5)
if __name__ == "__main__":
    app = App()
    app.mainloop()
