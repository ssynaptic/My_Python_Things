# Library Management Program (In Development)

from customtkinter import (CTk,
                           CTkFrame,
                           CTkLabel,
                           CTkImage,
                           CTkButton,
                           CTkEntry,
                           CTkCombobox)
from tkinter import LabelFrame
from os.path import (dirname,
                     join)
from PIL import (ImageTk,
                 Image)
                 
from tkinter.messagebox import showinfo

class App(CTk):
    img_folder = join(dirname(__file__), "img")
    print(img_folder)
    def __init__(self):
        super().__init__()
        self.geometry("500x400+100+100")
        self.resizable(False, False)
        self.title("Library Management")
        self.update()
        
        #self.configure(fg_color="#ffffff")
        self.configure(fg_color="#FFF2E2")
        
#        CTkFrame(self,
#                 width=100,
#                 height=400,
#                 border_width=2,
#                 fg_color="#ffffff",
#                 border_color="#000000").place(x=0, y=0)

        self.right_section_container = LabelFrame(self,
                                                  background="#ffffff",
                                                  borderwidth=1,
                                                  foreground="#999999",
                                                  height=399,
                                                  highlightbackground="#ffffff",
                                                  highlightcolor="#ffffff",
                                                  highlightthickness=0,
                                                  labelanchor="n",
                                                  relief="solid",
                                                  takefocus=False,
                                                  text="",
                                                  width=140).place(x=1, y=1)
        
        self.logo_img = CTkImage(Image.open(join(self.img_folder,
                                                 "logo.png")).resize((50, 50)))
        self.header = CTkLabel(master=self.right_section_container,
                               text="LibManager",
                               height=30,
                               corner_radius=5,
                               fg_color="#f9ffca",
                               text_color="#000000",
                               font=("Fira Code Retina", 17),
                               anchor="w",
                               image=self.logo_img,
                               compound="left").grid(row=0,
        #self.header.grid(row=0,
                                                     column=0,
                                                     sticky="w",
                                                     pady=30,
                                                     padx=12)
        self.search_box = CTkEntry(master=self.right_section_container,
                                    textvariable=None,
                                    width=118,
                                    height=30,
                                    corner_radius=0,
                                    fg_color="#ffffff",
                                    border_color="#000000",
                                    text_color="#000000",
                                    placeholder_text_color="#ff5644",
                                    placeholder_text="SEARCH",
                                    font=("Verdana", 12),
                                    state="normal",
                                    justify="center")
        self.search_box.grid(row=1,
                             column=0,
                             padx=0,
                             pady=5)
#        self.search_box.map(fg_color=[("active", "#ff5644")],
#                                      ("pressed", "gray"))
        self.star_img = CTkImage(Image.open(join(self.img_folder,
                                                   "featured_star.png")).resize((30, 30)))
        CTkButton(master=self.right_section_container,
                  width=118,
                  height=20,
                  corner_radius=5,
                  fg_color="#ffffff",
                  hover_color="#ffebdd",
                  border_color="black",
                  text_color="#000000",
                  text_color_disabled="#000000",
                  text="Featured",
                  font=("Fira Code Retina", 17),
                  image=self.star_img,
                  compound="left").grid(row=2,
                                       column=0,
                                       padx=10,
                                       pady=10)
if __name__ == "__main__":
    app = App()
    app.mainloop()