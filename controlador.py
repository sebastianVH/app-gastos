from tkinter import Tk,ttk
import tkinter as tk
from peewee import *

import vista,modelo

# Mi controlador puede pasarle mi ventana a ventanita. Lo que crea la parte visual...

class Controller:
    def __init__(self, main):
        self.main_controller = main
        self.objeto_base = modelo.Abmc()                                              
        self.objeto_vista = vista.Vista(self.main_controller,self.objeto_base) # Le paso el controlador a la vista
        self.select_database()

    def select_database(self):
        database = self.objeto_base.select_database()
        if not database:
            self.main_controller.quit()
            return
        db = SqliteDatabase(database)
        self.objeto_base.conn = db.connect()
        self.objeto_base.cursor = db.cursor()
        modelo.Tabla._meta.database = db
        db.create_tables(modelo.Tabla)
        self.objeto_base.actualizar_tree(self.objeto_vista.tree)


# Acá abajo genero una ventana de Tkinter

if __name__ == "__main__":
    main_tk = Tk()
    aplicacion = Controller(main_tk)
    main_tk.mainloop()

