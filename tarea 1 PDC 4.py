"""
main.py
Gestor de libros: menú interactivo de consola.
Usa las funciones definidas en database.py
"""

import database as db


# ---------- Funciones auxiliares ----------

def pedir_texto(mensaje):
    """Pide un texto al usuario y no permite que quede vacío."""
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("⚠ Este campo no puede estar vacío.")


def pedir_estado(mensaje="¿Ya lo leíste? (s/n): "):
    """Pide el estado de lectura. Devuelve True (leído) o False (no leído)."""
    while True:
        respuesta = input(mensaje).strip().lower()
        if respuesta in ("s", "si", "sí"):
            return True
        if respuesta in ("n", "no"):
            return False
        print("⚠ Responde con 's' o 'n'.")


def pedir_id(mensaje="ID del libro: "):
    """Pide un ID numérico. Devuelve None si no es válido."""
    try:
        return int(input(mensaje).strip())
    except ValueError:
        print("⚠ El ID debe ser un número.")
        return None


def texto_estado(leido):
    """Convierte 0/1 en texto legible."""
    return "Leído" if leido else "No leído"


def mostrar_libros(libros):
    """Muestra una lista de libros en formato de tabla."""
    if not libros:
        print("\nNo se encontraron libros.")
        return

    print(f"\n{'ID':<5}{'Título':<30}{'Autor':<25}{'Género':<18}{'Estado':<10}")
    print("-" * 88)
    for id_libro, titulo, autor, genero, leido in libros:
        print(f"{id_libro:<5}{titulo[:28]:<30}{autor[:23]:<25}{genero[:16]:<18}{texto_estado(leido):<10}")


# ---------- Opciones del menú ----------

def opcion_agregar():
    print("\n--- Agregar nuevo libro ---")
    titulo = pedir_texto("Título: ")
    autor = pedir_texto("Autor: ")
    genero = pedir_texto("Género: ")
    leido = pedir_estado()
    id_nuevo = db.agregar_libro(titulo, autor, genero, leido)
    print(f"✔ Libro agregado con ID {id_nuevo}.")


def opcion_actualizar():
    print("\n--- Actualizar libro ---")
    id_libro = pedir_id()
    if id_libro is None:
        return

    libro = db.obtener_libro(id_libro)
    if libro is None:
        print("⚠ No existe un libro con ese ID.")
        return

    _, titulo, autor, genero, leido = libro
    print("Deja el campo vacío y presiona Enter para mantener el valor actual.")

    nuevo_titulo = input(f"Título [{titulo}]: ").strip() or titulo
    nuevo_autor = input(f"Autor [{autor}]: ").strip() or autor
    nuevo_genero = input(f"Género [{genero}]: ").strip() or genero

    cambiar = input(f"Estado actual: {texto_estado(leido)}. ¿Cambiarlo? (s/n): ").strip().lower()
    nuevo_leido = (not leido) if cambiar in ("s", "si", "sí") else bool(leido)

    db.actualizar_libro(id_libro, nuevo_titulo, nuevo_autor, nuevo_genero, nuevo_leido)
    print("✔ Libro actualizado correctamente.")


def opcion_eliminar():
    print("\n--- Eliminar libro ---")
    id_libro = pedir_id()
    if id_libro is None:
        return

    libro = db.obtener_libro(id_libro)
    if libro is None:
        print("⚠ No existe un libro con ese ID.")
        return

    if pedir_estado(f"¿Seguro que quieres eliminar '{libro[1]}'? (s/n): "):
        db.eliminar_libro(id_libro)
        print("✔ Libro eliminado.")
    else:
        print("Operación cancelada.")


def opcion_listar():
    print("\n--- Listado de libros ---")
    mostrar_libros(db.listar_libros())


def opcion_buscar():
    print("\n--- Buscar libros ---")
    print("1. Por título")
    print("2. Por autor")
    print("3. Por género")
    opcion = input("Elige una opción: ").strip()

    campos = {"1": "titulo", "2": "autor", "3": "genero"}
    if opcion not in campos:
        print("⚠ Opción no válida.")
        return

    valor = pedir_texto("Texto a buscar: ")
    mostrar_libros(db.buscar_libros(campos[opcion], valor))


# ---------- Menú principal ----------

def mostrar_menu():
    print("\n========== GESTOR DE LIBROS ==========")
    print("1. Agregar nuevo libro")
    print("2. Actualizar información de un libro")
    print("3. Eliminar libro existente")
    print("4. Ver listado de libros")
    print("5. Buscar libros")
    print("6. Salir")


def main():
    db.crear_tabla()

    acciones = {
        "1": opcion_agregar,
        "2": opcion_actualizar,
        "3": opcion_eliminar,
        "4": opcion_listar,
        "5": opcion_buscar,
    }

    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ").strip()

        if opcion == "6":
            print("¡Hasta pronto! 👋")
            break
        elif opcion in acciones:
            acciones[opcion]()
        else:
            print("⚠ Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    main()
