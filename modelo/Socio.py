from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Session
from sqlalchemy.exc import IntegrityError
from db.Conector import Base

class Socio(Base):
    __tablename__ = "socios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dni = Column(String(20), unique=True, nullable=False, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    direccion = Column(String(255), nullable=False)

    prestamos = relationship("Prestamo", back_populates="socio", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Socio dni={self.dni} nombre={self.nombre} apellido={self.apellido}>"

    @classmethod
    def crear(cls, session: Session, dni: str, nombre: str, apellido: str, *, commit: bool = False) -> "Socio":
        """Crea un socio nuevo. Lanza ValueError si el DNI ya existe."""
        dni = (dni or "").strip()
        nombre = (nombre or "").strip()
        apellido = (apellido or "").strip()

        if not dni or not nombre or not apellido:
            raise ValueError("dni, nombre y apellido son obligatorios")

        existente = session.query(cls).filter_by(dni=dni).one_or_none()
        if existente:
            raise ValueError(f"Ya existe un socio con DNI {dni}")

        user = cls(dni=dni, nombre=nombre, apellido=apellido)
        session.add(user)

        if commit:
            try:
                session.commit()
                session.refresh(user)
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"El DNI {dni} ya existe (UNIQUE).") from e

        return user

    @classmethod
    def obtener_por_dni(cls, session: Session, dni: str) -> "Socio | None":
        return session.query(cls).filter_by(dni=dni.strip()).one_or_none()

    @classmethod
    def get_or_create(cls, session: Session, dni: str, nombre: str, apellido: str, *, commit: bool = False) -> "Socio":
        """Devuelve el socio si existe; si no, lo crea."""
        user = cls.obtener_por_dni(session, dni)
        if user:
            return user
        return cls.crear(session, dni, nombre, apellido, commit=commit)