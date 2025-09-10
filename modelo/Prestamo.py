from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, select
from sqlalchemy.orm import relationship, Session
from db.Conector import Base
from modelo import Ejemplar, Socio

class Prestamo(Base):
    __tablename__ = "prestamos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ejemplar_id = Column(Integer, ForeignKey("ejemplares.id", ondelete="RESTRICT"), nullable=False, index=True)
    socio_id = Column(Integer, ForeignKey("socios.id", ondelete="RESTRICT"), nullable=False, index=True)
    fecha_prestamo = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    fecha_devolucion_pactada = Column(DateTime(timezone=True), nullable=False)
    fecha_devolucion = Column(DateTime(timezone=True), nullable=True)

    ejemplar = relationship("Ejemplar", back_populates="prestamos")
    socio = relationship("Socio", back_populates="prestamos")

    def __repr__(self):
        return f"<Prestamo id={self.id} ejemplar_id={self.ejemplar_id} socio_id={self.socio_id}>"

    @classmethod
    def crear(cls, session: Session, ejemplar: Ejemplar, socio: Socio):
        """Genera un préstamo si el ejemplar está disponible"""
        if not ejemplar.disponible:
            raise ValueError("El ejemplar no está disponible para préstamo")

        ejemplar.disponible = False
        session.add(ejemplar)

        prestamo = cls(ejemplar=ejemplar, socio=socio)
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
        
    def obtener_prestamos(self, session: Session):
        """Recupera todos los préstamos"""
        prestamos = session.execute(select(Prestamo)).scalars().all()
        return prestamos
    
    def obtener_prestamos_por_socio(self, session: Session, socio_dni: str):
        """Recupera todos los préstamos de un socio específico por su DNI"""
        prestamos = session.execute(
            select(Prestamo).join(Socio).where(Socio.dni == socio_dni)
        ).scalars().all()
        return prestamos