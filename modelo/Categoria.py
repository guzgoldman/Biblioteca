from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from modelo.LibroCategoria import libro_categoria
from db.Conector import Base

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False)
    
    libros = relationship('Libro', secondary=libro_categoria, back_populates='categorias')
    
    def __repr__(self):
        return f"<Categoria id={self.id} nombre={self.nombre}>"