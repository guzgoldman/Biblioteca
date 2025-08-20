# scripts/crear_tablas.py (por ejemplo)
from db.Conector import Base, engine
from modelo.Libro import Libro
from modelo.Usuario import Usuario
from modelo.Prestamo import Prestamo
from modelo.Historial import Historial

Base.metadata.create_all(bind=engine)
print("Tablas creadas ✅")