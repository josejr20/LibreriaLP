from src.database.conexion import ConexionDB

class DeliveryController:

    def __init__(self):
        self.conn = ConexionDB()

    # ----------------------------------------------------------------------
    # 1. BUSCAR PERSONAL DELIVERY POR NOMBRE, APELLIDO O DNI
    # ----------------------------------------------------------------------
    def buscar_delivery(self, texto):
        """
        Busca personal delivery por nombre, apellido o DNI.
        """
        try:
            conexion = self.conn.conectar()
            cursor = conexion.cursor(dictionary=True)

            query = """
                SELECT iddelivery, nombres, apellidos, dni
                FROM delivery
                WHERE nombres LIKE %s
                OR apellidos LIKE %s
                OR dni LIKE %s;
            """

            like_text = f"%{texto}%"
            cursor.execute(query, (like_text, like_text, like_text))

            resultados = cursor.fetchall()
            cursor.close()
            conexion.close()

            return resultados

        except Exception as e:
            print("Error en buscar_delivery:", e)
            return []


    # ----------------------------------------------------------------------
    # 2. OBTENER PEDIDOS ENTREGADOS POR UN DELIVERY
    # ----------------------------------------------------------------------
    def obtener_pedidos_entregados(self, iddelivery):
        """
        Devuelve todos los pedidos ENTREGADOS por un personal delivery.
        """
        try:
            conexion = self.conn.conectar()
            cursor = conexion.cursor(dictionary=True)

            query = """
                SELECT 
                    p.idpedido,
                    p.numero_pedido,
                    p.fecha_pedido,
                    p.fecha_entrega,
                    p.observaciones,
                    p.total,
                    c.nombres AS cliente_nombre,
                    c.apellidos AS cliente_apellidos
                FROM pedidos p
                INNER JOIN clientes c ON c.idcliente = p.idcliente
                WHERE p.iddelivery = %s
                AND p.estado = 'entregado'
                ORDER BY p.fecha_entrega DESC;
            """

            cursor.execute(query, (iddelivery,))

            pedidos = cursor.fetchall()

            cursor.close()
            conexion.close()

            return pedidos

        except Exception as e:
            print("Error en obtener_pedidos_entregados:", e)
            return []
