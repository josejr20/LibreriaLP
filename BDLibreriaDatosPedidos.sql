USE libreriautp;

CREATE TABLE carrito (
    idcarrito INT AUTO_INCREMENT PRIMARY KEY,
    idcliente INT NOT NULL,
    idproducto INT NOT NULL,
    cantidad INT NOT NULL DEFAULT 1,
    fecha_agregado DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (idcliente) REFERENCES clientes(idcliente),
    FOREIGN KEY (idproducto) REFERENCES productos(idproducto),
    UNIQUE KEY unique_cliente_producto (idcliente, idproducto)
);

-- Actualizar tabla clientes para agregar usuario y contraseña
ALTER TABLE clientes ADD COLUMN usuario VARCHAR(50) UNIQUE AFTER idcliente;
ALTER TABLE clientes ADD COLUMN contrasena VARCHAR(100) AFTER usuario;

-- Insertar un cliente
INSERT INTO clientes (usuario, contrasena, dni, nombres, apellidos, direccion, distrito, correo, celular)
VALUES ('jose', 'jose', '71609243', 'Jose', 'Jara Rojas', 'Nuev. Chimbote', 'Ancash', 'jose@gmail.com', '946559632');

-- Script para insertar datos de prueba en LibreriaUTP

USE libreriautp;

-- Insertar categorías
INSERT INTO categorias (nombre, descripcion) VALUES
('Útiles Escolares', 'Productos para el colegio y universidad'),
('Oficina', 'Artículos para oficina y escritorio'),
('Arte y Dibujo', 'Materiales de arte y dibujo técnico'),
('Tecnología', 'Productos tecnológicos y electrónicos');

-- Insertar productos
INSERT INTO productos (numero_serie, nombre, descripcion, precio, stock, color, dimensiones, idcategoria) VALUES
-- Útiles Escolares
('PROD-001', 'Cuaderno Anillado A4', 'Cuaderno universitario 100 hojas', 8.50, 50, 'Azul', '21x29.7cm', 1),
('PROD-002', 'Lapiceros Faber Castell x12', 'Caja de lapiceros colores surtidos', 15.00, 30, 'Varios', '15x10cm', 1),
('PROD-003', 'Mochila Escolar', 'Mochila resistente con múltiples compartimientos', 85.00, 20, 'Negro', '40x30x15cm', 1),
('PROD-004', 'Calculadora Científica', 'Calculadora Casio FX-991', 75.00, 15, 'Negro', '8x16cm', 1),

-- Oficina
('PROD-005', 'Archivador A4', 'Archivador de palanca tamaño A4', 12.00, 40, 'Negro', '30x28cm', 2),
('PROD-006', 'Resaltadores x4', 'Set de resaltadores colores neón', 8.00, 60, 'Varios', '12x3cm', 2),
('PROD-007', 'Engrapador Metálico', 'Engrapador profesional hasta 50 hojas', 25.00, 25, 'Gris', '15x5cm', 2),
('PROD-008', 'Papel Bond A4 x500', 'Paquete de papel bond blanco', 18.00, 100, 'Blanco', '21x29.7cm', 2),

-- Arte y Dibujo
('PROD-009', 'Set de Acuarelas x24', 'Colores de acuarela profesional', 45.00, 12, 'Varios', '20x15cm', 3),
('PROD-010', 'Lápices de Dibujo x12', 'Set de lápices grafito HB a 8B', 35.00, 18, 'Negro', '18x12cm', 3),
('PROD-011', 'Block de Dibujo A3', 'Block de 50 hojas para dibujo', 22.00, 25, 'Blanco', '42x29.7cm', 3),
('PROD-012', 'Regla T Acrílica', 'Regla T profesional 60cm', 38.00, 10, 'Transparente', '60x5cm', 3),

-- Tecnología
('PROD-013', 'Mouse Inalámbrico', 'Mouse ergonómico con receptor USB', 35.00, 30, 'Negro', '10x6cm', 4),
('PROD-014', 'Teclado USB', 'Teclado en español con cable USB', 45.00, 20, 'Negro', '45x15cm', 4),
('PROD-015', 'USB 32GB', 'Memoria USB 3.0 alta velocidad', 25.00, 50, 'Negro', '5x2cm', 4),
('PROD-016', 'Audífonos Bluetooth', 'Audífonos inalámbricos con micrófono', 120.00, 15, 'Negro', '18x8cm', 4);

-- Insertar más clientes de prueba
INSERT INTO clientes (usuario, contrasena, dni, nombres, apellidos, direccion, distrito, correo, celular) VALUES
('maria.lopez', 'maria123', '87654321', 'María', 'López Fernández', 'Jr. Los Rosales 456', 'Trujillo', 'maria.lopez@email.com', '987654322'),
('carlos.ruiz', 'carlos123', '11223344', 'Carlos', 'Ruiz Medina', 'Av. América 789', 'Victor Larco', 'carlos.ruiz@email.com', '987654323');

-- Insertar personal de delivery
INSERT INTO delivery (dni, nombres, apellidos, celular) VALUES
('55667788', 'Pedro', 'Gómez', '987111222'),
('99887766', 'Ana', 'Torres', '987333444');




