import tkinter as tk
from tkinter import messagebox
import operator

def operacion(n1, n2, op):
    n1 = float(n1)
    n2 = float(n2)
    operadores = {1 : operator.add,
                  2 : operator.sub,
                  3 : operator.mul,
                  4 : operator.truediv}
    fop = operadores.get(op)
    return fop(n1, n2)
    
def calculate():
    opcion = x.get()
    n1 = number1.get()
    n2 = number2.get()
    if not n1 or not n2:
        messagebox.showwarning(title="Error", message="""Falta uno o mas numeros. 
Por favor introduzcalos para continuar""")
    if n1.isdigit() and n2.isdigit():
        result = operacion(n1, n2, opcion)
        messagebox.showinfo(title="The Result Is:", message=result)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x190")
    root.title("Calculator")
    root.resizable(0, 0)
    root.config(bg="blue", bd=2, relief="groove")
    
    message = tk.Label(root, text="Select An Option Below", bg="yellow", fg="black", bd=2,
    relief="sunken", font=("Arial", 13), width=22).place(x=60, y=10)
    
    x = tk.IntVar()
    x.set(value=1)
    
    tk.Radiobutton(root, text="Sumar", fg="green", value=1, variable=x, width=8).place(x=10, y=55)
    tk.Radiobutton(root, text="Restar", fg="green", value=2, variable=x, width=8).place(x=105, y=55)
    tk.Radiobutton(root, text="Multip", fg="green", value=3, variable=x, width=8).place(x=205, y=55)
    tk.Radiobutton(root, text="Dividir", fg="green", value=4, variable=x, width=8).place(x=300, y=55)
    
    indication = tk.Label(root, text="<--Numbers-->", bg="black", fg="yellow", bd=2, 
    relief="sunken", font=("Verdana", 10)).place(x=140, y=85)
    
    number1 = tk.Entry(root, bg="green", fg="yellow", bd=2, relief="groove", font=("Hack", 12),
    width=10)
    number1.place(x=12, y=85)
    number1.insert(0, 0)
    
    number2 = tk.Entry(root, bg="purple", fg="cyan", bd=2, relief="groove", font=("Hack", 12),
    width=10)
    number2.place(x=265, y=85)
    number2.insert(0, 0)
    
    calcular = tk.Button(root, text="Calcular", activeforeground="spring green", bd=2, relief="groove",
    font=("Hack", 12), width=32, command=calculate).place(x=3, y=125)
    
    root.mainloop()