from tkinter.messagebox import showerror
from tkinter.messagebox import showinfo
from tkinter.messagebox import askyesno
from tkinter import messagebox, filedialog,Toplevel,ttk
from datetime import date,datetime
from tkcalendar import DateEntry
import tkinter as tkint
from tkinter import *

from sqlite3 import *
import sqlite3
from peewee import *

from controlador import *

import re
from reg8 import Validar

db = SqliteDatabase("database.db")

############################ Declaro BASE:
class BaseModel(Model):
    class Meta:
        database = db

############################ Declaro TABLA:
class Tabla(BaseModel):
    
    id= AutoField() # Agregué el campo id
    fecha=DateField()
    tipo = CharField() # Esto es una restricción para que no se repitan los títulos.
    monto = FloatField()
    descripcion = CharField(max_length=100)

tables=[Tabla]

db.connect()
db.create_tables([Tabla])


############################ CRUD:

class Abmc():
    def __init__(self) -> None: pass
        
    def agregar(self, fecha,tipo,monto,descripcion,tree):
        
        try:
            tabla = Tabla()
            tabla.fecha = fecha
            tabla.tipo = tipo.get()
            tabla.monto = monto.get()
            tabla.descripcion = descripcion.get()
            tabla.save()
            
            tree.insert("", "end", values=(tabla.fecha,tabla.tipo,tabla.monto,tabla.descripcion),tags=(tabla.tipo,))
            self.mensaje_alta()
            self.vaciarcampos(tipo,monto,descripcion)
            self.actualizar_tree(tree)
        except:
            pass

    def borrar(self, tree):
        valor = tree.selection()
        item = tree.item(valor)
        borrar = Tabla.get(Tabla.id == item["text"]) 
        if askyesno("Atención", "¿Desea confirmar?"):
            borrar.delete_instance()
            tree.delete(valor)
        self.actualizar_tree(tree)

    def actualizar_tree(self, treeview):
        # Borrado en la tabla:
        registros = treeview.get_children()
        for elemento in registros:
            treeview.delete(elemento)
        # Extraigo datos:
        for row in Tabla.select(): # Esto me traerá todo lo que tenga la tabla "Productos"
            treeview.insert("", "end", text=row.id, values=(row.fecha,row.tipo,row.monto,row.descripcion),tags=(row.tipo))

    def mostrar(self, tree):
        self.actualizar_tree(tree)

    def modificar(self, fecha,tipo,monto,descripcion, tree): # Tuve que agregar producto y precio acá
        valor1 = tree.selection()
        registros = tree.item(valor1)
        mi_id = registros["text"]
        actualizar = Tabla.update(fecha = fecha, tipo = tipo.get(), monto = monto.get(),descripcion = descripcion.get()).where(Tabla.id == mi_id)
        if askyesno("Atencion","¿Desea confirmar la modificacion?"):
            actualizar.execute()
            self.mensaje_modificar()
            self.actualizar_tree(tree)
        self.vaciarcampos(tipo,monto,descripcion)
        # self.messagebox.showinfo("Atención", "Producto modificado con éxito")

    def vaciarcampos(self,tipo,monto,descripcion):
        tipo.set("")
        monto.set("")
        descripcion.set("")

    def salir(self,master):
        if self.askyesno("Atención", "¿Desea salir?"):
            master.quit() # cambié el "quit" por el "destroy" 

    def eliminar_bd(self, tree): # Intento definir el "eliminar_bd"
        if askyesno("Atencion","Desea borrar la base de datos?"):
            #db.drop_tables(Tabla) # se elimina la tabla directamente de la base de datos
            Tabla.truncate_table() #con truncate, borramos todos los registros de la tabla
            self.mensaje_eliminarbd() 
            self.actualizar_tree(tree)
    
    def nueva_db(self):
        self.new_window = tk.Toplevel()
        self.new_window.title("Crear nueva base de datos")
        
        # Etiqueta y entrada de texto para el nombre de usuario
        tk.Label(self.new_window, text="Ingrese un nombre de la DataBase:").grid(row=0, column=0, padx=5, pady=5)
        self.user_entry = tk.Entry(self.new_window)
        self.user_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Botón para crear la base de datos con el nombre ingresado
        tk.Button(self.new_window, text="Crear base de datos", command=self.create_db_with_username).grid(row=1, column=1, padx=5, pady=5)      
    
    def create_db_with_username(self):
        username = self.user_entry.get()
        db.create_tables([Tabla(username)])

        if not username:
            messagebox.showerror("Error", "Debe ingresar un nombre a su Database")
            return
        # Crear la conexión a la base de datos con el nombre de usuario ingresado
        try:
            conn = db.connect(f"{username}.db")
            messagebox.showinfo("Base de datos creada", f"Se ha creado la base de datos {username}.db")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo crear la base de datos: {str(e)}")
        self.new_window.destroy()
        
    def cambiar_db(self):
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()
        self.new_window = tk.Toplevel()
        self.new_window.title("Seleccion de base de datos")
        self.combo_db = ttk.Combobox(self.new_window, values=self.get_database_list())
        self.combo_db.grid(row=0, column=0, padx=5, pady=5)
        self.btn_change_db = tk.Button(self.new_window, text="Cambiar Base de Datos", command=self.change_database)
        self.btn_change_db.grid(row=0, column=1, padx=5, pady=5)

    def get_database_list(self):
        # Obtener la lista de las bases de datos disponibles
        self.cursor.execute("SELECT name FROM sqlite_master;")
        tables = self.cursor.fetchall()
        print(tables)
        database_list = []
        for table in tables:
            database_list.append(table[0].split('.')[0])
        return list(set(database_list))
    
    def change_database(self):
        # Cambiar la base de datos
        new_db_name = self.combo_db.get()
        self.conn.close()
        self.conn = sqlite3.connect(f"{new_db_name}.db")
        self.cursor = self.conn.cursor()
        messagebox.showinfo("Cambio de Base de Datos", f"Se ha cambiado a la base de datos {new_db_name}.db")
        self.new_window.destroy()
    
    @staticmethod
    def mensaje_alta():
        messagebox.showinfo("Atencion","Ingreso realizado con éxito")

    @staticmethod
    def mensaje_borrar():
        messagebox.showinfo("Atencion","Registro eliminado con éxito")

    @staticmethod
    def mensaje_modificar():
        messagebox.showinfo("Atencion","Registro modificado con éxito")

    @staticmethod
    def mensaje_eliminarbd():
        messagebox.showinfo("Atencion","Base de datos eliminada")
    
    @staticmethod
    def mensaje_revisar():
        messagebox.showerror("Atencion","Revise los campos que ingreso")

