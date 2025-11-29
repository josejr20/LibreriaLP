DROP DATABASE IF EXISTS LibreriaUTP;
CREATE DATABASE LibreriaUTP;
USE LibreriaUTP;

CREATE TABLE usuarios (
    idusuario INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    contrasena VARCHAR(100) NOT NULL,
    rol ENUM('administrador', 'empleado') NOT NULL,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    dni VARCHAR(8) UNIQUE
);

CREATE TABLE clientes (
    idcliente INT AUTO_INCREMENT PRIMARY KEY,
    dni VARCHAR(8) NOT NULL UNIQUE,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    direccion VARCHAR(150),
    distrito VARCHAR(100),
    correo VARCHAR(100),
    celular VARCHAR(9)
);

CREATE TABLE categorias (
    idcategoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255)
);

CREATE TABLE productos (
    idproducto INT AUTO_INCREMENT PRIMARY KEY,
    numero_serie VARCHAR(50) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255),
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    color VARCHAR(50),
    dimensiones VARCHAR(100),
    idcategoria INT,
    FOREIGN KEY (idcategoria) REFERENCES categorias(idcategoria)
);

CREATE TABLE delivery (
    iddelivery INT AUTO_INCREMENT PRIMARY KEY,
    dni VARCHAR(8) UNIQUE NOT NULL,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    celular VARCHAR(9)
);

CREATE TABLE pedidos (
    idpedido INT AUTO_INCREMENT PRIMARY KEY,
    numero_pedido VARCHAR(20) NOT NULL UNIQUE,
    fecha_pedido DATE NOT NULL,
    fecha_entrega DATE,
    observaciones VARCHAR(255),
    subtotal DECIMAL(10,2),
    igv DECIMAL(10,2),
    total DECIMAL(10,2),
    estado ENUM('pendiente','en_proceso','entregado','anulado') DEFAULT 'pendiente',
    idcliente INT NOT NULL,
    idusuario INT NOT NULL,
    iddelivery INT,
    FOREIGN KEY (idcliente) REFERENCES clientes(idcliente),
    FOREIGN KEY (idusuario) REFERENCES usuarios(idusuario),
    FOREIGN KEY (iddelivery) REFERENCES delivery(iddelivery)
);

CREATE TABLE detalle_pedido (
    iddetalle INT AUTO_INCREMENT PRIMARY KEY,
    idpedido INT NOT NULL,
    idproducto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unit DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (idpedido) REFERENCES pedidos(idpedido),
    FOREIGN KEY (idproducto) REFERENCES productos(idproducto)
);

CREATE TABLE entregas (
    identrega INT AUTO_INCREMENT PRIMARY KEY,
    idpedido INT NOT NULL,
    fecha_entrega DATE NOT NULL,
    observaciones VARCHAR(255),
    FOREIGN KEY (idpedido) REFERENCES pedidos(idpedido)
);