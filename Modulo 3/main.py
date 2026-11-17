"""Aplicación de consola para gestionar una biblioteca personal (MariaDB + SQLAlchemy)."""
import sys

from database import Base, engine
from models import ESTADOS_LECTURA
import crud
from crud import ErrorBaseDatos


def pedir_texto(mensaje, obligatorio=True):
    while True:
        valor = input(mensaje).strip()
        if valor or not obligatorio:
            return valor
        print("  ⚠ Este campo no puede estar vacío.")


def pedir_estado(obligatorio=True):
    opciones = ", ".join(f"{i}) {e}" for i, e in enumerate(ESTADOS_LECTURA, 1))
    while True:
        valor = input(f"Estado de lectura ({opciones}): ").strip()
        if not valor and not obligatorio:
            return ""
        if valor.isdigit() and 1 <= int(valor) <= len(ESTADOS_LECTURA):
            return ESTADOS_LECTURA[int(valor) - 1]
        print("  ⚠ Opción no válida.")


def pedir_id(mensaje="ID del libro: "):
    while True:
        valor = input(mensaje).strip()
        if valor.isdigit():
            return int(valor)
        print("  ⚠ Ingresa un número entero válido.")


def mostrar_libros(libros):
    if not libros:
        print("\nNo se encontraron libros.")
        return
    print(f"\n{'ID':<5}{'Título':<35}{'Autor':<25}{'Género':<18}{'Estado':<10}")
    print("-" * 93)
    for l in libros:
        print(f"{l.id:<5}{l.titulo[:33]:<35}{l.autor[:23]:<25}{l.genero[:16]:<18}{l.estado_lectura:<10}")


def opcion_agregar():
    print("\n--- Agregar nuevo libro ---")
    titulo = pedir_texto("Título: ")
    autor = pedir_texto("Autor: ")
    genero = pedir_texto("Género: ")
    estado = pedir_estado()
    libro = crud.agregar_libro(titulo, autor, genero, estado)
    print(f"✔ Libro agregado con ID {libro.id}.")


def opcion_actualizar():
    print("\n--- Actualizar libro ---")
    libro_id = pedir_id()
    libro = crud.obtener_libro(libro_id)
    if libro is None:
        print("✖ No existe un libro con ese ID.")
        return
    print(f"Libro actual: {libro.titulo} | {libro.autor} | {libro.genero} | {libro.estado_lectura}")
    print("(Deja vacío lo que no quieras cambiar)")
    titulo = pedir_texto("Nuevo título: ", obligatorio=False)
    autor = pedir_texto("Nuevo autor: ", obligatorio=False)
    genero = pedir_texto("Nuevo género: ", obligatorio=False)
    estado = pedir_estado(obligatorio=False)
    crud.actualizar_libro(libro_id, titulo, autor, genero, estado)
    print("✔ Libro actualizado.")


def opcion_eliminar():
    print("\n--- Eliminar libro ---")
    libro_id = pedir_id()
    libro = crud.obtener_libro(libro_id)
    if libro is None:
        print("✖ No existe un libro con ese ID.")
        return
    confirmar = input(f"¿Eliminar '{libro.titulo}'? (s/n): ").strip().lower()
    if confirmar == "s":
        crud.eliminar_libro(libro_id)
        print("✔ Libro eliminado.")
    else:
        print("Operación cancelada.")


def opcion_listar():
    print("\n--- Listado de libros ---")
    mostrar_libros(crud.listar_libros())


def opcion_buscar():
    print("\n--- Buscar libros ---")
    print("1) Por título\n2) Por autor\n3) Por género")
    criterios = {"1": "titulo", "2": "autor", "3": "genero"}
    eleccion = input("Buscar por: ").strip()
    if eleccion not in criterios:
        print("✖ Opción no válida.")
        return
    texto = pedir_texto("Texto a buscar: ")
    mostrar_libros(crud.buscar_libros(criterios[eleccion], texto))


MENU = """
===== BIBLIOTECA PERSONAL (MariaDB) =====
1. Agregar nuevo libro
2. Actualizar información de un libro
3. Eliminar libro existente
4. Ver listado de libros
5. Buscar libros
6. Salir
"""

ACCIONES = {
    "1": opcion_agregar,
    "2": opcion_actualizar,
    "3": opcion_eliminar,
    "4": opcion_listar,
    "5": opcion_buscar,
}


def main():
    # Crea las tablas si no existen y comprueba la conexión
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        print("✖ No se pudo conectar con MariaDB. Revisa la configuración en database.py")
        print(f"  Detalle: {e.__class__.__name__}")
        sys.exit(1)

    while True:
        print(MENU)
        opcion = input("Elige una opción: ").strip()
        if opcion == "6":
            print("¡Hasta pronto!")
            break
        accion = ACCIONES.get(opcion)
        if accion is None:
            print("✖ Opción no válida.")
            continue
        try:
            accion()
        except ErrorBaseDatos as e:
            print(f"✖ {e}")
        except (KeyboardInterrupt, EOFError):
            print("\nOperación cancelada.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma finalizado.")
