from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Session
from sqlalchemy.exc import IntegrityError
from db.Conector import Base

class Ejemplar(Base):
    __tablename__ = "ejemplares"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(50), unique=True, nullable=False, index=True)
    numero_ejemplar = Column(Integer, nullable=False, index=True)  # Número autoincremental por libro
    disponible = Column(Boolean, nullable=False, default=True)
    libro_id = Column(Integer, ForeignKey("libros.id", ondelete="RESTRICT"), nullable=False, index=True)
    
    libro = relationship("Libro", back_populates="ejemplares")
    prestamos = relationship("Prestamo", back_populates="ejemplar")

    def __repr__(self):
        return f"<Ejemplar id={self.id} codigo={self.codigo} numero={self.numero_ejemplar} disponible={self.disponible}>"

    @classmethod
    def crear(cls, session: Session, libro_id: int, codigo: str = None, *, commit: bool = False) -> "Ejemplar":
        """Crea un nuevo ejemplar para un libro con numeración autoincremental."""
        from modelo.Libro import Libro  # Import aquí para evitar imports circulares
        
        # Verificar que el libro existe
        libro = session.query(Libro).filter_by(id=libro_id).one_or_none()
        if not libro:
            raise ValueError(f"No existe un libro con ID {libro_id}")
        
        # Obtener el siguiente número de ejemplar para este libro
        max_numero = session.query(cls).filter_by(libro_id=libro_id).count()
        siguiente_numero = max_numero + 1
        
        # Generar código si no se proporciona
        if not codigo:
            codigo = f"LIB-{libro_id}-{siguiente_numero:03d}"  # Formato: LIB-1-001, LIB-1-002, etc.
        
        # Verificar que el código sea único
        existente = session.query(cls).filter_by(codigo=codigo).one_or_none()
        if existente:
            raise ValueError(f"Ya existe un ejemplar con código '{codigo}'")
        
        ejemplar = cls(
            libro_id=libro_id,
            numero_ejemplar=siguiente_numero,
            codigo=codigo,
            disponible=True
        )
        session.add(ejemplar)
        
        if commit:
            try:
                session.commit()
                session.refresh(ejemplar)
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Error al crear el ejemplar: {str(e)}") from e
        
        return ejemplar
    
    @classmethod
    def crear_multiples(cls, session: Session, libro_id: int, cantidad: int, *, commit: bool = False) -> list["Ejemplar"]:
        """Crea múltiples ejemplares para un libro con numeración autoincremental."""
        from modelo.Libro import Libro  # Import aquí para evitar imports circulares
        
        if cantidad < 1:
            raise ValueError("La cantidad debe ser mayor a 0")
        
        # Verificar que el libro existe
        libro = session.query(Libro).filter_by(id=libro_id).one_or_none()
        if not libro:
            raise ValueError(f"No existe un libro con ID {libro_id}")
        
        # Obtener el siguiente número de ejemplar para este libro
        max_numero = session.query(cls).filter_by(libro_id=libro_id).count()
        
        ejemplares = []
        for i in range(cantidad):
            siguiente_numero = max_numero + i + 1
            codigo = f"LIB-{libro_id}-{siguiente_numero:03d}"
            
            ejemplar = cls(
                libro_id=libro_id,
                numero_ejemplar=siguiente_numero,
                codigo=codigo,
                disponible=True
            )
            session.add(ejemplar)
            ejemplares.append(ejemplar)
        
        if commit:
            try:
                session.commit()
                for ejemplar in ejemplares:
                    session.refresh(ejemplar)
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Error al crear los ejemplares: {str(e)}") from e
        
        return ejemplares
    
    @classmethod
    def buscar_por_codigo(cls, session: Session, codigo: str) -> "Ejemplar":
        """Busca un ejemplar por su código."""
        if not codigo:
            raise ValueError("El código es obligatorio")
        
        ejemplar = session.query(cls).filter_by(codigo=codigo).one_or_none()
        if not ejemplar:
            raise ValueError(f"No existe un ejemplar con código '{codigo}'")
        return ejemplar
    
    @classmethod
    def listar_por_libro(cls, session: Session, libro_id: int) -> list["Ejemplar"]:
        """Lista todos los ejemplares de un libro ordenados por número de ejemplar."""
        return session.query(cls).filter_by(libro_id=libro_id).order_by(cls.numero_ejemplar).all()
    
    @classmethod
    def listar_disponibles_por_libro(cls, session: Session, libro_id: int) -> list["Ejemplar"]:
        """Lista los ejemplares disponibles de un libro ordenados por número de ejemplar."""
        return session.query(cls).filter_by(libro_id=libro_id, disponible=True).order_by(cls.numero_ejemplar).all()

    def marcar_como_prestado(self, session: Session):
        """Marca este ejemplar como no disponible"""
        if not self.disponible:
            raise ValueError("El ejemplar ya está prestado")
        self.disponible = False
        session.add(self)

    def marcar_como_disponible(self, session: Session):
        """Marca este ejemplar como disponible"""
        self.disponible = True
        session.add(self)