from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from db.Conector import Base

class Historial(Base):
    __tablename__ = "historial"

    id = Column(Integer, primary_key=True, autoincrement=True)
    accion = Column(String(50), nullable=False)
    detalle = Column(Text, nullable=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    prestamo_id  = Column(Integer, ForeignKey("prestamos.id", ondelete="SET NULL"), nullable=True)
    ejemplar_id  = Column(Integer, ForeignKey("ejemplares.id", ondelete="SET NULL"), nullable=True)
    socio_id   = Column(Integer, ForeignKey("socios.id",  ondelete="SET NULL"), nullable=True)

    prestamo = relationship("Prestamo")
