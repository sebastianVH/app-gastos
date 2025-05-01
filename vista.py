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
from controlador import Controller

class Vista():
    def __init__(self, main: Controller , objeto_base: Abmc):
        # self.modelo=Model()
        self.master = main 
        self.objeto_base = objeto_base
        self.tree = ttk.Treeview(self.master, height=20, columns=("#0", "#1","#2","#3","#4")) # Agregué el "self.master"
        
        # Para tener un retorno en la vista, agregamos:
        
        self.master.title(f"Control de gastos - {self.objeto_base.db}")
        self.master.geometry("550x650")

        # Variables: 
        self.fecha = DateEntry()
        self.tipo = StringVar()
        self.moneda = StringVar()
        self.monto = DoubleVar()
        self.descripcion = StringVar()
        
        menubar = Menu(self.master)
        self.master.config(menu=menubar)
        menu_archivo = Menu(menubar, tearoff=0)
        
        menu_archivo.add_command(label="Crear nueva plantilla", command=lambda: self.objeto_base.nueva_db(self.master))
        menu_archivo.add_command(label="Cambiar plantilla", command=lambda: self.objeto_base.cambiar_db(self.tree,self.master))
        menu_archivo.add_command(label="Eliminar plantilla de datos", command=lambda: self.objeto_base.eliminar_bd(self.tree))
        menu_archivo.add_command(label="Salir", command=lambda: self.objeto_base.salir(self.master))
        menubar.add_cascade(label="Archivo", menu=menu_archivo)

        
        self.tree.tag_configure('Ingreso', background='green')
        self.tree.tag_configure('Egreso', background='red')
        
        self.tree.place(x=30, y=145)
        self.tree.column("#0", width=40)
        self.tree.column("#1", width=80)
        self.tree.column("#2", width=60)
        self.tree.column("#3", width=60)
        self.tree.column("#4", width=160)
        self.tree.column("#5", width=60)
        self.tree.heading("#0", text="Id", anchor="center")
        self.tree.heading("#1", text="Fecha", anchor="center")
        self.tree.heading("#2", text="Tipo", anchor="center")
        self.tree.heading("#3", text="Monto", anchor="center")
        self.tree.heading("#4", text="Descripcion", anchor="center")
        self.tree.heading("#5", text="Moneda", anchor="center")
        
        scrollbar = ttk.Scrollbar(self.master, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(x=500, y=145, height=430)
        
        fecha1 = Label(self.master, text="Fecha: ",justify="left")
        fecha1.place(x=30, y=0)
        entryfecha1 = DateEntry(self.master, width=20, date_pattern='dd-mm-yyyy')

        entryfecha1.place(x=120, y=0)
        self.fecha = entryfecha1
    
        tipo1 = Label(self.master, text="Tipo: ",justify="left")
        tipo1.place(x=30, y=30)
        entrytipo1 = ttk.Combobox(self.master, values=["Ingreso", "Egreso"], textvariable=self.tipo, width=20)
        entrytipo1.place(x=120, y=30)
        
        moneda1 = Label(self.master, text="Moneda: ",justify="left")
        moneda1.place(x=30, y=120)
        entrymoneda1 = ttk.Combobox(self.master, values=["ARS", "USD"], textvariable=self.moneda, width=20)
        entrymoneda1.place(x=120, y=120)
        
        monto1 = Label(self.master, text="Monto: ",justify="left")
        monto1.place(x=30, y=60)
        entrymonto1 = Entry(self.master, textvariable=self.monto, width=23)
        entrymonto1.grid(row=3, column=2)
        entrymonto1.place(x=120, y=60)
        
        descripcion1 = Label(self.master, text="Descripcion: ",justify="left")
        descripcion1.place(x=30, y=90)
        entrydescripcion1 = Entry(self.master, textvariable=self.descripcion, width=23)
        entrydescripcion1.place(x=120, y=90)
        
        balance_pesos_label = Label(self.master, text="Balance ARS: 0.00")
        balance_pesos_label.place(x=30, y=590) # o utiliza el método grid() si lo prefieres
        balance_dolares_label = Label(self.master, text="Balance USD: 0.00")
        balance_dolares_label.place(x=30, y=610) # o utiliza el método grid() si lo prefieres

        botonagregar = Button(self.master,text="Agregar", width=10, command=lambda: self.objeto_base.agregar(self.fecha,self.tipo,self.monto,self.descripcion, self.moneda, self.tree, balance_pesos_label, balance_dolares_label))
        botonagregar.place(x=370, y=0)
        
        botonmostrar = Button(self.master,text="Actualizar",width=10,command=lambda: self.objeto_base.mostrar(self.tree, balance_pesos_label, balance_dolares_label))
        botonmostrar.place(x=370, y=30)
        
        botonmodificar = Button(self.master, text="Editar", width=10, command=lambda: self.objeto_base.modificar(self.fecha,self.tipo,self.monto,self.descripcion, self.moneda ,self.tree, balance_pesos_label, balance_dolares_label))
        botonmodificar.place(x=370, y=60)
        
        botonborrar = Button(self.master,text="Eliminar", width=10, command=lambda: self.objeto_base.borrar(self.tree, balance_pesos_label, balance_dolares_label))
        botonborrar.place(x=370, y=90)
        ###########################################################################################
        self.tree.bind("<<TreeviewSelect>>", lambda event: self.autocompletar_campos())
        ###########################################################################################
    def autocompletar_campos(self):
        self.tree.unbind("<<TreeviewSelect>>")
        try:
            selected_item = self.tree.selection()  # Obtener la fila seleccionada
            if not selected_item:
                return
                # Obtener los valores de la fila seleccionada
            item = self.tree.item(selected_item[0])
            valores = item['values']  # Lista con los valores de la fila
            fecha = datetime.strptime(valores[0], '%d-%m-%Y')  # Convertir la fecha a un objeto datetime
            self.fecha.set_date(fecha) # Fecha
            self.tipo.set(valores[1])        # Tipo (Ingreso/Egreso)
            self.monto.set(valores[2])       # Monto
            self.descripcion.set(valores[3]) # Descripción
            self.moneda.set(valores[4])       # Moneda (Pesos/Dólares)
        finally:
            self.tree.bind("<<TreeviewSelect>>", lambda event: self.autocompletar_campos())

