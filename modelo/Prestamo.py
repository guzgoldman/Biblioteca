from sqlalchemy.exc import IntegrityError
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, func, select
from sqlalchemy.orm import relationship, Session
from db.Conector import Base
from modelo import Ejemplar, Socio

class Prestamo(Base):
    __tablename__ = "prestamos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ejemplar_id = Column(String, ForeignKey("ejemplares.codigo", ondelete="RESTRICT"), nullable=False, index=True)
    socio_id = Column(Integer, ForeignKey("socios.dni", ondelete="RESTRICT"), nullable=False, index=True)
    administrador_id = Column(Integer, ForeignKey("administradores.dni", ondelete="RESTRICT"), nullable=False, index=True)
    fecha_prestamo = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    fecha_devolucion_pactada = Column(DateTime(timezone=True), nullable=False)
    fecha_devolucion = Column(DateTime(timezone=True), nullable=True)

    ejemplar = relationship("Ejemplar", back_populates="prestamos")
    socio = relationship("Socio", back_populates="prestamos")
    administrador = relationship("Administrador", back_populates="prestamos")

    def __repr__(self):
        return f"<Prestamo id={self.id} ejemplar_id={self.ejemplar_id} socio_id={self.socio_id} admin_id={self.administrador_id}>"

    @classmethod
    def crear(cls, session: Session, ejemplar_id: int, socio_id: int, administrador_id: int, dias_prestamo: int, *, commit: bool = False) -> "Prestamo":
        """Genera un préstamo si el ejemplar está disponible. Calcula la fecha de devolución basándose en los días especificados."""
        from modelo.Ejemplar import Ejemplar
        from modelo.Socio import Socio
        from modelo.Administrador import Administrador
        from datetime import datetime, timedelta

        # Validar días de préstamo
        if dias_prestamo < 1:
            raise ValueError("Los días de préstamo deben ser mayor a 0")
        if dias_prestamo > 30:
            raise ValueError("No se pueden prestar libros por más de 30 días")

        # Verificar existencia y disponibilidad
        ejemplar = session.query(Ejemplar).filter_by(id=ejemplar_id).one_or_none()
        if not ejemplar:
            raise ValueError(f"No existe un ejemplar con ID {ejemplar_id}")
        if not ejemplar.disponible:
            raise ValueError("El ejemplar no está disponible para préstamo")

        socio = session.query(Socio).filter_by(id=socio_id).one_or_none()
        if not socio:
            raise ValueError(f"No existe un socio con ID {socio_id}")

        administrador = session.query(Administrador).filter_by(id=administrador_id).one_or_none()
        if not administrador:
            raise ValueError(f"No existe un administrador con ID {administrador_id}")

        # Calcular fechas
        fecha_prestamo = datetime.now()
        fecha_devolucion_pactada = fecha_prestamo + timedelta(days=dias_prestamo)

        # Marcar ejemplar como no disponible
        ejemplar.marcar_como_prestado(session)

        # Crear un único préstamo correctamente vinculado
        prestamo = cls(
            ejemplar_id=ejemplar_id,
            socio_id=socio_id,
            administrador_id=administrador_id,
            fecha_prestamo=fecha_prestamo,
            fecha_devolucion_pactada=fecha_devolucion_pactada,
            ejemplar=ejemplar,
            socio=socio,
            administrador=administrador
        )
        session.add(prestamo)

        if commit:
            try:
                session.commit()
                session.refresh(prestamo)
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Error al crear el préstamo: {str(e)}") from e

        return prestamo


    def devolver(self, session: Session, administrador_id: int = None, *, commit: bool = False) -> "Prestamo":
        """Marca el préstamo como devuelto y libera el ejemplar"""
        from datetime import datetime
        
        if self.fecha_devolucion is not None:
            raise ValueError("Este préstamo ya fue devuelto")

        # Registrar fecha de devolución
        self.fecha_devolucion = datetime.now()
        
        # Marcar el ejemplar como disponible
        self.ejemplar.marcar_como_disponible(session)

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
        
        if commit:
            try:
                session.commit()
                session.refresh(self)
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Error al devolver el préstamo: {str(e)}") from e
        
        return self
    
    @classmethod
    def buscar_por_id(cls, session: Session, prestamo_id: int) -> "Prestamo":
        """Busca un préstamo por ID."""
        prestamo = session.query(cls).filter_by(id=prestamo_id).one_or_none()
        if not prestamo:
            raise ValueError(f"No existe un préstamo con ID {prestamo_id}")
        return prestamo
    
    @classmethod
    def listar_por_socio(cls, session: Session, socio_id: int) -> list["Prestamo"]:
        """Lista todos los préstamos de un socio."""
        return session.query(cls).filter_by(socio_id=socio_id).order_by(cls.fecha_prestamo.desc()).all()
    
    @classmethod
    def listar_activos_por_socio(cls, session: Session, socio_id: int) -> list["Prestamo"]:
        """Lista los préstamos activos (no devueltos) de un socio."""
        return session.query(cls).filter_by(socio_id=socio_id, fecha_devolucion=None).order_by(cls.fecha_prestamo.desc()).all()
    
    @classmethod
    def listar_por_administrador(cls, session: Session, administrador_id: int) -> list["Prestamo"]:
        """Lista todos los préstamos realizados por un administrador."""
        return session.query(cls).filter_by(administrador_id=administrador_id).order_by(cls.fecha_prestamo.desc()).all()
    
    @classmethod
    def listar_vencidos(cls, session: Session) -> list["Prestamo"]:
        """Lista los préstamos vencidos (no devueltos y fecha pactada pasada)."""
        from datetime import datetime
        return session.query(cls).filter(
            cls.fecha_devolucion == None,
            cls.fecha_devolucion_pactada < datetime.now()
        ).order_by(cls.fecha_devolucion_pactada).all()
    
    def esta_vencido(self) -> bool:
        """Verifica si el préstamo está vencido."""
        from datetime import datetime
        return self.fecha_devolucion is None and self.fecha_devolucion_pactada < datetime.now()
    
    def esta_activo(self) -> bool:
        """Verifica si el préstamo está activo (no devuelto)."""
        return self.fecha_devolucion is None
    
    def dias_restantes(self) -> int:
        """Calcula cuántos días quedan para la devolución. Retorna número negativo si está vencido."""
        from datetime import datetime
        if self.fecha_devolucion is not None:
            return 0  # Ya fue devuelto
        
        dias_restantes = (self.fecha_devolucion_pactada.date() - datetime.now().date()).days
        return dias_restantes
    
    def dias_prestamo_originales(self) -> int:
        """Calcula cuántos días de préstamo se pactaron originalmente."""
        return (self.fecha_devolucion_pactada.date() - self.fecha_prestamo.date()).days
    
    def obtener_resumen(self) -> dict:
        """Retorna un resumen completo del préstamo para mostrar en la interfaz."""
        return {
            'id': self.id,
            'libro_titulo': self.ejemplar.libro.titulo if self.ejemplar and self.ejemplar.libro else "N/A",
            'libro_autor': self.ejemplar.libro.autor if self.ejemplar and self.ejemplar.libro else "N/A",
            'ejemplar_codigo': self.ejemplar.codigo if self.ejemplar else "N/A",
            'socio_nombre': f"{self.socio.nombre} {self.socio.apellido}" if self.socio else "N/A",
            'socio_dni': self.socio.dni if self.socio else "N/A",
            'administrador_nombre': f"{self.administrador.nombre} {self.administrador.apellido}" if self.administrador else "N/A",
            'fecha_prestamo': self.fecha_prestamo.strftime('%d/%m/%Y') if self.fecha_prestamo else "N/A",
            'fecha_devolucion_pactada': self.fecha_devolucion_pactada.strftime('%d/%m/%Y') if self.fecha_devolucion_pactada else "N/A",
            'fecha_devolucion': self.fecha_devolucion.strftime('%d/%m/%Y') if self.fecha_devolucion else None,
            'dias_prestamo_originales': self.dias_prestamo_originales(),
            'dias_restantes': self.dias_restantes() if self.esta_activo() else 0,
            'esta_activo': self.esta_activo(),
            'esta_vencido': self.esta_vencido(),
            'estado': 'Devuelto' if not self.esta_activo() else ('Vencido' if self.esta_vencido() else 'Activo')
        }