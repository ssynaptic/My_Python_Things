import customtkinter as ctk
from tkinter.messagebox import (showinfo,
                                showerror)
import tkinter as tk
from signupbackend import SignUpBackend
from loginbackend import LogInBackend
from PIL import Image
from os.path import (dirname,
                     join)
import string

class BaseForm(ctk.CTkFrame):
    def __init__(self, action_text, img_folder_path, **kwargs):
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
        form.place(x=320, y=100)

        message = ctk.CTkLabel(master=form,
                                      width=150,
                                      height=30,
                                      corner_radius=0,
                                      bg_color="#ffffff",
                                      fg_color="#ffffff",
                                      text_color="#000000",
                                      text_color_disabled="#000000",
                                      text=action_text,
                                      font=("Jetbrains Mono", 25),
                                      anchor="center")

        form.update()

        form_container_width = form.winfo_width()

        message_x = (form_container_width // 2) - (150 // 2)
        message.place(x=message_x, y=10)

        self.username_input = ctk.CTkEntry(master=form,
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
        self.username_input.place(x=inputs_x, y=60)

        self.password_input = ctk.CTkEntry(master=form,
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
        self.password_input.place(x=inputs_x, y=110)

        action_button = ctk.CTkButton(master=form,
                                     width=150,
                                     height=35,
                                     corner_radius=7,
                                     border_width=0,
                                     bg_color="#ffffff",
                                     fg_color="#3c94ff",
                                     hover_color="#0022ff",
                                     border_color="#ffffff",
                                     text_color="#ffffff",
                                     text_color_disabled="#ffffff",
                                     text=action_text,
                                     font=("Jetbrains Mono", 20),
                                     state="normal",
                                     hover=True,
                                     command=self.get_data,
                                     anchor="center")
        action_button_x = (form_container_width // 2) - (150 // 2)
        action_button.place(x=action_button_x, y=160)


class SignUpForm(BaseForm):
    def __init__(self, **kwargs):
        super().__init__(action_text="Log In", **kwargs)
        self.backend = SignUpBackend()

    def get_data(self):
        username = self.username_input.get()
        password = self.password_input.get()

        if len(username) < 5 or not username:
            showerror(title="Error",
                      message="The user name should be longer")
            return
        if len(password) < 10 or not password:
            showerror(title="Error",
                      message="The password should be longer")
            return

        for char in username:
            if char in string.punctuation:
                showerror(title="Error",
                          message="Bad username. Verify that not contain special symbols")
                return
        db_results = self.backend.check_if_db_exists()
        if db_results == "is_valid":
            self.backend.create_database()
            self.backend.create_users_table()
            self.backend.create_user(username=username,
                                     password=password)
            showinfo(title="Success",
                     message="""User created successfully.
You will be redirected to the home page""")
            self.destroy()
            return

        if db_results == "there_is_an_equal":
            db_integrity = self.backend.check_db_integrity()
            if db_integrity == "is_valid":
                checking_existence = self.backend.check_if_user_exists(username=username,
                                                                password=password)
                if checking_existence:
                    showerror(title="Error",
                              message="Already exists a user with the same credentials")
                else:
                    self.backend.create_user(username=username,
                                             password=password)
                    showinfo(title="Success",
                             message="""User created successfully.
You will be redirected to the home page""")
                    self.destroy()
                return
            else:
                showerror(title="Error",
                          message="The content of the database appears to be altered")
                return

        if db_results == "is_invalid":
            showerror(title="Error",
                      message="Can't create the database. There seems to be a file or folder with the same name")
            return

class LogInForm(BaseForm):
    def __init__(self, **kwargs):
        super().__init__(action_text="Log In", **kwargs)
        self.backend = LogInBackend()

    def get_data(self):
        username = self.username_input.get()
        password = self.password_input.get()

        if len(username) < 5 or not username:
            showerror(title="Error",
                      message="The user name should be longer")
            return
        if len(password) < 10 or not password:
            showerror(title="Error",
                      message="The password should be longer")
            return

        for char in username:
            if char in string.punctuation:
                showerror(title="Error",
                          message="Bad username. Verify that not contain special symbols")
                return
        db_results = self.backend.check_if_db_exists()

        if db_results == "is_valid":
            db_integrity = self.backend.check_db_integrity()
            if db_integrity == "is_valid":
                check_user_existence = self.backend.check_if_user_exists(username=username,
                                                                         password=password)
                if check_user_existence:
                    showinfo(title="Success",
                              message=f"""Succcessfully logged as {username}.
You will be redirected to the home page""")
                    self.destroy()
                else:
                    showerror(title="Error",
                              message=f"Failed to login as {username}")

class TopNavigationBar(ctk.CTkFrame):
    def __init__(self, img_folder_path, **kwargs):
        super().__init__(**kwargs)
        logo_img_path = join(img_folder_path, "logo.png")
        logo_img = ctk.CTkImage(Image.open(logo_img_path), size=(20, 20))

        logo_button = ctk.CTkButton(master=self,
                                    # width=50,
                                    # height=35,
                                    corner_radius=0,
                                    border_width=0,
                                    bg_color="#ffffff",
                                    fg_color="#3c94ff",
                                    hover_color="#0022ff",
                                    border_color="#ffffff",
                                    text_color="#ffffff",
                                    text_color_disabled="#ffffff",
                                    text=action_text,
                                    font=("Jetbrains Mono", 20),
                                    state="normal",
                                    hover=True,
                                    command=self.get_data,
                                    anchor="center")


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

        login_form = LogInForm(img_folder_path=img_folder_path,
                                 master=self,
                                 width=600,
                                 height=500,
                                 border_width=0,
                                 fg_color="#ffffff",
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
    app.after(1, app.x)
    app.mainloop()