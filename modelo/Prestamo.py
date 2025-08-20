from datetime import datetime
class Prestamo:
    
    def __init__(self, libro, usuario, fechaPrestamo = datetime.datetime, fechaDevolucion = None):
        self.libro=libro
        self.usuario=usuario

    def __str__(self):
        return f"Prestamo del libro {self.libro.titulo} al usuario {self.usuario.nombre} {self.usuario.apellido} en la fecha {self.fechaPrestamo}"
