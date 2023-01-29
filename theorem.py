import tkinter as tk
from tkinter import ttk 
from tkinter.colorchooser import askcolor
from tkinter import messagebox
from math import sqrt

def change_color():
    color = askcolor(title="Choose The Background Color")
    root.config(bg=color[1])
    canvas.configure(background=color[1])

def calculate():
        try:
            operation = menu.get()
            cateto_1 = abs(float(cateto1.get()))
            cateto_2 = abs(float(cateto2.get()))
            hipotennussa = abs(float(hipotenusa.get()))
            if operation == ("Hipotenusa"):
                result = sqrt(cateto_1 ** 2 + cateto_2 ** 2)
                result = round(result, 2)
                hipotenusa.delete(0, tk.END)
                hipotenusa.insert(0, result)
            
            if operation == ("Cateto"):
                index = 0
                if cateto_1 > 0 and cateto_2 > 0:
                    raise ValueError
                if cateto_1 and not cateto_2:
                    cateto_x = cateto_1
                    index += 1
                if not cateto_1 and cateto_2:
                    cateto_x = cateto_2
                    index += 2
                result = sqrt(hipotennussa ** 2 - cateto_x ** 2)
                if index == 1:
                    cateto2.delete(0, tk.END)
                    cateto2.insert(0, round(result, 2))
                if index == 2:
                    cateto1.delete(0, tk.END)
                    cateto1.insert(0, round(result, 2))
                
        except:
            messagebox.showwarning(title="Error",
            message="""Revise que los valores sean
correctos de acuerdo a la operacion que
quiere realizar.
Si va a dejar un valor en blanco debe ponerlo en 0""")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x255")
    root.iconbitmap("icon.ico")
    root.title("Phytagoras Theorem")
    root.config(bd=3, relief="sunken")
    
    # Frame donde estan ubicados los Input de los Valores
    s = ttk.Style()
    s.theme_use("default")
    s.configure("Frame.TFrame", background="red", borderwidth=3, relief="solid")
    section = ttk.Frame(root, style="Frame.TFrame", width=107, height=247).place(x=2, y=2)
    
    # Etiqueta para indicar que en la parte derecha estan ubicados
    # los Input de los valores
    s.configure("LabelV.TLabel", background="#f6ff4b", foreground="#1d9c00", 
    font=("Verdana", 12, "underline"), borderwidth=3, relief="solid",
    width=8, anchor="center")
    label1 = ttk.Label(root, text="Valores", style="LabelV.TLabel").place(x=8, y=8)
    
    # Etiqueta para indicar que el Input de abajo es el del Cateto A
    s.configure("LabelCA.TLabel", background="#2610a2", foreground="#85ff8b",
    font=("Verdana", 10), width=9, anchor="center")
    label_c1 = ttk.Label(root, text="Cateto A", style="LabelCA.TLabel").place(x=10, y=42)
    
    # Input del Cateto A
    s.configure("EntryC1.TEntry", background="#ffffff", foreground="#2610a2",
    font=("Hack", 10), borderwidth=2, relief="raised")
    cateto1 = ttk.Entry(root, style="EntryCA.TEntry", width=12)
    cateto1.place(x=11, y=68)
    cateto1.insert(0, 0)
    
    # Etiqueta para indicar que el Input de abajo es el del Cateto B 
    s.configure("LabelCB.TLabel", background="#2610a2", foreground="#85ff8b",
    font=("Verdana", 10), width=9, anchor="center")
    label_c2 = ttk.Label(root, text="Cateto B", style="LabelCB.TLabel").place(x=10, y=100)
    
    # Input del Cateto B
    s.configure("EntryC2.TEntry", background="#ffffff", foreground="#2610a2",
    font=("Hack", 10), bordewidth=2, relief="raised")
    cateto2 = ttk.Entry(root, style="EntryC2.TEntry", width=12)
    cateto2.place(x=11, y=130)
    cateto2.insert(0, 0)
    
    # Etiqueta para indicar que el Input de abajo es el de la Hipotenusa   
    s.configure("LabelH.TLabel", background="#2610a2", foreground="#85ff8b",
    font=("Verdana", 10), width=9, anchor="center")
    label_h = ttk.Label(root, text="Hipotenusa", style="LabelH.TLabel").place(x=10, y=160)
    
    # Input de la Hipotenusa
    s.configure("EntryH.TEntry", background="#ffffff", foreground="#2610a2",
    font=("Hack", 10), borderwidth=2, relief="raised")
    hipotenusa = ttk.Entry(root, style="EntryH.TEntry", width=12)
    hipotenusa.place(x=11, y=190)
    hipotenusa.insert(0, 0)
    
    # Menu para seleccionar operacion
    s.configure("Menu.TCombobox", foreground="green", 
    font=("Hack", 6),borderwidth=3, relief="solid")
    menu = ttk.Combobox(root, style="Menu.TCombobox",
    values=["Hipotenusa", "Cateto"], width=9, 
    state="readonly")
    menu.current(0)
    menu.place(x=10, y=218)
    
    # Creacion de Canvas para hacer flechas
    canvas = tk.Canvas(root, width=173, height=216,
    highlightthickness=0)
    canvas.create_line(80, 0, 80, 80, arrow=tk.LAST)
    canvas.create_line(80, 130, 80, 210, arrow=tk.FIRST)
    canvas.place(x=115, y=32)
    
    # Creacion de Boton para calcular resultados
    s.configure("TButton", background="#120057", foreground="#47ff52")
    s.map("TButton", background=[("active", "#120057")])
    boton_calcular = ttk.Button(root, text="Calcular", 
    command=calculate).place(x=160, y=120)
    
    # Boton para cambiar el color de fondo
    s.configure("ButtonCC.TButton", background="#005c1b",
    foreground="#ffee70", font=("Hack", 6, "underline"), 
    borderwidth=2, relief="solid")
    botonCC = ttk.Button(root, style="ButtonCC.TButton",
    text="Color", command=change_color).place(x=225, y=2)
    root.mainloop() 