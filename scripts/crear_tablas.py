from db.Conector import Base, engine
from modelo import Libro, Ejemplar, Prestamo, Socio, Administrador, Categoria, LibroCategoria, Historial

Base.metadata.create_all(bind=engine)