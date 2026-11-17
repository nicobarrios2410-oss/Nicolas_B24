"""Modelos ORM de la aplicación."""
from sqlalchemy import Column, Integer, String, UniqueConstraint
from database import Base

ESTADOS_LECTURA = ("Pendiente", "Leyendo", "Leído")


class Libro(Base):
    __tablename__ = "libros"
    # No se permiten dos libros con el mismo título y autor
    __table_args__ = (UniqueConstraint("titulo", "autor", name="uq_titulo_autor"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(200), nullable=False, index=True)
    autor = Column(String(150), nullable=False, index=True)
    genero = Column(String(100), nullable=False, index=True)
    estado_lectura = Column(String(20), nullable=False, default="Pendiente")

    def __repr__(self):
        return (f"<Libro id={self.id} titulo={self.titulo!r} autor={self.autor!r} "
                f"genero={self.genero!r} estado={self.estado_lectura!r}>")
