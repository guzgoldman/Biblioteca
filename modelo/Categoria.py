from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Session
from sqlalchemy.exc import IntegrityError
from modelo.LibroCategoria import libro_categoria
from db.Conector import Base

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False)
    
    libros = relationship('Libro', secondary=libro_categoria, back_populates='categorias')
    
    def __repr__(self):
        return f"<Categoria id={self.id} nombre={self.nombre}>"
    
    @classmethod
    def crear(cls, session: Session, nombre: str, *, commit: bool = False) -> "Categoria":
        """Crea una nueva categoría. Lanza ValueError si el nombre ya existe."""
        nombre = (nombre or "").strip()
        
        if not nombre:
            raise ValueError("El nombre de la categoría es obligatorio")
        
        existente = session.query(cls).filter_by(nombre=nombre).one_or_none()
        if existente:
            raise ValueError(f"Ya existe una categoría con el nombre '{nombre}'")
        
        categoria = cls(nombre=nombre)
        session.add(categoria)
        
        if commit:
            try:
                session.commit()
                session.refresh(categoria)
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"El nombre '{nombre}' ya existe (UNIQUE).") from e
        
        return categoria
    
    @classmethod
    def buscar_por_id(cls, session: Session, categoria_id: int) -> "Categoria":
        """Busca una categoría por ID. Lanza ValueError si no existe."""
        categoria = session.query(cls).filter_by(id=categoria_id).one_or_none()
        if not categoria:
            raise ValueError(f"No existe una categoría con ID {categoria_id}")
        return categoria
    
    @classmethod
    def buscar_por_nombre(cls, session: Session, nombre: str) -> "Categoria":
        """Busca una categoría por nombre. Lanza ValueError si no existe."""
        nombre = (nombre or "").strip()
        if not nombre:
            raise ValueError("El nombre es obligatorio para la búsqueda")
        
        categoria = session.query(cls).filter_by(nombre=nombre).one_or_none()
        if not categoria:
            raise ValueError(f"No existe una categoría con el nombre '{nombre}'")
        return categoria
    
    @classmethod
    def listar_todas(cls, session: Session) -> list["Categoria"]:
        """Retorna todas las categorías ordenadas por nombre."""
        return session.query(cls).order_by(cls.nombre).all()
    
    def actualizar(self, session: Session, nombre: str = None, *, commit: bool = False) -> "Categoria":
        """Actualiza los datos de la categoría."""
        if nombre is not None:
            nombre = nombre.strip()
            if not nombre:
                raise ValueError("El nombre no puede estar vacío")
            
            # Verificar que no exista otra categoría con el mismo nombre
            existente = session.query(self.__class__).filter(
                self.__class__.nombre == nombre,
                self.__class__.id != self.id
            ).one_or_none()
            
            if existente:
                raise ValueError(f"Ya existe otra categoría con el nombre '{nombre}'")
            
            self.nombre = nombre
        
        if commit:
            try:
                session.commit()
                session.refresh(self)
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Error al actualizar: {str(e)}") from e
        
        return self
    
    def eliminar(self, session: Session, *, commit: bool = False) -> bool:
        """Elimina la categoría. Retorna True si se eliminó correctamente."""
        # Verificar si tiene libros asociados
        if self.libros:
            raise ValueError(f"No se puede eliminar la categoría '{self.nombre}' porque tiene libros asociados")
        
        session.delete(self)
        
        if commit:
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Error al eliminar la categoría: {str(e)}") from e
        
        return True