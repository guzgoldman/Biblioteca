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

    def buscar_por_titulo(self, titulo):
        actual=self.cabeza
        while actual:
            if actual.dato.titulo.lower()== titulo.lower():
                return actual.dato
            actual=actual.siguiente
            return None
        

