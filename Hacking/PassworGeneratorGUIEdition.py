import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor
from tkinter.messagebox import showinfo, showwarning
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
        self.config(bg="white", font=("Hack", 14), width=8, justify="center",
        bd=2, relief="solid")

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self["fg"] = self.placeholder_color

    def foc_in(self, *args):
        if self["fg"] == self.placeholder_color:
            self.delete(0, tk.END)
            self["fg"] = self.default_fg_color
    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap("password.ico")
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
        self.help_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(menu=self.help_menu, label="Help")
        self.bind_all("<Control-h>", self.show_help)
        self.help_menu.add_command(label="Help", accelerator="Ctrl+H",
        command=self.show_help)
        self.config(menu=self.menu_bar)

        self.image = ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(__file__),
        "images\\passwordimage.png")).resize((20, 17)))

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", background="yellow", foreground="black",
        borderwidth=2, relief="groove", font=("Helvetica", 12), anchor="center")
        self.style.map("TButton", background=[("active", "yellow")])

        self.button1 = ttk.Button(self, text="Generate Password", style="TButton",
        width=20, image=self.image, compound=tk.RIGHT, cursor="hand2",
        command=self.generate_password).place(x=20, y=110)
        self.length = EntryWithPlaceholder(placeholder="Length")
        self.length.place(x=267, y=112)
    def change_color(self, event=None):
        color = askcolor(title="Background Color")
        self.config(bg=color[1])
    def generate_password(self, length=15):
        if len(self.length.get()) > 0 and str(self.length.get()) == True:
            showwarning(title="Error", message="You must provide an integer as the length of the password")

        if self.length.get().isdigit() == True and len(self.length.get()) > 0:
            length = int(self.length.get())
        else:
            length = length
        lower_case = list(string.ascii_lowercase)
        upper_case = list(string.ascii_uppercase)
        simbols = ["!", "#", "$", "%", "&", "/", "(", ")", "=",
        "?", "¿", "¡", "+", "*", "{", "}", "[", "]", ":", ".", "-", "_"]
        characters = lower_case + upper_case + simbols
        password = ("").join([str(choice(characters)) for x in range(1, length+1)])
        showinfo(title="New Password", message=f"This Is Your New Password:\n{password}")
        self.clipboard_append(password)
    def show_help(self, event=None):
        showinfo(title="Help", message="""This program will create strong passwords depending on the
length that you pass to it. If you do not give a length, a default length of 15 characters will be used
(This is the minimum length for a strong password today). After you have generated your
password it will be copied to the clipboard. \nThe passwords you have generated may become one as
they are copied to the clipboard""")
if __name__ == "__main__":
    app = App()
    app.mainloop()
