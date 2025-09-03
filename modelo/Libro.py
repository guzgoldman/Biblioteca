from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Session
from modelo.Ejemplar import Ejemplar
from db.Conector import Base
from modelo.LibroCategoria import libro_categoria

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
    def registrar_libro(cls, session: Session, titulo: str, autor: str, cantidad: int=1, codigos=None):
        if cantidad < 1 and not codigos:
            raise ValueError("Debes indicar 'cantidad' > 0 o una lista de 'codigos'.")

        libro = session.query(cls).filter_by(titulo=titulo, autor=autor).one_or_none()
        if not libro:
            libro = cls(titulo=titulo, autor=autor)
            session.add(libro)
            session.flush()

        if codigos:
            for c in codigos:
                session.add(Ejemplar(codigo=c, libro_id=libro.id))
        else:
            existentes = len(libro.ejemplares)
            start = existentes + 1
            for i in range(start, start + cantidad):
                codigo_gen = f"LIB-{libro.id}-{i}"
                session.add(Ejemplar(codigo=codigo_gen, libro_id=libro.id))

        return libro