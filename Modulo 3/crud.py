"""Operaciones CRUD y búsqueda sobre libros usando SQLAlchemy."""
from contextlib import contextmanager
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError

from database import SessionLocal
from models import Libro


class ErrorBaseDatos(Exception):
    """Error amigable para mostrar al usuario."""


@contextmanager
def sesion():
    """Abre una sesión, confirma al final y revierte ante cualquier error."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise ErrorBaseDatos(
            "Error de integridad: ya existe un libro con ese título y autor."
        ) from e
    except OperationalError as e:
        db.rollback()
        raise ErrorBaseDatos(
            "No se pudo conectar con MariaDB. Verifica que el servicio esté activo "
            "y que usuario, contraseña, host y base de datos sean correctos."
        ) from e
    except SQLAlchemyError as e:
        db.rollback()
        raise ErrorBaseDatos(f"Error en la base de datos: {e}") from e
    finally:
        db.close()


def agregar_libro(titulo, autor, genero, estado):
    with sesion() as db:
        libro = Libro(titulo=titulo, autor=autor, genero=genero, estado_lectura=estado)
        db.add(libro)
        db.flush()  # obtiene el id generado
        return libro


def listar_libros():
    with sesion() as db:
        return db.query(Libro).order_by(Libro.id).all()


def obtener_libro(libro_id):
    with sesion() as db:
        return db.get(Libro, libro_id)


def actualizar_libro(libro_id, titulo=None, autor=None, genero=None, estado=None):
    """Actualiza solo los campos recibidos. Devuelve el libro o None si no existe."""
    with sesion() as db:
        libro = db.get(Libro, libro_id)
        if libro is None:
            return None
        if titulo:
            libro.titulo = titulo
        if autor:
            libro.autor = autor
        if genero:
            libro.genero = genero
        if estado:
            libro.estado_lectura = estado
        return libro


def eliminar_libro(libro_id):
    """Devuelve True si se eliminó, False si no existía."""
    with sesion() as db:
        libro = db.get(Libro, libro_id)
        if libro is None:
            return False
        db.delete(libro)
        return True


def buscar_libros(criterio, texto):
    """criterio: 'titulo', 'autor' o 'genero'. Búsqueda parcial sin distinguir mayúsculas."""
    columnas = {"titulo": Libro.titulo, "autor": Libro.autor, "genero": Libro.genero}
    columna = columnas[criterio]
    with sesion() as db:
        return db.query(Libro).filter(columna.ilike(f"%{texto}%")).order_by(Libro.id).all()
