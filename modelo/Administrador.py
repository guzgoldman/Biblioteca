from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Session
from sqlalchemy.exc import IntegrityError
from db.Conector import Base
import hashlib

class Administrador(Base):
    __tablename__ = "administradores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dni = Column(Integer, unique=True, nullable=False, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)

    # Relación con préstamos
    prestamos = relationship("Prestamo", back_populates="administrador")

    def __repr__(self):
        return f"<Administrador dni={self.dni} nombre={self.nombre} apellido={self.apellido}>"

    def verificar_password(self, password: str) -> bool:
        """Verifica si el password proporcionado coincide con el hash almacenado."""
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        print(self.password, password_hash)
        return self.password == password_hash

    @classmethod
    def crear(cls, session: Session, dni: str, nombre: str, apellido: str, password: str, *, commit: bool = False) -> "Administrador":
        """Crea un administrador nuevo. Lanza ValueError si el DNI ya existe."""
        dni = (dni or "").strip()
        nombre = (nombre or "").strip()
        apellido = (apellido or "").strip()
        password = (password or "").strip()

        if not dni or not nombre or not apellido or not password:
            raise ValueError("DNI, Nombre, Apellido y Password son obligatorios")

        existente = session.query(cls).filter_by(dni=dni).one_or_none()
        if existente:
            raise ValueError(f"Ya existe un administrador con DNI {dni}")

        # Hashear el password usando SHA-256
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

        user = cls(dni=dni, nombre=nombre, apellido=apellido, password=password_hash)
        session.add(user)

        if commit:
            try:
                session.commit()
                session.refresh(user)
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"El DNI {dni} ya existe (UNIQUE).") from e

        return user