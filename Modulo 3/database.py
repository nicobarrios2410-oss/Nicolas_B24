"""Configuración de la conexión a MariaDB con SQLAlchemy."""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Cadena de conexión. Se puede sobrescribir con la variable de entorno DATABASE_URL.
# Formato: mariadb+pymysql://usuario:contraseña@host:puerto/nombre_bd
DB_USER = os.getenv("DB_USER", "biblioteca_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "biblioteca_pass")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "biblioteca")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"mariadb+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
)

# pool_pre_ping comprueba que la conexión siga viva antes de usarla
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
Base = declarative_base()
