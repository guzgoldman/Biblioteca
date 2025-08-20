from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from db.Conector import Base

class Libro(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # Código de catálogo (único)
    codigo = Column(String(50), unique=True, nullable=False, index=True)
    titulo = Column(String(200), nullable=False)
    autor = Column(String(150), nullable=False)
    disponible = Column(Boolean, nullable=False, default=True)

    # Relación 1:N con Prestamo
    prestamos = relationship("Prestamo", back_populates="libro", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Libro codigo={self.codigo} titulo={self.titulo!r} disponible={self.disponible}>"
