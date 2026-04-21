CREATE DATABASE inventario_db;
USE inventario_db;

CREATE TABLE categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre_categoria VARCHAR(100)
);

CREATE TABLE productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre_producto VARCHAR(100),
    descripcion TEXT,
    stock INT,
    precio DECIMAL(10,2),
    id_categoria INT,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
);

CREATE TABLE movimientos (
    id_movimiento INT AUTO_INCREMENT PRIMARY KEY,
    id_producto INT,
    cantidad INT,
    tipo_movimiento ENUM('entrada', 'salida'),
    fecha_movimiento DATETIME,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(50) UNIQUE,
    email VARCHAR(100) UNIQUE,
    contraseña VARCHAR(255),
    rol ENUM('admin', 'usuario'),
    activo BOOLEAN DEFAULT TRUE
);