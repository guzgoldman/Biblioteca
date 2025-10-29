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

    prestamos = relationship(
        "Prestamo",
        back_populates="socio",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Socio dni={self.dni} nombre={self.nombre} apellido={self.apellido}>"

    # ==========================================================
    #   MÉTODOS DE CLASE
    # ==========================================================
    @classmethod
    def obtener_por_dni(cls, session: Session, dni: str) -> "Socio | None":
        """Devuelve el socio que coincida con el DNI, o None si no existe."""
        dni = (dni or "").strip()
        if not dni:
            return None

        session.expire_all()  # 🔥 fuerza a recargar desde la base real
        socio = session.query(cls).filter_by(dni=dni).one_or_none()
        print(f"[DEBUG] Buscando socio con DNI: {dni} -> {socio}")
        return socio

    @classmethod
    def crear(cls, session: Session, dni: str, nombre: str, apellido: str, *, commit: bool = False) -> "Socio":
        """Crea un socio nuevo. Lanza ValueError si el DNI ya existe."""
        dni = (dni or "").strip()
        nombre = (nombre or "").strip()
        apellido = (apellido or "").strip()

        if not dni or not nombre or not apellido:
            raise ValueError("dni, nombre y apellido son obligatorios")

        # Validar duplicado antes de crear
        existente = cls.obtener_por_dni(session, dni)
        if existente:
            raise ValueError(f"Ya existe un socio con DNI {dni}")

        socio = cls(dni=dni, nombre=nombre, apellido=apellido, direccion="")  # dirección vacía por ahora
        session.add(socio)

        if commit:
            try:
                session.flush()
                session.commit()
                session.refresh(socio)
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"El DNI {dni} ya existe (UNIQUE).") from e

        return socio