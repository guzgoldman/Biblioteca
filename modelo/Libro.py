from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Session
from sqlalchemy.exc import IntegrityError
from db.Conector import Base
from modelo.LibroCategoria import LibroCategoria
from modelo.Categoria import Categoria

class Libro(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(200), nullable=False)
    autor = Column(String(150), nullable=False)
    isbn = Column(String(20), nullable=False, unique=True)

    ejemplares = relationship(
        "Ejemplar",
        back_populates="libro",
        primaryjoin="Libro.isbn==Ejemplar.libro_isbn",
        cascade="all, delete-orphan"
    )

    # Relación directa con LibroCategoria
    categorias_rel = relationship(
        "LibroCategoria",
        back_populates="libro",
        cascade="all, delete-orphan"
    )

    # Acceso indirecto a Categorías (solo lectura)
    categorias = relationship(
        "Categoria",
        secondary="libro_categoria",
        primaryjoin="Libro.isbn==LibroCategoria.libro_isbn",
        secondaryjoin="LibroCategoria.categoria_code==Categoria.code",
        viewonly=True
    )

    def __repr__(self):
        return f"<Libro id={self.id} titulo={self.titulo!r} autor={self.autor!r}>"

    # ==========================================================
    # CREAR LIBRO + EJEMPLARES INICIALES
    # ==========================================================
    @classmethod
    def crear_con_ejemplares(
        cls,
        session: Session,
        titulo: str,
        autor: str,
        isbn: str,
        codigo_identificador: str,
        cantidad_ejemplares: int = 1,
        *,
        commit: bool = False
    ) -> "Libro":
        """
        Crea un nuevo libro y genera los ejemplares iniciales.
        """
        from modelo.Ejemplar import Ejemplar

        titulo = (titulo or "").strip()
        autor = (autor or "").strip()
        isbn = (isbn or "").strip()
        codigo_identificador = (codigo_identificador or "").strip().upper()

        if not titulo or not autor or not isbn or not codigo_identificador:
            raise ValueError("Título, autor, ISBN y código identificador son obligatorios.")

        if cantidad_ejemplares < 1:
            raise ValueError("Debe ingresar al menos un ejemplar.")

        # Validar duplicados
        if session.query(cls).filter_by(isbn=isbn).first():
            raise ValueError(f"Ya existe un libro con ISBN '{isbn}'")

        # Crear libro
        libro = cls(titulo=titulo, autor=autor, isbn=isbn)
        session.add(libro)
        session.flush()  # asegura que el libro exista en sesión

        # Crear ejemplares iniciales
        Ejemplar.crear_multiples(
            session,
            libro_isbn=isbn,
            cantidad=cantidad_ejemplares,
            commit=False
        )

        if commit:
            try:
                session.commit()
                session.refresh(libro)
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Error al crear el libro y sus ejemplares: {str(e)}") from e

        return libro

    # ==========================================================
    # EDITAR O AGREGAR EJEMPLARES
    # ==========================================================
    def editar(
        self,
        session: Session,
        nuevo_titulo: str = None,
        nuevo_autor: str = None,
        nuevos_ejemplares: int = 0,
        codigo_identificador: str = None,
        *,
        commit: bool = False
    ):
        """
        Permite editar los datos del libro o agregar nuevos ejemplares.
        Si 'nuevos_ejemplares' > 0, se agregan ejemplares adicionales.
        """
        from modelo.Ejemplar import Ejemplar

        # Edición de campos básicos
        cambios = []
        if nuevo_titulo and nuevo_titulo.strip() and nuevo_titulo.strip() != self.titulo:
            self.titulo = nuevo_titulo.strip()
            cambios.append("título")

        if nuevo_autor and nuevo_autor.strip() and nuevo_autor.strip() != self.autor:
            self.autor = nuevo_autor.strip()
            cambios.append("autor")

        # Agregar ejemplares
        nuevos = []
        if nuevos_ejemplares and nuevos_ejemplares > 0:
            if not codigo_identificador:
                raise ValueError("Debe indicar el código identificador para generar nuevos ejemplares.")
            nuevos = Ejemplar.crear_multiples(
                session,
                libro_isbn=self.isbn,
                cantidad=nuevos_ejemplares,
                commit=False
            )
            cambios.append(f"{nuevos_ejemplares} ejemplares nuevos")

        session.add(self)

        if commit:
            try:
                session.commit()
                session.refresh(self)
                for ej in nuevos:
                    session.refresh(ej)
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Error al actualizar el libro: {str(e)}") from e

        if not cambios:
            return "No se realizaron cambios en el libro."
        return f"Libro actualizado correctamente ({', '.join(cambios)})."

    # ==========================================================
    # CONSULTAS
    # ==========================================================
    @classmethod
    def buscar_por_isbn(cls, session: Session, isbn: str) -> "Libro":
        libro = session.query(cls).filter_by(isbn=isbn).one_or_none()
        if not libro:
            raise ValueError(f"No existe un libro con ISBN '{isbn}'")
        return libro

    @classmethod
    def buscar_por_titulo_autor(cls, session: Session, titulo: str, autor: str) -> "Libro":
        libro = session.query(cls).filter_by(titulo=titulo.strip(), autor=autor.strip()).one_or_none()
        if not libro:
            raise ValueError(f"No existe un libro '{titulo}' del autor '{autor}'")
        return libro
