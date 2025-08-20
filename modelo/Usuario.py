class Usuario:

    def __init__(self, dni, nombre, apellido):
        self.dni=dni
        self.nombre=nombre
        self.apellido=apellido

    def __str__(self):
        return f"DNI: {self.dni}, Nombre: {self.nombre}, Apellido: {self.apellido}"
