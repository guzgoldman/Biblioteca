from modelo.Libro import Libro
from modelo.Historial import Historial
from modelo.Prestamo import Prestamo
from modelo.Administrador import Administrador
from estructuras.ListaEnlazada import ListaEnlazada
from estructuras.Pila import Pila

class SistemaBiblioteca:

    def __init__(self):
        self.catalogo_libros=ListaEnlazada()
        self.lista_socios=ListaEnlazada()
        self.lista_administradores=ListaEnlazada()
        self.Historial_Prestamos=Pila()

    def agregar_libro(self, codigo, titulo, autor):
        nuevo_libro=Libro(codigo, titulo, autor)
        self.catalogo_libros.agregar(nuevo_libro)
        print(f"El libro '{titulo}' fue agregado con éxito.")

    def agregar_usuario(self, dni, nombre, apellido):
        nuevo_usuario=Usuario(dni, nombre, apellido)
        self.lista_usuarios.agregar(nuevo_usuario)
        print(f"El usuario '{nombre}{apellido}' fue agregado con exito")
        
    def buscar_libro_por_titulo(self, titulo):
        return self.catalogo_libros.buscar_por_titulo(titulo)
    
    




