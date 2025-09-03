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
    
    def buscar_libro_por_autor(self, autor):
        return self.catalogo_libros.buscar_por_autor(autor)
        
    def buscar_libro_por_codigo(self, codigo):
        return self.catalogo_libros.buscar_por_codigo(codigo)
    
    def buscar_usuario_por_dni(self, dni):
        return self.lista_usuarios.buscar_por_dni(dni)
    
    def buscar_usuario_por_nombre(self, nombre):
        return self.lista_usuarios.buscar_por_nombre(nombre)
    
    def buscar_usuario_por_apellido(self, apellido):
        return self.lista_usuarios.buscar_por_apellido(apellido)
            
    def prestar_libro(self, codigo_libro, dni_usuario):
        libro = self.catalogo_libros.buscar_por_codigo(codigo_libro)
        usuario = self.lista_usuarios.buscar_por_dni(dni_usuario)
        
        # Validaciones
        if not libro:
            print("El libro no existe en el sistema.")
            return False
        if not usuario:
            print("El usuario no se encuentra registrado.")
            return False
        if not libro.disponible:
            print(f"El libro '{libro.titulo}' no se encuentra disponible.")
            return False
        
        # Se realiza el préstamo y se actualiza el estado
        libro.disponible = False
        nuevo_prestamo = Prestamo(libro, usuario)
        
        # Se apila la operación en el historial
        self.Historial_Prestamos.apilar(nuevo_prestamo)
        
        print(f"El libro '{libro.titulo}' fue prestado con éxito a '{usuario.nombre}'.")
        return True
    
    def devolver_libro(self, codigo_libro):
        libro = self.catalogo_libros.buscar_por_codigo(codigo_libro)
        
        # Validaciones
        if not libro:
            print("El libro no existe en el sistema.")
            return False
        
        if libro.disponible:
            print(f"El libro '{libro.titulo}' ya se encuentra disponible.")
            return False
        
        # Se realiza la devolución y se actualiza el estado
        libro.disponible = True
        
        # Se apila la devolución
        self.Historial_Prestamos.apilar(("DEVOLUCION", libro))
        
        print(f"El libro '{libro.titulo}' fue devuelto con éxito.")
        return True
        
    def deshacer_ultima_accion(self):
        """
        Revierte la última acción (préstamo o devolución) usando la pila LIFO.
        """
        if self.Historial_Prestamos.esta_vacia():
            print("No hay operaciones para deshacer.")
            return False
        
        ultima_operacion = self.Historial_Prestamos.desapilar()
        
        # Si la operación es una instancia de la clase Prestamo, revierte el préstamo.
        if isinstance(ultima_operacion, Prestamo):
            libro_afectado = ultima_operacion.libro
            libro_afectado.disponible = True
            print(f"La última operación (préstamo de '{libro_afectado.titulo}') ha sido deshecha. El libro ahora está disponible.")
        
        # Si la operación es una tupla ("DEVOLUCION", libro), revierte la devolución.
        elif isinstance(ultima_operacion, tuple) and ultima_operacion[0] == "DEVOLUCION":
            libro_afectado = ultima_operacion[1]
            libro_afectado.disponible = False
            print(f"La última operación (devolución de '{libro_afectado.titulo}') ha sido deshecha. El libro ahora está prestado.")
       