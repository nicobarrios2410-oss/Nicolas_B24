"""
crear_bd.py
Crea la base de datos 'aventureros.db' a partir de schema.sql,
inserta datos de ejemplo y muestra algunas consultas para comprobar
que las relaciones funcionan.
"""

import os
import sqlite3

CARPETA = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(CARPETA, "aventureros.db")
SCHEMA_PATH = os.path.join(CARPETA, "schema.sql")


def crear_base_de_datos():
    """Borra la BD anterior (si existe) y crea las tablas desde schema.sql."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        conn.executescript(f.read())
    return conn


def insertar_datos(conn):
    """Inserta datos de ejemplo en todas las tablas."""
    heroes = [
        ("Aragorn", "Guerrero", 12),
        ("Gandalf", "Mago", 20),
        ("Legolas", "Arquero", 15),
        ("Gimli", "Guerrero", 11),
        ("Elara", "Clériga", 8),
    ]
    misiones = [
        ("Rescatar al aldeano", 2, "Bosque Sombrío", 150),
        ("Defender la torre", 3, "Torre del Norte", 400),
        ("Cazar al dragón", 5, "Montañas de Fuego", 2000),
        ("Limpiar la cripta", 4, "Cripta Olvidada", 900),
    ]
    monstruos = [
        ("Grix", "Goblin", 2),
        ("Ignis", "Dragón", 10),
        ("Lord Mortis", "No-muerto", 7),
        ("Uruk", "Orco", 4),
        ("Sombra", "No-muerto", 5),
    ]

    conn.executemany(
        "INSERT INTO heroes (nombre, clase, nivel_experiencia) VALUES (?, ?, ?)", heroes
    )
    conn.executemany(
        "INSERT INTO misiones (nombre, dificultad, localizacion, recompensa) VALUES (?, ?, ?, ?)",
        misiones,
    )
    conn.executemany(
        "INSERT INTO monstruos (nombre, tipo, nivel_amenaza) VALUES (?, ?, ?)", monstruos
    )

    # (mision_id, heroe_id)
    participaciones = [
        (1, 1), (1, 5),
        (2, 1), (2, 3), (2, 4),
        (3, 1), (3, 2), (3, 3), (3, 4),
        (4, 2), (4, 5),
    ]
    conn.executemany(
        "INSERT INTO misiones_heroes (mision_id, heroe_id) VALUES (?, ?)", participaciones
    )

    # (mision_id, monstruo_id)
    enfrentamientos = [
        (1, 1),
        (2, 4), (2, 1),
        (3, 2),
        (4, 3), (4, 5),
    ]
    conn.executemany(
        "INSERT INTO misiones_monstruos (mision_id, monstruo_id) VALUES (?, ?)", enfrentamientos
    )

    conn.commit()


def mostrar(titulo, filas, encabezados):
    """Imprime el resultado de una consulta de forma sencilla."""
    print(f"\n=== {titulo} ===")
    print(" | ".join(encabezados))
    print("-" * 60)
    for fila in filas:
        print(" | ".join(str(x) for x in fila))


def consultas_de_ejemplo(conn):
    """Consultas que usan JOIN sobre las tablas puente."""
    filas = conn.execute(
        """
        SELECT m.nombre, GROUP_CONCAT(h.nombre, ', ')
        FROM misiones m
        JOIN misiones_heroes mh ON mh.mision_id = m.id
        JOIN heroes h ON h.id = mh.heroe_id
        GROUP BY m.id
        """
    ).fetchall()
    mostrar("Héroes que participaron en cada misión", filas, ["Misión", "Héroes"])

    filas = conn.execute(
        """
        SELECT m.nombre, GROUP_CONCAT(mo.nombre || ' (' || mo.tipo || ')', ', ')
        FROM misiones m
        JOIN misiones_monstruos mm ON mm.mision_id = m.id
        JOIN monstruos mo ON mo.id = mm.monstruo_id
        GROUP BY m.id
        """
    ).fetchall()
    mostrar("Monstruos enfrentados en cada misión", filas, ["Misión", "Monstruos"])

    filas = conn.execute(
        """
        SELECT h.nombre, h.clase, COUNT(mh.mision_id), SUM(m.recompensa)
        FROM heroes h
        JOIN misiones_heroes mh ON mh.heroe_id = h.id
        JOIN misiones m ON m.id = mh.mision_id
        GROUP BY h.id
        ORDER BY SUM(m.recompensa) DESC
        """
    ).fetchall()
    mostrar(
        "Misiones y oro por héroe",
        filas,
        ["Héroe", "Clase", "Nº misiones", "Oro total"],
    )


def probar_restricciones(conn):
    """Comprueba que los CHECK y las FOREIGN KEY realmente rechazan datos inválidos."""
    print("\n=== Prueba de restricciones ===")

    try:
        conn.execute(
            "INSERT INTO misiones (nombre, dificultad, localizacion, recompensa) "
            "VALUES ('Misión inválida', 9, 'Ninguna', 100)"
        )
    except sqlite3.IntegrityError as e:
        print(f" Dificultad fuera de rango rechazada: {e}")

    try:
        conn.execute("INSERT INTO misiones_heroes (mision_id, heroe_id) VALUES (99, 1)")
    except sqlite3.IntegrityError as e:
        print(f" Clave foránea inexistente rechazada: {e}")

    try:
        conn.execute("INSERT INTO misiones_heroes (mision_id, heroe_id) VALUES (1, 1)")
    except sqlite3.IntegrityError as e:
        print(f" Participación duplicada rechazada: {e}")


def main():
    conn = crear_base_de_datos()
    insertar_datos(conn)
    consultas_de_ejemplo(conn)
    probar_restricciones(conn)
    conn.close()
    print(f"\nBase de datos creada en: {DB_PATH}")


if __name__ == "__main__":
    main()
