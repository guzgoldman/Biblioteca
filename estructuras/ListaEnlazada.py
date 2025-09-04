class Nodo:
    def __init__(self, dato):
        self.dato=dato
        self.siguiente=None

class ListaEnlazada:
    def __init__(self):
        self.cabeza=None

    def agregar (self, dato):
        nuevo_nodo= Nodo(dato)
        if not self.cabeza:
            self.cabeza=nuevo_nodo
        else:
            actual=self.cabeza
            while actual.siguiente:
                actual=actual.siguiente
            actual.siguiente=nuevo_nodo

# búsqueda de libros
    def buscar_por_titulo(self, titulo):
        actual=self.cabeza
        while actual:
            if actual.dato.titulo.lower()== titulo.lower():
                return actual.dato
            actual=actual.siguiente
        return None
        
    def buscar_por_autor(self, autor):
        actual = self.cabeza
        while actual:
            if actual.dato.autor.lower() == autor.lower():
                return actual.dato
            actual = actual.siguiente
        return None
    
    def buscar_por_codigo(self, codigo):
        actual = self.cabeza
        while actual:
            if actual.dato.codigo == codigo:
                return actual.dato
            actual = actual.siguiente
        return None

    # Búsqueda de usuarios
    def buscar_por_dni(self, dni):
        actual = self.cabeza
        while actual:
            if actual.dato.dni == dni:
                return actual.dato
            actual = actual.siguiente
        return None

    def buscar_por_nombre(self, nombre):
        actual = self.cabeza
        while actual:
            if actual.dato.nombre.lower() == nombre.lower():
                return actual.dato
            actual = actual.siguiente
        return None
        
    def buscar_por_apellido(self, apellido):
        actual = self.cabeza
        while actual:
            if actual.dato.apellido.lower() == apellido.lower():
                return actual.dato
            actual = actual.siguiente
        return None
