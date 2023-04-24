from tkinter import ttk
from tkinter import StringVar
from tkinter import IntVar
from tkinter import DoubleVar
from tkinter import Label
from tkinter import Button
from tkinter import Menu
from tkinter import Entry
from tkinter import messagebox
from tkinter import *
from tkcalendar import *
from datetime import datetime

# from modelobagnato7 import Model
from modelo import Abmc 

class Vista():
    def __init__(self, main):
        # self.modelo=Model()
        self.master = main #cua
        self.objeto_base = Abmc()
        
        # Para tener un retorno en la vista, agregamos:
        
        self.master.title("Control de gastos")
        self.master.geometry("500x500")

        # Variables: 
        self.fecha = DateEntry()
        self.tipo = StringVar()
        self.monto = DoubleVar()
        self.descripcion = StringVar()
        self.tree = None # Esto me parece que no va?
        

        menubar = Menu(self.master)
        self.master.config(menu=menubar)
        menu_archivo = Menu(menubar, tearoff=0)
        # menu_archivo.add_command(label="Eliminar base de datos", command=self.objeto_base.eliminar_bd(self.tree)) # Cambié el "tree" por el "self.tree"
        
        menu_archivo.add_command(label="Eliminar base de datos", command=lambda: self.objeto_base.eliminar_bd(self.tree))
        menu_archivo.add_command(label="Salir", command=lambda: self.objeto_base.salir(self.master))
        menu_archivo.add_command(label="Crear nueva base", command=lambda: self.objeto_base.nuevaTabla())
        menubar.add_cascade(label="Archivo", menu=menu_archivo)


        self.tree = ttk.Treeview(self.master, height=10, columns=("#0", "#1","#2","#3")) # Agregué el "self.master"
        
        self.tree.tag_configure('Ingreso', background='green')
        self.tree.tag_configure('Egreso', background='red')
        
        self.tree.place(x=30, y=130)
        self.tree.column("#0", width=60)
        self.tree.column("#1", width=80)
        self.tree.column("#2", width=80)
        self.tree.column("#3", width=80)
        self.tree.column("#4", width=120)
        self.tree.heading("#0", text="Id", anchor="center")
        self.tree.heading("#1", text="Fecha", anchor="center")
        self.tree.heading("#2", text="Tipo", anchor="center")
        self.tree.heading("#3", text="Monto", anchor="center")
        self.tree.heading("#4", text="Descripcion", anchor="center")


        
        fecha1 = Label(self.master, text="Fecha: ")
        fecha1.grid(row=1, column=0)
        entryfecha1 = DateEntry(self.master, width=20, date_pattern='dd-mm-yyyy')
        entryfecha1.grid(row=1, column=1)
        fecha = entryfecha1.get_date().strftime('%d-%m-%Y')
        print(fecha)

        tipo1 = Label(self.master, text="Tipo: ")
        tipo1.grid(row=2, column=0)
        entrytipo1 = ttk.Combobox(self.master, values=["Ingreso", "Egreso"], textvariable=self.tipo, width=20)
        entrytipo1.grid(row=2, column=1, padx=5)
        
        monto1 = Label(self.master, text="Monto: ")
        monto1.grid(row=3, column=0)
        entrymonto1 = Entry(self.master, textvariable=self.monto, width=23)
        entrymonto1.grid(row=3, column=1, padx=5)
        
        descripcion1 = Label(self.master, text="Descripcion: ")
        descripcion1.grid(row=4, column=0)
        entrydescripcion1 = Entry(self.master, textvariable=self.descripcion, width=23)
        entrydescripcion1.grid(row=4, column=1, padx=5)

        # Acá agregamos el "modelobagnato." y saco los .get para poder mandar variables de tkinter y no de python... Los () me permiten pasar parámetros
        botonagregar = Button(self.master,text="Agregar", width=10, command=lambda: self.objeto_base.agregar(entryfecha1.get_date().strftime('%d-%m-%Y'),self.tipo,self.monto,self.descripcion,self.tree))
        botonagregar.grid(row=1, column=3, padx=20)
        
        botonmostrar = Button(self.master,text="Actualizar",width=10,command=lambda: self.objeto_base.mostrar(self.tree))
        botonmostrar.grid(row=2, column=3, padx=20)
        
        botonmodificar = Button(self.master, text="Editar", width=10, command=lambda: self.objeto_base.modificar(entryfecha1.get_date().strftime('%d-%m-%Y'),self.tipo,self.monto,self.descripcion,self.tree))
        botonmodificar.grid(row=3, column=3, padx=20)
        
        botonborrar = Button(self.master,text="Eliminar", width=10, command=lambda: self.objeto_base.borrar(self.tree))
        botonborrar.grid(row=4, column=3, padx=20)
        ###########################################################################################
        
        ###########################################################################################
    
        
