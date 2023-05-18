import tkinter as tk
from tkinter import ttk
from os.path import join, dirname
from tkinter.colorchooser import askcolor

class App(tk.Tk):
    def __init__(self):
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

        self.menu_bar.add_cascade(menu=self.menu_edit, label="Edit")

        self.config(menu=self.menu_bar)

        self.style = ttk.Style()
        self.style.configure("Section.TFrame", background="red",
        borderwidth=2, relief="solid", width=80, height=346)
        self.section_buttons = ttk.Frame(self, 
        style="Section.TFrame", width=100, 
        height=346).place(x=2, y=2)
    def change_color(self):
        color = askcolor(title="Background Color")    
        self.config(bg=color[1])

if __name__ == ("__main__"):
    app = App()
    app.mainloop()
