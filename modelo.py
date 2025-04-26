import datetime
from tkinter.messagebox import showerror,showinfo,askyesno
from tkinter import messagebox, filedialog
import tkinter as tkint

from peewee import SqliteDatabase, Model, CharField, FloatField, DateField, AutoField


############################ Declaro BASE:
class BaseModel(Model):
    pass

############################ Declaro TABLA:
class Tabla(BaseModel):
    
    id= AutoField() # Agregué el campo id
    fecha=DateField()
    tipo = CharField() # Esto es una restricción para que no se repitan los títulos.
    monto = FloatField()
    descripcion = CharField(max_length=100)

tables=[Tabla]


############################ CRUD:

class Abmc():
    def __init__(self) -> None:
        self.conn = None
        self.db = None
        self.cursor = None
        
    def agregar(self, fecha,tipo,monto,descripcion,tree,balance_label):
        
        try:
            tabla = Tabla()

            tabla.fecha = fecha.get_date().strftime('%d-%m-%Y')
            tabla.tipo = tipo.get()
            tabla.monto = monto.get()
            tabla.descripcion = descripcion.get()
            if not tipo.get() or not monto.get() or not descripcion.get():
                return self.mensaje_revisar()
            tabla.save()
            
            tree.insert("", "end", values=(tabla.fecha,tabla.tipo,tabla.monto,tabla.descripcion),tags=(tabla.tipo,))
            self.mensaje_alta()
            self.vaciarcampos(tipo,monto,descripcion,fecha)
            self.calcular_balance(tree,balance_label)
            self.actualizar_tree(tree)
        except:
            pass

    def borrar(self, tree,balance_label):
        fila = tree.selection()
        if not fila:
            self.mensaje_fila()# Si no selecciona una fila, le aviso que seleccione una fila
            return
        item = tree.item(fila)
        borrar = Tabla.get(Tabla.id == item["text"]) 
        if askyesno("Atención", "¿Desea confirmar?"):
            borrar.delete_instance()
            tree.delete(fila)
            self.mensaje_borrar()
        self.calcular_balance(tree,balance_label)
        self.actualizar_tree(tree)

    def actualizar_tree(self, treeview):
        # Borrado en la tabla:
        registros = treeview.get_children()
        for elemento in registros:
            treeview.delete(elemento)
        # Extraigo datos:
        for row in Tabla.select(): # Esto me traerá todo lo que tenga la tabla
            treeview.insert("", "end", text=row.id, values=(row.fecha,row.tipo,row.monto,row.descripcion),tags=(row.tipo))
        
        
    def mostrar(self, tree, balance_label):
        self.actualizar_tree(tree)
        self.calcular_balance(tree,balance_label)

    def modificar(self, fecha,tipo,monto,descripcion, tree,balance_label): # Tuve que agregar producto y precio acá
        fila = tree.selection()
        if not fila:
            self.mensaje_fila()# Si no selecciona una fila, le aviso que seleccione una fila
            return
        registros = tree.item(fila)
        mi_id = registros["text"]
        actualizar = Tabla.update(fecha = fecha.get_date().strftime('%d-%m-%Y'), tipo = tipo.get(), monto = monto.get(),descripcion = descripcion.get()).where(Tabla.id == mi_id)
        if askyesno("Atencion","¿Desea confirmar la modificacion?"):
            actualizar.execute()
            self.mensaje_modificar()
            self.actualizar_tree(tree)
            self.calcular_balance(tree,balance_label)
        self.vaciarcampos(tipo,monto,descripcion,fecha)

    def vaciarcampos(self,tipo,monto,descripcion,fecha):
        tipo.set("")
        monto.set("")
        descripcion.set("")
        today = datetime.datetime.now().strftime("%d-%m-%Y") # Cambié el formato de la fecha
        fecha.set_date(today)

    def salir(self,master):
        if askyesno("Atención", "¿Desea salir?"):
            master.quit() # cambié el "quit" por el "destroy" 

    def eliminar_bd(self, tree): # Intento definir el "eliminar_bd"
        if askyesno("Atencion","Desea borrar la planilla de datos?"):
            #db.drop_tables(Tabla) # se elimina la tabla directamente de la planilla de datos
            Tabla.truncate_table() #con truncate, borramos todos los registros de la tabla
            self.mensaje_eliminarbd() 
            self.actualizar_tree(tree)
    
    def nueva_db(self):
        self.new_window = tkint.Toplevel()
        self.new_window.title("Crear nueva planilla de datos")
        
        # Etiqueta y entrada de texto para el nombre de usuario
        tkint.Label(self.new_window, text="Ingrese un nombre de la planilla:").grid(row=0, column=0, padx=5, pady=5)
        self.user_entry = tkint.Entry(self.new_window)
        self.user_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Botón para crear la planilla de datos con el nombre ingresado
        tkint.Button(self.new_window, text="Crear planilla de datos", command=self.create_db_with_username).grid(row=1, column=1, padx=5, pady=5)      
    
    def create_db_with_username(self):
        user_input = self.user_entry.get()

        if not user_input:
            messagebox.showerror("Error", "Debe ingresar un nombre a su Database")
            return
        # Crear la conexión a la planilla de datos con el nombre de usuario ingresado
        try:
            self.db = SqliteDatabase(f"{user_input}.db")
            self.conn = self.db.connect(f"{user_input}.db")
            Tabla._meta.database = self.db
            self.db.create_tables([Tabla])
            messagebox.showinfo("planilla de datos creada", f"Se ha creado la planilla de datos {user_input}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear la planilla de datos: {str(e)}")
        self.new_window.destroy()
        
    def cambiar_db(self, tree):
        pathfile = self.select_database()
        if not pathfile:
            return
        if not pathfile.endswith('.db'):
            messagebox.showerror("Error", "El archivo seleccionado no es una planilla de datos válida. (finaliza en .db)")
            return
        if self.conn:
            self.db = SqliteDatabase(pathfile)
            self.conn = self.db.connect()
            self.cursor = self.db.cursor()
            Tabla._meta.database = self.db
            self.db.create_tables(Tabla)
            messagebox.showinfo("Cambio de planilla de datos", f"Se ha cambiado a la planilla de datos: {pathfile.split('/')[-1]}")
            self.actualizar_tree(tree)

    def select_database(self) -> None:

        file_path = filedialog.askopenfilename(
            title="Seleccionar planilla de datos",
            filetypes=[("Archivos de planilla de datos", "*.db")]
        )
        if not file_path:
            messagebox.showerror("Error", "No se seleccionó ningún archivo.")
            return None
        if not file_path.endswith('.db'):
            messagebox.showerror("Error", "El archivo seleccionado no es una planilla de datos válida.")
            return None
        return file_path
        
    def calcular_balance(self,tree,balance_label):
        ingresos = 0.0
        egresos = 0.0
        for item in tree.get_children():
            tags = tree.item(item)['tags']
            if 'Ingreso' in tags:
                ingresos += float(tree.item(item)['values'][2])
            elif 'Egreso' in tags:
                egresos += float(tree.item(item)['values'][2])
        balance = ingresos - egresos
        balance_label.config(text=f"Balance: {balance:.2f}")
    
    @staticmethod
    def mensaje_alta():
       showinfo("Atencion","Ingreso realizado con éxito")

    @staticmethod
    def mensaje_borrar():
       showinfo("Atencion","Registro eliminado con éxito")

    @staticmethod
    def mensaje_modificar():
       showinfo("Atencion","Registro modificado con éxito")

    @staticmethod
    def mensaje_eliminarbd():
       showinfo("Atencion","planilla de datos eliminada")
    
    @staticmethod
    def mensaje_revisar():
       showerror("Atencion","Revise los campos que ingreso")
        
    @staticmethod
    def mensaje_fila():
       showerror("Atencion","Seleccione una fila")

