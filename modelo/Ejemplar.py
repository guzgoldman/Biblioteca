# modelo/Ejemplar.py
from typing import List, Optional
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, Session
from sqlalchemy.exc import IntegrityError
from db.Conector import Base


class Ejemplar(Base):
    __tablename__ = "ejemplares"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(50), unique=True, nullable=False, index=True)
    numero_ejemplar = Column(Integer, nullable=False, index=True)
    disponible = Column(Boolean, nullable=False, default=True)
    libro_isbn = Column(
        String(50),
        ForeignKey("libros.isbn", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    alta_ejemplar = Column(DateTime(timezone=True), nullable=False)
    baja_ejemplar = Column(DateTime(timezone=True), nullable=True)

    # Si en Libro la PK no es isbn, asegurate de definir el back_populates con primaryjoin en ese modelo
    libro = relationship(
        "Libro",
        back_populates="ejemplares",
        primaryjoin="Ejemplar.libro_isbn==Libro.isbn",
        foreign_keys=[libro_isbn],
    )
    prestamos = relationship("Prestamo", back_populates="ejemplar")

    def __repr__(self) -> str:
        return f"<Ejemplar id={self.id} codigo={self.codigo} numero={self.numero_ejemplar} disponible={self.disponible}>"

    # ---------------------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------------------
    @staticmethod
    def _obtener_codigo_base(libro) -> str:
        """
        Intenta obtener el 'código identificador' del libro.
        Ajustá el nombre del atributo si en tu modelo se llama distinto.
        Admito varios alias comunes para evitar errores.
        """
        for attr in ("codigo_identificador", "codigo_base", "identificador", "slug_codigo"):
            val = getattr(libro, attr, None)
            if val:
                return val
        raise ValueError(
            "El libro no tiene definido su código identificador "
            "(esperado: Libro.codigo_identificador o codigo_base)."
        )

    @classmethod
    def _siguiente_numero_para_isbn(cls, session: Session, libro_isbn: str) -> int:
        """Devuelve MAX(numero_ejemplar)+1 para ese ISBN (sin crear huecos si hubo bajas)."""
        max_num = session.query(func.max(cls.numero_ejemplar)).filter_by(libro_isbn=libro_isbn).scalar()
        return (max_num or 0) + 1

    # ---------------------------------------------------------------------
    # Creación
    # ---------------------------------------------------------------------
    @classmethod
    def crear(
        cls,
        session: Session,
        libro_isbn: str,
        *,
        codigo: Optional[str] = None,
        commit: bool = False,
    ) -> "Ejemplar":
        """
        Crea un ejemplar para el libro indicado por ISBN.
        Si no se pasa 'codigo', se genera como '<codigo_identificador>-<n>'.
        """
        from modelo.Libro import Libro  # evitar import circular

        libro = session.query(Libro).filter_by(isbn=libro_isbn).one_or_none()
        if not libro:
            raise ValueError(f"No existe un libro con ISBN '{libro_isbn}'")

        sig_num = cls._siguiente_numero_para_isbn(session, libro_isbn)

        if not codigo:
            codigo_base = cls._obtener_codigo_base(libro)
            codigo = f"{codigo_base}-{sig_num}"

        # Unicidad del código
        if session.query(cls.id).filter_by(codigo=codigo).first():
            raise ValueError(f"Ya existe un ejemplar con código '{codigo}'")

        ej = cls(
            libro_isbn=libro_isbn,
            numero_ejemplar=sig_num,
            codigo=codigo,
            disponible=True,
        )
        session.add(ej)

        if commit:
            try:
                session.commit()
                session.refresh(ej)
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Error al crear el ejemplar: {str(e)}") from e

        return ej

    @classmethod
    def crear_multiples(
        cls,
        session: Session,
        libro_isbn: str,
        cantidad: int,
        *,
        commit: bool = False,
    ) -> List["Ejemplar"]:
        """
        Crea 'cantidad' ejemplares para el libro (ISBN).
        Genera códigos con el código identificador del libro + correlativo.
        """
        if cantidad < 1:
            raise ValueError("La cantidad debe ser mayor a 0")

        from modelo.Libro import Libro

        libro = session.query(Libro).filter_by(isbn=libro_isbn).one_or_none()
        if not libro:
            raise ValueError(f"No existe un libro con ISBN '{libro_isbn}'")

        codigo_base = cls._obtener_codigo_base(libro)
        sig_num = cls._siguiente_numero_para_isbn(session, libro_isbn)

        creados: List[Ejemplar] = []
        try:
            for offset in range(cantidad):
                num = sig_num + offset
                codigo = f"{codigo_base}-{num}"

                if session.query(cls.id).filter_by(codigo=codigo).first():
                    raise ValueError(f"El código generado ya existe: '{codigo}'")

                ej = cls(
                    libro_isbn=libro_isbn,
                    numero_ejemplar=num,
                    codigo=codigo,
                    disponible=True,
                )
                session.add(ej)
                creados.append(ej)

            if commit:
                session.commit()
                for ej in creados:
                    session.refresh(ej)
        except Exception:
            session.rollback()
            raise

        return creados

    # ---------------------------------------------------------------------
    # Consultas
    # ---------------------------------------------------------------------
    @classmethod
    def buscar_por_codigo(cls, session: Session, codigo: str) -> "Ejemplar":
        if not codigo:
            raise ValueError("El código es obligatorio")
        ej = session.query(cls).filter_by(codigo=codigo).one_or_none()
        if not ej:
            raise ValueError(f"No existe un ejemplar con código '{codigo}'")
        return ej

    @classmethod
    def listar_por_libro(cls, session: Session, libro_isbn: str) -> List["Ejemplar"]:
        return (
            session.query(cls)
            .filter_by(libro_isbn=libro_isbn)
            .order_by(cls.numero_ejemplar.asc())
            .all()
        )

    @classmethod
    def listar_disponibles_por_libro(cls, session: Session, libro_isbn: str) -> List["Ejemplar"]:
        return (
            session.query(cls)
            .filter_by(libro_isbn=libro_isbn, disponible=True)
            .order_by(cls.numero_ejemplar.asc())
            .all()
        )

    # ---------------------------------------------------------------------
    # Estados
    # ---------------------------------------------------------------------
    def marcar_como_prestado(self, session: Session):
        if not self.disponible:
            raise ValueError("El ejemplar ya está prestado")
        self.disponible = False
        session.add(self)

    def marcar_como_disponible(self, session: Session):
        self.disponible = True
        session.add(self)