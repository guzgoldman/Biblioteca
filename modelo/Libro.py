from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Session
from sqlalchemy.exc import IntegrityError
from db.Conector import Base
from modelo.LibroCategoria import libro_categoria
from modelo.Categoria import Categoria

class Libro(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(200), nullable=False)
    autor = Column(String(150), nullable=False)

    ejemplares = relationship("Ejemplar", back_populates="libro", cascade="all, delete-orphan")
    categorias = relationship("Categoria", secondary=libro_categoria, back_populates="libros")

    def __repr__(self):
        return f"<Libro id={self.id} titulo={self.titulo!r} autor={self.autor!r}>"

    @classmethod
    def crear(cls, session: Session, titulo: str, autor: str, *, commit: bool = False) -> "Libro":
        """Crea un nuevo libro. Lanza ValueError si ya existe."""
        titulo = (titulo or "").strip()
        autor = (autor or "").strip()
        
        if not titulo or not autor:
            raise ValueError("Título y autor son obligatorios")
        
        # Verificar si ya existe un libro con el mismo título y autor
        existente = session.query(cls).filter_by(titulo=titulo, autor=autor).one_or_none()
        if existente:
            raise ValueError(f"Ya existe un libro '{titulo}' del autor '{autor}'")
        
        libro = cls(titulo=titulo, autor=autor)
        session.add(libro)
        
        if commit:
            try:
                session.commit()
                session.refresh(libro)
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Error al crear el libro: {str(e)}") from e
        
        return libro
    
    @classmethod
    def registrar_libro_con_ejemplares(cls, session: Session, titulo: str, autor: str, cantidad: int = 1, *, commit: bool = False) -> "Libro":
        """Registra un libro nuevo o usa uno existente y agrega ejemplares."""
        from modelo.Ejemplar import Ejemplar
        
        titulo = (titulo or "").strip()
        autor = (autor or "").strip()
        
        if not titulo or not autor:
            raise ValueError("Título y autor son obligatorios")
        
        if cantidad < 1:
            raise ValueError("La cantidad debe ser mayor a 0")
        
        libro = session.query(cls).filter_by(titulo=titulo, autor=autor).one_or_none()
        if not libro:
            libro = cls(titulo=titulo, autor=autor)
            session.add(libro)
            session.flush()
        
        ejemplares = Ejemplar.crear_multiples(session, libro.id, cantidad, commit=False)
        
        if commit:
            try:
                session.commit()
                session.refresh(libro)
                for ejemplar in ejemplares:
                    session.refresh(ejemplar)
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Error al registrar el libro con ejemplares: {str(e)}") from e
        
        return libro
    
    def agregar_ejemplares(self, session: Session, cantidad: int, *, commit: bool = False) -> list:
        """Agrega nuevos ejemplares a este libro."""
        from modelo.Ejemplar import Ejemplar  # Import aquí para evitar imports circulares
        
        if cantidad < 1:
            raise ValueError("La cantidad debe ser mayor a 0")
        
        ejemplares = Ejemplar.crear_multiples(session, self.id, cantidad, commit=False)
        
        if commit:
            try:
                session.commit()
                for ejemplar in ejemplares:
                    session.refresh(ejemplar)
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Error al agregar ejemplares: {str(e)}") from e
        
        return ejemplares
    
    def obtener_ejemplares_disponibles(self, session: Session) -> list:
        """Retorna los ejemplares disponibles de este libro."""
        from modelo.Ejemplar import Ejemplar  # Import aquí para evitar imports circulares
        return Ejemplar.listar_disponibles_por_libro(session, self.id)
    
    def obtener_todos_ejemplares(self, session: Session) -> list:
        """Retorna todos los ejemplares de este libro ordenados por número."""
        from modelo.Ejemplar import Ejemplar  # Import aquí para evitar imports circulares
        return Ejemplar.listar_por_libro(session, self.id)
    
    @classmethod
    def buscar_por_id(cls, session: Session, libro_id: int) -> "Libro":
        """Busca un libro por ID."""
        libro = session.query(cls).filter_by(id=libro_id).one_or_none()
        if not libro:
            raise ValueError(f"No existe un libro con ID {libro_id}")
        return libro
    
    @classmethod
    def buscar_por_titulo_autor(cls, session: Session, titulo: str, autor: str) -> "Libro":
        """Busca un libro por título y autor."""
        titulo = (titulo or "").strip()
        autor = (autor or "").strip()
        
        if not titulo or not autor:
            raise ValueError("Título y autor son obligatorios")
        
        libro = session.query(cls).filter_by(titulo=titulo, autor=autor).one_or_none()
        if not libro:
            raise ValueError(f"No existe un libro '{titulo}' del autor '{autor}'")
        return libro