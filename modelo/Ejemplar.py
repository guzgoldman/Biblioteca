from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Session
from db.Conector import Base

class Ejemplar(Base):
    __tablename__ = "ejemplares"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(50), unique=True, nullable=False, index=True)
    disponible = Column(Boolean, nullable=False, default=True)

    libro_id = Column(Integer, ForeignKey("libros.id", ondelete="RESTRICT"), nullable=False, index=True)
    libro = relationship("Libro", back_populates="ejemplares")

    prestamos = relationship("Prestamo", back_populates="ejemplar")

    def __repr__(self):
        return f"<Ejemplar id={self.id} codigo={self.codigo} disponible={self.disponible}>"

    def marcar_como_prestado(self, session: Session):
        """Marca este ejemplar como no disponible"""
        if not self.disponible:
            raise ValueError("El ejemplar ya está prestado")
        self.disponible = False
        session.add(self)

    def marcar_como_disponible(self, session: Session):
        """Marca este ejemplar como disponible"""
        self.disponible = True
        session.add(self)