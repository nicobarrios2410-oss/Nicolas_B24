-- Script opcional: crea la base de datos, el usuario y la tabla manualmente.
-- Ejecutar como root:  mariadb -u root -p < schema.sql

CREATE DATABASE IF NOT EXISTS biblioteca
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'biblioteca_user'@'localhost' IDENTIFIED BY 'biblioteca_pass';
GRANT ALL PRIVILEGES ON biblioteca.* TO 'biblioteca_user'@'localhost';
FLUSH PRIVILEGES;

USE biblioteca;

CREATE TABLE IF NOT EXISTS libros (
  id INT AUTO_INCREMENT PRIMARY KEY,
  titulo VARCHAR(200) NOT NULL,
  autor VARCHAR(150) NOT NULL,
  genero VARCHAR(100) NOT NULL,
  estado_lectura VARCHAR(20) NOT NULL DEFAULT 'Pendiente',
  CONSTRAINT uq_titulo_autor UNIQUE (titulo, autor),
  INDEX ix_libros_titulo (titulo),
  INDEX ix_libros_autor (autor),
  INDEX ix_libros_genero (genero)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
