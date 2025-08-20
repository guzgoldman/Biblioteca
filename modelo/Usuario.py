from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.Conector import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dni = Column(String(20), unique=True, nullable=False, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)

    # Relación 1:N con Prestamo
    prestamos = relationship("Prestamo", back_populates="usuario", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Usuario dni={self.dni} nombre={self.nombre} apellido={self.apellido}>"
