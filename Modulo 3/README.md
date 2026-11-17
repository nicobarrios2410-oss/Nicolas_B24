# Biblioteca Personal — MariaDB + SQLAlchemy

Aplicación de consola en Python para gestionar una biblioteca personal. Esta versión reemplaza SQLite por **MariaDB** y usa **SQLAlchemy (ORM)** para definir y manipular los datos.

## Funcionalidades

1. Agregar nuevo libro (título, autor, género y estado de lectura)
2. Actualizar información de un libro
3. Eliminar un libro
4. Ver listado de libros
5. Buscar libros por título, autor o género
6. Salir

El manejo de excepciones cubre conexión fallida, errores de integridad (libro duplicado) y otros errores de SQLAlchemy.

## Estructura del proyecto

```
biblioteca/
├── main.py            # Menú interactivo
├── crud.py            # Operaciones con la BD y manejo de excepciones
├── models.py          # Modelo ORM (Libro)
├── database.py        # Configuración del engine y la cadena de conexión
├── schema.sql         # Script SQL opcional (BD, usuario y tabla)
├── requirements.txt   # Dependencias
└── README.md
```

## 1. Instalar MariaDB

**Windows**
1. Descarga el instalador desde https://mariadb.org/download/ y ejecútalo.
2. Define una contraseña para `root` y deja marcado "Install as service".
3. Abre "MariaDB Client (HeidiSQL)" o la consola `mariadb` desde el menú Inicio.

**Ubuntu / Debian**
```bash
sudo apt update
sudo apt install mariadb-server -y
sudo systemctl enable --now mariadb
sudo mariadb-secure-installation
```

Verifica la instalación:
```bash
mariadb --version
```

## 2. Crear la base de datos, el usuario y la(s) tabla(s)

Entra a la consola de MariaDB:
```bash
mariadb -u root -p
```

Ejecuta:
```sql
CREATE DATABASE biblioteca CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'biblioteca_user'@'localhost' IDENTIFIED BY 'biblioteca_pass';
GRANT ALL PRIVILEGES ON biblioteca.* TO 'biblioteca_user'@'localhost';
FLUSH PRIVILEGES;
```

La tabla `libros` se crea **automáticamente** al ejecutar la aplicación (`Base.metadata.create_all`). Si prefieres crearla a mano, usa el script incluido:
```bash
mariadb -u root -p < schema.sql
```

Estructura de la tabla `libros`:

| Campo | Tipo | Notas |
|---|---|---|
| id | INT | PK, autoincremental |
| titulo | VARCHAR(200) | obligatorio |
| autor | VARCHAR(150) | obligatorio |
| genero | VARCHAR(100) | obligatorio |
| estado_lectura | VARCHAR(20) | Pendiente / Leyendo / Leído |

Restricción única: (`titulo`, `autor`).

## 3. Instalar dependencias de Python

Se recomienda un entorno virtual:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

## 4. Configurar la cadena de conexión

La cadena de conexión está en `database.py` y tiene este formato:

```
mariadb+pymysql://USUARIO:CONTRASEÑA@HOST:PUERTO/NOMBRE_BD
```

Ejemplo con los valores por defecto:
```
mariadb+pymysql://biblioteca_user:biblioteca_pass@localhost:3306/biblioteca
```

Puedes cambiarla editando `database.py` o, sin tocar el código, con variables de entorno:

```bash
# Linux / macOS
export DB_USER=biblioteca_user
export DB_PASSWORD=biblioteca_pass
export DB_HOST=localhost
export DB_PORT=3306
export DB_NAME=biblioteca

# Windows (PowerShell)
$env:DB_USER="biblioteca_user"
$env:DB_PASSWORD="biblioteca_pass"
```

También se acepta una cadena completa en `DATABASE_URL`.

## 5. Ejecutar la aplicación

```bash
python main.py
```

## Solución de problemas

- **"No se pudo conectar con MariaDB"**: comprueba que el servicio esté activo (`sudo systemctl status mariadb` en Linux) y que usuario, contraseña, host y base de datos coincidan con la configuración.
- **Access denied for user**: revisa el `CREATE USER` / `GRANT` del paso 2.
- **Error de integridad**: intentaste registrar un libro con el mismo título y autor que otro existente.
