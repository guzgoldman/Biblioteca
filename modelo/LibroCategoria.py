from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.Conector import Base

class LibroCategoria(Base):
    __tablename__ = "libro_categoria"

    id = Column(Integer, primary_key=True, autoincrement=True)
    libro_isbn = Column(String(50), ForeignKey("libros.isbn", ondelete="CASCADE"), nullable=False)
    categoria_code = Column(String(50), ForeignKey("categorias.code", ondelete="CASCADE"), nullable=False)

    # Relaciones bidireccionales
    libro = relationship("Libro", back_populates="categorias_rel")
    categoria = relationship("Categoria", back_populates="libros_rel")
