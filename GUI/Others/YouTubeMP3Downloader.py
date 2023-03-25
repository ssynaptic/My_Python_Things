import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showwarning
from pytube import YouTube
import os
from PIL import ImageTk, Image
def download():
#    try:
        url = given_url.get("0.0", "end")
        audio = YouTube(url)
        output = audio.streams.get_audio_only().download()
        path = os.path.splitext(output)
        new_file = path[0] + '.mp3'
        os.rename(output, new_file)
#    except:
        showwarning(title="Error", message="An error has occurred with the download, check that the link is not misspelled")

if __name__ == "__main__":
    images_folder = os.path.join(os.path.dirname(__file__), "images")
    root = tk.Tk()
    root.title("YouTube MP3 Downloader")
    root.iconbitmap(os.path.join(images_folder, "youtube.ico"))
    root.geometry("400x300+500+200")
    root.resizable(0, 0)
    root.config(bg="red", bd=3, relief="sunken")

    image = ImageTk.PhotoImage(Image.open(os.path.join(images_folder,
    "youtube.png")).resize((140, 90)))

    ttk.Label(root, image=image).place(x=126, y=10)
    
    style = ttk.Style()
    style.configure("Label1.TLabel", background="white",
    foreground="black", font=("Verdana", 10, "bold"), borderwidth=0,
    anchor="center")
    
    ttk.Label(root, text="URL To Video --> ",
    style="Label1.TLabel", width=18).place(x=10, y=120)

    given_url = tk.Text(root, background="white", foreground="red",
    font=("Hack", 12), padx=0, pady=0, borderwidth=2, relief="solid", width=19, 
    height=1).place(x=190, y=120)
    
    style.configure("Button1.TButton", background="yellow", foreground="green",
    font=("Verdana", 10, "italic"), borderwidth=5, relief="solid")
    
    ttk.Button(root, text="Download", style="Button1.TButton",
    width=10, command=download).place(x=140, y=150)
    
    root.mainloop()
