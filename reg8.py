import re

class Validar():
    def __init__(self, producto):
        self.producto = producto

    def analizar(self, producto):
        patron = "^\S[A-Za-záéíóú]*$"
        assert re.match(patron, producto)