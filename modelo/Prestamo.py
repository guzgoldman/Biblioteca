from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from db.Conector import Base

class Prestamo(Base):
    __tablename__ = "prestamos"

    id = Column(Integer, primary_key=True, autoincrement=True)

    libro_id = Column(Integer, ForeignKey("libros.id", ondelete="RESTRICT"), nullable=False, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="RESTRICT"), nullable=False, index=True)

    fecha_prestamo = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    fecha_devolucion = Column(DateTime(timezone=True), nullable=True)

    # Relaciones
    libro = relationship("Libro", back_populates="prestamos")
    usuario = relationship("Usuario", back_populates="prestamos")

    def __repr__(self):
        return f"<Prestamo id={self.id} libro_id={self.libro_id} usuario_id={self.usuario_id}>"
