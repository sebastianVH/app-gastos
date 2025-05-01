import sqlite3
import tkinter as tk
from tkinter import ttk

class MyApp:
    def __init__(self):
        self.db_name = 'mi_basededatos.db'
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        self.root = tk.Tk()
        self.root.title("Mi aplicación")

        # Crear el combobox con las opciones de las bases de datos
        self.combo_db = ttk.Combobox(self.root, values=self.get_database_list())
        self.combo_db.grid(row=0, column=0, padx=5, pady=5)
        self.combo_db.current(0) # selecciona el primer valor por defecto

        # Crear botón para cambiar la base de datos
        self.btn_change_db = tk.Button(self.root, text="Cambiar Base de Datos", command=self.change_database)
        self.btn_change_db.grid(row=0, column=1, padx=5, pady=5)

        self.root.mainloop()

    def get_database_list(self):
        # Obtener la lista de las bases de datos disponibles
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cursor.fetchall()
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
