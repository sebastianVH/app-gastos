from tkinter import Tk,ttk
import tkinter as tk

import vista,modelo


# Mi controlador puede pasarle mi ventana a ventanita. Lo que crea la parte visual...

class Controller:
    def __init__(self, main):
        self.main_Controller = main
        self.objeto_vista = vista.Vista(self.main_Controller) 


# Acá abajo genero una ventana de Tkinter

if __name__ == "__main__":
    main_tk = Tk()
    aplicacion = Controller(main_tk)
    main_tk.mainloop()

