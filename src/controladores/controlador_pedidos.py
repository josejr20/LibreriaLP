from src.database.conexion import ConexionDB

class ControladorPedidos:
    def __init__(self):
        self.conexion = ConexionDB()

    def obtener_personal_delivery(self):
        db = self.conexion.conectar()
        if db is None:
            return []
        
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM delivery"
        cursor.execute(query)
        resultado = cursor.fetchall()
        self.conexion.cerrar_conexion()
        return resultado

    def obtener_productos(self):
        db = self.conexion.conectar()
        if db is None:
            return []
        
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM productos WHERE stock > 0"
        cursor.execute(query)
        resultado = cursor.fetchall()
        self.conexion.cerrar_conexion()
        return resultado

    def obtener_producto_por_serie(self, numero_serie):
        db = self.conexion.conectar()
        if db is None:
            return None
        
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM productos WHERE numero_serie = %s"
        cursor.execute(query, (numero_serie,))
        resultado = cursor.fetchone()
        self.conexion.cerrar_conexion()
        return resultado

    def buscar_cliente_por_dni(self, dni):
        db = self.conexion.conectar()
        if db is None:
            return None
        
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM clientes WHERE dni = %s"
        cursor.execute(query, (dni,))
        resultado = cursor.fetchone()
        self.conexion.cerrar_conexion()
        return resultado

    def obtener_delivery_por_dni(self, dni):
        db = self.conexion.conectar()
        if db is None:
            return None
        
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM delivery WHERE dni = %s"
        cursor.execute(query, (dni,))
        resultado = cursor.fetchone()
        self.conexion.cerrar_conexion()
        return resultado

    def registrar_pedido(self, numero_pedido, fecha_pedido, fecha_entrega, observaciones,
                        subtotal, igv, total, idcliente, idusuario, iddelivery, productos):
        db = self.conexion.conectar()
        if db is None:
            return False
        
        try:
            cursor = db.cursor()
            
            # Insertar pedido
            query_pedido = """
                INSERT INTO pedidos 
                (numero_pedido, fecha_pedido, fecha_entrega, observaciones, 
                 subtotal, igv, total, idcliente, idusuario, iddelivery, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'pendiente')
            """
            cursor.execute(query_pedido, (
                numero_pedido, fecha_pedido, fecha_entrega, observaciones,
                subtotal, igv, total, idcliente, idusuario, iddelivery
            ))
            
            idpedido = cursor.lastrowid
            
            # Insertar detalles del pedido
            query_detalle = """
                INSERT INTO detalle_pedido 
                (idpedido, idproducto, cantidad, precio_unit, subtotal)
                VALUES (%s, %s, %s, %s, %s)
            """
            
            for producto in productos:
                cursor.execute(query_detalle, (
                    idpedido,
                    producto['idproducto'],
                    producto['cantidad'],
                    producto['precio'],
                    producto['subtotal']
                ))
                
                # Actualizar stock
                query_stock = "UPDATE productos SET stock = stock - %s WHERE idproducto = %s"
                cursor.execute(query_stock, (producto['cantidad'], producto['idproducto']))
            
            db.commit()
            self.conexion.cerrar_conexion()
            return True
            
        except Exception as e:
            print(f"Error al registrar pedido: {e}")
            db.rollback()
            self.conexion.cerrar_conexion()
            return False

    def buscar_pedidos_por_cliente(self, criterio, valor):
        db = self.conexion.conectar()
        if db is None:
            return []
        
        cursor = db.cursor(dictionary=True)
        
        if criterio == "nombre":
            query = """
                SELECT p.*, c.nombres, c.apellidos, c.dni as dni_cliente
                FROM pedidos p
                INNER JOIN clientes c ON p.idcliente = c.idcliente
                WHERE c.nombres LIKE %s
                ORDER BY p.fecha_pedido DESC
            """
            cursor.execute(query, (f"%{valor}%",))
        elif criterio == "apellido":
            query = """
                SELECT p.*, c.nombres, c.apellidos, c.dni as dni_cliente
                FROM pedidos p
                INNER JOIN clientes c ON p.idcliente = c.idcliente
                WHERE c.apellidos LIKE %s
                ORDER BY p.fecha_pedido DESC
            """
            cursor.execute(query, (f"%{valor}%",))
        elif criterio == "rango_fechas":
            fecha_desde, fecha_hasta = valor
            query = """
                SELECT p.*, c.nombres, c.apellidos, c.dni as dni_cliente
                FROM pedidos p
                INNER JOIN clientes c ON p.idcliente = c.idcliente
                WHERE p.fecha_pedido BETWEEN %s AND %s
                ORDER BY p.fecha_pedido DESC
            """
            cursor.execute(query, (fecha_desde, fecha_hasta))
        
        resultado = cursor.fetchall()
        self.conexion.cerrar_conexion()
        return resultado

    def obtener_detalle_pedido(self, idpedido):
        db = self.conexion.conectar()
        if db is None:
            return []
        
        cursor = db.cursor(dictionary=True)
        query = """
            SELECT dp.*, pr.nombre, pr.numero_serie
            FROM detalle_pedido dp
            INNER JOIN productos pr ON dp.idproducto = pr.idproducto
            WHERE dp.idpedido = %s
        """
        cursor.execute(query, (idpedido,))
        resultado = cursor.fetchall()
        self.conexion.cerrar_conexion()
        return resultado

    def registrar_entrega(self, idpedido, fecha_entrega, observaciones):
        db = self.conexion.conectar()
        if db is None:
            return False
        
        try:
            cursor = db.cursor()
            
            # Insertar entrega
            query_entrega = """
                INSERT INTO entregas (idpedido, fecha_entrega, observaciones)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query_entrega, (idpedido, fecha_entrega, observaciones))
            
            # Actualizar estado del pedido
            query_update = "UPDATE pedidos SET estado = 'entregado' WHERE idpedido = %s"
            cursor.execute(query_update, (idpedido,))
            
            db.commit()
            self.conexion.cerrar_conexion()
            return True
            
        except Exception as e:
            print(f"Error al registrar entrega: {e}")
            db.rollback()
            self.conexion.cerrar_conexion()
            return False

    def obtener_pedidos_pendientes_por_cliente(self, dni_cliente):
        db = self.conexion.conectar()
        if db is None:
            return []
        
        cursor = db.cursor(dictionary=True)
        query = """
            SELECT p.*, c.nombres, c.apellidos
            FROM pedidos p
            INNER JOIN clientes c ON p.idcliente = c.idcliente
            WHERE c.dni = %s AND p.estado != 'entregado'
            ORDER BY p.fecha_pedido DESC
        """
        cursor.execute(query, (dni_cliente,))
        resultado = cursor.fetchall()
        self.conexion.cerrar_conexion()
        return resultado

    def obtener_pedidos_por_delivery(self, dni_delivery):
        db = self.conexion.conectar()
        if db is None:
            return []
        
        cursor = db.cursor(dictionary=True)
        query = """
            SELECT p.*, c.nombres, c.apellidos, d.nombres as delivery_nombres, d.apellidos as delivery_apellidos
            FROM pedidos p
            INNER JOIN clientes c ON p.idcliente = c.idcliente
            INNER JOIN delivery d ON p.iddelivery = d.iddelivery
            WHERE d.dni = %s AND p.estado != 'entregado'
            ORDER BY p.fecha_pedido DESC
        """
        cursor.execute(query, (dni_delivery,))
        resultado = cursor.fetchall()
        self.conexion.cerrar_conexion()
        return resultado