import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk
import os
import string
from random import choice

class EntryWithPlaceholder(tk.Entry):
    def __init__(self, main=None, placeholder="<PLACEHOLDER>", color="grey"):
        super().__init__(main)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self["fg"]
        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)
        self.put_placeholder()
        self.config(bg="white", font=("Hack", 12), width=8, justify="center",
        bd=2, relief="solid")
        self.insert(0, "0")

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self["fg"] = self.placeholder_color

    def foc_in(self, *args):
        if self["fg"] == self.placeholder_color:
            self.delete("0", "end")
            self["fg"] = self.default_fg_color
    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("400x300+300+200")
        self.title("Password Generator")
        self.resizable(0, 0)
        self.configure(bg="#E4D0D0", bd=3, relief="sunken")

        self.menu_bar = tk.Menu()
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(menu=self.edit_menu, label="Edit")
        self.bind_all("<Control-c>", self.change_color)
        self.edit_menu.add_command(label="Color", accelerator="Ctrl+C",
        command=self.change_color)
        self.config(menu=self.menu_bar)

        self.image = ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(__file__),
        "images\\passwordimage.png")).resize((20, 17)))

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", background="yellow", foreground="black",
        borderwidth=2, relief="groove", font=("Helvetica", 12), anchor="center")
        self.style.map("TButton", background=[("active", "yellow")])

        self.button1 = ttk.Button(self, text="Generate Password", style="TButton",
        width=20, image=self.image, compound=tk.RIGHT, cursor="hand2").place(x=30, y=20)
        self.length = EntryWithPlaceholder(self, placeholder="Length", color="grey").place(x=280, y=24)
        self.password = self.generate_password(int(self.length.get()))
    def change_color(self, event=None):
        color = askcolor(title="Background Color")
        self.config(bg=color[1])
    def generate_password(self, length):
        lower_case = list(string.ascii_lowercase)
        upper_case = list(string.ascii_uppercase)
        simbols = ["!", "#", "$", "%", "&", "/", "(", ")", "=", 
        "?", "¿", "¡", "+", "*", "{", "}", "[", "]", ":", ".", "-", "_"]
        characters = lower_case + upper_case + simbols
        password = ("").join([str(random.choice(characters)) for x in range(1, length+1)])
if __name__ == "__main__":
    app = App()
    app.mainloop()
