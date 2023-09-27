import customtkinter as ctk
import tkinter as tk
from PIL import Image
from os.path import (dirname,
                     join)

class LoginForm(ctk.CTkFrame):
    def __init__(self, img_folder_path, **kwargs):
        super().__init__(**kwargs)
        app_image_path = join(img_folder_path, "logo.png")
        app_image = ctk.CTkImage(Image.open(app_image_path), size=(100, 100))

        header = ctk.CTkLabel(master=self,
                              text="Library\nManagement",
                              width=250,
                              height=150,
                              corner_radius=0,
                              bg_color="#ffffff",
                              fg_color="#ffffff",
                              text_color="#000000",
                              font=("Jetbrains Mono", 20),
                              anchor="center",
                              image=app_image,
                              compound="top",
                              justify="center",
                              cursor="hand2")
        header.place(x=50, y=150)
        self.update()

        form = ctk.CTkFrame(master=self,
                            width=250,
                            height=280,
                            corner_radius=7,
                            border_width=2,
                            bg_color="#ffffff",
                            fg_color="#ffffff",
                            border_color="#44ff00")
        form.place(x=320, y=80)

#        signup_message = ctk.CTkLabel(master=form,
#                                      width=None,
#                                      height=None,
#                                      corner_radius=0,
#                                      bg_color="#ffffff",
#                                      fg_color="#ffffff",
#                                      text_color="#000000",
#                                      text_color_disabled="#000000",
#                                      text="Sign Up",
#                                      font=("JetBrains Mono", 15))

        signup_message = ctk.CTkLabel(master=form,
                                      width=150,
                                      height=30,
                                      corner_radius=0,
                                      bg_color="#ffffff",
                                      fg_color="#ffffff",
                                      text_color="#000000",
                                      text_color_disabled="#000000",
                                      text="Sign Up",
                                      font=("Jetbrains Mono", 25),
                                      anchor="center")

        form.update()

        form_container_width = form.winfo_width()

        signup_message_x = (form_container_width // 2) - (150 // 2)
        signup_message.place(x=signup_message_x, y=10)

        username_input = ctk.CTkEntry(master=form,
                                      width=190,
                                      height=30,
                                      corner_radius=7,
                                      border_width=1,
                                      bg_color="#ffffff",
                                      fg_color="#ffffff",
                                      border_color="#9a9a9a",
                                      text_color="#000000",
                                      placeholder_text_color="#9a9a9a",
                                      placeholder_text="USERNAME",
                                      font=("Fira Code Retina", 15),
                                      state="normal",
                                      justify="center")
        form.update()
        inputs_x = (form_container_width // 2) - (190 // 2)
        username_input.place(x=inputs_x, y=60)

        password_input = ctk.CTkEntry(master=form,
                                      width=190,
                                      height=30,
                                      corner_radius=7,
                                      border_width=1,
                                      bg_color="#ffffff",
                                      fg_color="#ffffff",
                                      border_color="#9a9a9a",
                                      text_color="#000000",
                                      placeholder_text_color="#9a9a9a",
                                      placeholder_text="PASSWORD",
                                      font=("Fira Code Retina", 15),
                                      state="normal",
                                      justify="center",
                                      show="*")
        password_input.place(x=inputs_x, y=110)

        login_button = ctk.CTkButton(master=form,
                                     width=150,
                                     height=28,
                                     corner_radius=7,
                                     border_width=0,
                                     bg_color="#ffffff",
                                     fg_color="#3c94ff",
                                     hover_color="#0022ff",
                                     border_color="#ffffff",
                                     text_color="#ffffff",
                                     text_color_disabled="#ffffff",
                                     text="Sign Up",
                                     font=("Jetbrains Mono", 20),
                                     state="normal",
                                     hover=True,
                                     #command=None,
                                     anchor="center")
        login_button_x = (form_container_width // 2) - (150 // 2)
        login_button.place(x=login_button_x, y=160)

class App(ctk.CTk):
    def __init__(self, img_folder_path):
        super().__init__()
        self.title("Library Management")
        self.geometry("600x500")
        self.resizable(False, False)

        self.center_window(window=self,
                           width=600,
                           height=500)
        self.configure(fg_color="#ffffff")

        login_form = LoginForm(img_folder_path=img_folder_path,
                               master=self,
                               width=600,
                               height=500,
                               border_width=0,
                               fg_color="#ffffff",
                               #fg_color="red",
                               border_color="#ffffff")
        login_form.place(x=1, y=1)

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