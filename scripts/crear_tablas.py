from db.Conector import Base, engine
from modelo import Libro, Ejemplar, Prestamo, Usuario, Historial

Base.metadata.create_all(bind=engine)