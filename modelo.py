from tkinter.messagebox import showerror
from tkinter.messagebox import showinfo
from tkinter.messagebox import askyesno
from tkinter import messagebox
from datetime import date,datetime
from tkcalendar import DateEntry
from tkinter import Toplevel
import tkinter as tkint
from tkinter import *

from tkinter import ttk
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

db.connect()
db.create_tables([Tabla])




############################ CRUD:

class Abmc():
    def __init__(self) -> None: pass
        
    def agregar(self, fecha,tipo,monto,descripcion,tree):
        print("Fecha de la tabla:" ,fecha)
        try:
            
            tabla = Tabla()
            tabla.fecha = fecha
            tabla.tipo = tipo.get()
            tabla.monto = monto.get()
            tabla.descripcion = descripcion.get()
            tabla.save()
            
            tree.insert("", "end", values=(tabla.fecha,tabla.tipo,tabla.monto,tabla.descripcion),tags=(tabla.tipo,))
            self.mensaje_alta()
            self.vaciarcampos(fecha,tipo,monto,descripcion)
            self.actualizar_tree(tree)
            # self.messagebox.showinfo("Lista de productos", "Producto agregado con éxito")
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
        self.vaciarcampos(fecha,tipo,monto,descripcion)
        # self.messagebox.showinfo("Atención", "Producto modificado con éxito")

    def vaciarcampos(self,fecha,tipo,monto,descripcion):
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
    
    def nuevaTabla(self):
        self.new_window = tk.Toplevel(tk.Tk())
        self.new_window.title("Crear nueva base de datos")
        
        # Etiqueta y entrada de texto para el nombre de usuario
        tk.Label(self.new_window, text="Ingrese un nombre de la DataBase:").grid(row=0, column=0, padx=5, pady=5)
        self.user_entry = tk.Entry(self.new_window)
        self.user_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Botón para crear la base de datos con el nombre ingresado
        tk.Button(self.new_window, text="Crear base de datos", command=self.create_db_with_username).grid(row=1, column=1, padx=5, pady=5)      
    
    def create_db_with_username(self):
        # Obtener el nombre de usuario ingresado
        username = self.user_entry.get()

        # Validar que se haya ingresado un nombre de usuario
        if not username:
            messagebox.showerror("Error", "Debe ingresar un nombre de usuario")
            return
        # Crear la conexión a la base de datos con el nombre de usuario ingresado
        try:
            conn = sqlite3.connect(f"{username}.db")
            messagebox.showinfo("Base de datos creada", f"Se ha creado la base de datos {username}.db")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo crear la base de datos: {str(e)}")
        self.new_window.destroy()

    @staticmethod
    def mensaje_alta():
        messagebox.showinfo("Atencion","Ingreso realizado con éxito")

    @staticmethod
    def mensaje_borrar():
        messagebox.showinfo("Atencion","Registro eliminado con éxito")

    @staticmethod
    def mensaje_modificar():
        messagebox.showinfo("Atencion","Producto modificado con éxito")

    @staticmethod
    def mensaje_eliminarbd():
        messagebox.showinfo("Atencion","Base de datos eliminada")


