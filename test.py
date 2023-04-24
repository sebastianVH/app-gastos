import tkinter as tk
import sqlite3
from tkinter import messagebox

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ejemplo de creación de base de datos")
        
        # Botón para crear una nueva base de datos
        self.btn_new_db = tk.Button(self, text="Crear nueva base de datos", command=self.create_new_db)
        self.btn_new_db.pack(pady=10)

    def create_new_db(self):
        # Crear una nueva ventana
        self.new_window = tk.Toplevel(self)
        self.new_window.title("Crear nueva base de datos")
        
        # Etiqueta y entrada de texto para el nombre de usuario
        tk.Label(self.new_window, text="Ingrese un nombre de usuario:").grid(row=0, column=0, padx=5, pady=5)
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
        
        # Cerrar la ventana de ingreso de nombre de usuario
        self.new_window.destroy()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
