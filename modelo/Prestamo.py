from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, Session
from db.Conector import Base
from modelo import Ejemplar, Usuario

class Prestamo(Base):
    __tablename__ = "prestamos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ejemplar_id = Column(Integer, ForeignKey("ejemplares.id", ondelete="RESTRICT"), nullable=False, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="RESTRICT"), nullable=False, index=True)
    fecha_prestamo = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    fecha_devolucion = Column(DateTime(timezone=True), nullable=True)

    ejemplar = relationship("Ejemplar", back_populates="prestamos")
    usuario = relationship("Usuario", back_populates="prestamos")

    def __repr__(self):
        return f"<Prestamo id={self.id} ejemplar_id={self.ejemplar_id} usuario_id={self.usuario_id}>"

    @classmethod
    def crear(cls, session: Session, ejemplar: Ejemplar, usuario: Usuario):
        """Genera un préstamo si el ejemplar está disponible"""
        if not ejemplar.disponible:
            raise ValueError("El ejemplar no está disponible para préstamo")

        ejemplar.disponible = False
        session.add(ejemplar)

        prestamo = cls(ejemplar=ejemplar, usuario=usuario)
        session.add(prestamo)
        return prestamo

    def devolver(self, session: Session):
        """Marca el préstamo como devuelto y libera el ejemplar"""
        if self.fecha_devolucion is not None:
            raise ValueError("Este préstamo ya fue devuelto")

        self.fecha_devolucion = func.now()
        self.ejemplar.disponible = True

        session.add(self)
        session.add(self.ejemplar)