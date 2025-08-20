class Libro:
    def __init__(self, codigo, titulo, autor):
        self.codigo=codigo
        self.titulo=titulo
        self.autor=autor
        self.disponible = True

    def __str__(self):
        estado="Disponible" if self.disponible else "Prestado"
        return f"Codigo: {self.codigo}, Título: {self.titulo}, Autor: {self.auto}, Estado:{estado}"
