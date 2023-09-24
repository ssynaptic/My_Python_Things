import customtkinter as ctk
import tkinter as tk
from tkinter.constants import LEFT
from os.path import (dirname,
                     join)
from PIL import Image

class LeftSectionFrameContainer(ctk.CTkFrame):
    def __init__(self, master, img_folder_path, **kwargs):
        super().__init__(master, **kwargs)

        header_img_path = join(img_folder_path, "logo.png")

        header_img = ctk.CTkImage(Image.open(header_img_path).resize((50, 50)))

        app_header = ctk.CTkLabel(self,
                                  text=("Library\nManagement"),
                                  width=100,
                                  height=20,
                                  corner_radius=7,
                                  fg_color="#ffffff",
                                  text_color="#000000",
                                  font=("Fira Code", 15),
                                  anchor="center",
                                  image=header_img,
                                  compound="top",
                                  justify="center")
        app_header.place(x=24, y=10)


        home_img_path = join(img_folder_path, "home.png")
        home_img = ctk.CTkImage(Image.open(home_img_path).resize((50, 50)))

        dashboard_button = ctk.CTkButton(master=self,
                                         width=135,
                                         height=25,
                                         corner_radius=7,
                                         border_width=1,
                                         border_spacing=3,
                                         fg_color="#ffffff",
                                         hover_color="#e0e1ff",
                                         border_color="#5c72ff",
                                         text_color="#000000",
                                         text_color_disabled="#000000",
                                         text="Home",
                                         font=("Fira Code Retina", 15),
                                         image=home_img,
                                         state="normal",
                                         hover=True,
                                         command=None,
                                         compound="left",
                                         anchor="center")
        dashboard_button.place(x=8, y=80)

        control_var = tk.StringVar(master=self,
                                   name="CONTROL_VARIABLE_0")

        categories_values = ("Technology", "History", "Mathematics")
        categories_menu = ctk.CTkComboBox(self,
                                          width=135,
                                          height=25,
                                          corner_radius=7,
                                          border_width=1,
                                          fg_color="#ffffff",
                                          border_color="#000000",
                                          button_color="#c8ffae",
                                          button_hover_color="#b1ff95",
                                          dropdown_fg_color="#e5ffe1",
                                          dropdown_hover_color="#eaffa4",
                                          dropdown_text_color="#000000",
                                          text_color="#000000",
                                          text_color_disabled="#000000",
                                          font=("Fira Code Retina", 15),
                                          dropdown_font=("Fira Code Semibold", 15),
                                          values=categories_values,
                                          state="readonly",
                                          hover=True,
                                          #command=callback,
                                          command=None,
                                          variable=control_var,
                                          justify="left")
        categories_menu.set(categories_values[0])
        categories_menu.place(x=8, y=120)

        star_img_path = join(img_folder_path, "featured_star.png")
        star_img = ctk.CTkImage(Image.open(star_img_path).resize((50, 50)))

        featured_button = ctk.CTkButton(master=self,
                                        width=135,
                                        height=30,
                                        corner_radius=7,
                                        border_width=2,
                                        border_spacing=0,
                                        fg_color="#ffffff",
                                        hover_color="#fffcdb",
                                        border_color="#1aff00",
                                        text_color="#000000",
                                        text_color_disabled="#343434",
                                        text="Featured",
                                        font=("Fira Code Retina", 15),
                                        image=star_img,
                                        state="normal",
                                        hover=True,
                                        command=None,
                                        compound="left",
                                        anchor="center")
        featured_button.place(x=8, y=160)


        master.update()

class AllFunctionalitiesContainer(ctk.CTkFrame):
    def __init__(self, master, img_folder_path, **kwargs):
        super().__init__(master=master, **kwargs)

        files_and_text = {"register_book.png": "Register\nBook",
                          "search_book.png": "Search\nBook",
                          "add_user.png": "Add\nUser"}

        for file in files_and_text.items():
            func = FunctionalityElement(master=self,
                                        img_folder_path=img_folder_path,
                                        img=file[0],
                                        text=file[1],
                                        command=None)
            func.pack()

        master.update()

class FunctionalityElement(ctk.CTkFrame):
    def __init__(self, master, img_folder_path, img, text, command, **kwargs):
        super().__init__(master=master, fg_color="#ffffff", **kwargs)
        img_path = join(img_folder_path, img)
        loaded_img = ctk.CTkImage(Image.open(img_path), size=(100, 100))

        function_button = ctk.CTkButton(master=self,
                                        width=160,
                                        height=160,
                                        corner_radius=10,
                                        border_width=2,
                                        border_spacing=2,
                                        bg_color="#ffffff",
                                        fg_color="#ffa57b",
                                        hover_color="#d4ff45",
                                        border_color="#cc652a",
                                        text_color="#000000",
                                        text_color_disabled="#000000",
                                        text=text,
                                        font=("Jetbrains Mono", 14),
                                        textvariable=None,
                                        image=loaded_img,
                                        state="normal",
                                        hover=True,
                                        command=command,
                                        compound="top",
                                        anchor="center")
        function_button.pack(anchor="w",
                             expand=False,
                             padx=3,
                             pady=3,
                             side=LEFT)


#        function_label = ctk.CTkLabel(master=self,
#                                      text=text,
#                                      width=200,
#                                      height=200,
#                                      corner_radius=10,
#                                      bg_color="#ffffff",
#                                      fg_color="#ffa57b",
#                                      text_color=("#000000"),
#                                      font=("Fira Code Retina", 14),
#                                      anchor="center",
#                                      image=loaded_img,
#                                      compound="top",
#                                      justify="center",
#                                      cursor="hand2")
#        function_label.pack()

        master.update()
class App(ctk.CTk):
    def __init__(self, img_folder_path):
        super().__init__()
        self.title("Library Management")
        self.geometry("600x500")
        self.resizable(False, False)

        self.center_window(window=self,
                           width=600,
                           height=500)

        self.update()

        self.configure(fg_color="#fffbe9")

        self.left_section_container = LeftSectionFrameContainer(master=self,
                                                                 img_folder_path=img_folder_path,
                                                                 width=150,
                                                                 height=490,
                                                                 border_width=3,
                                                                 fg_color="#ffffff",
                                                                 border_color="#ffcca0")
        self.left_section_container.place(x=5, y=5)

        self.right_section_container = AllFunctionalitiesContainer(master=self,
                                                                   img_folder_path=img_folder_path,
                                                                   width=400,
                                                                   height=200,
                                                                   border_width=3,
                                                                   fg_color="#ffffff",
                                                                   border_color="#90ffb5")
        self.right_section_container.place(x=160, y=5)

    def center_window(self, window, width, height):
        window.geometry(f"{width}x{height}")
        window.update()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        window_width = window.winfo_width()
        window_height = window.winfo_height()

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        window.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    img_folder = join(dirname(__file__), "img")
    app = App(img_folder_path=img_folder)
    app.mainloop()