from decimal import Decimal
from src.database.conexion import ConexionDB

class ControladorConsultaDelivery:
    def __init__(self):
        self.conexion = ConexionDB()

    def obtener_pedidos_entregados_por_delivery(self, iddelivery):
        db = self.conexion.conectar()
        if db is None:
            return []

        cursor = db.cursor(dictionary=True)

        query = """
            SELECT p.*, 
                c.nombres AS cliente_nombres, 
                c.apellidos AS cliente_apellidos
            FROM pedidos p
            INNER JOIN clientes c ON c.idcliente = p.idcliente
            WHERE p.iddelivery = %s
            AND p.estado = 'entregado'
            ORDER BY p.fecha_entrega DESC
        """

        cursor.execute(query, (iddelivery,))
        resultado = cursor.fetchall()
        self.conexion.cerrar_conexion()

        # Convertir Decimals a float
        resultados_convertidos = []
        for r in resultado:
            rd = dict(r)
            for key, value in rd.items():
                if isinstance(value, Decimal):
                    rd[key] = float(value)
            resultados_convertidos.append(rd)

        return resultados_convertidos
    
    # ----------------------------------------------------------------------
    # OBTENER PEDIDOS PENDIENTES POR UN DELIVERY
    # ----------------------------------------------------------------------
    def obtener_pedidos_pendientes_por_delivery(self, iddelivery):
        db = self.conexion.conectar()
        if db is None:
            return []

        cursor = db.cursor(dictionary=True)

        query = """
            SELECT p.*, 
                c.nombres AS cliente_nombres,
                c.apellidos AS cliente_apellidos
            FROM pedidos p
            INNER JOIN clientes c ON c.idcliente = p.idcliente
            WHERE p.iddelivery = %s
            AND p.estado = 'pendiente'
            ORDER BY p.fecha_pedido ASC
        """

        cursor.execute(query, (iddelivery,))
        resultado = cursor.fetchall()
        self.conexion.cerrar_conexion()

        # Convertir Decimal → float
        resultados_convertidos = []
        for r in resultado:
            rd = dict(r)
            for key, value in rd.items():
                if isinstance(value, Decimal):
                    rd[key] = float(value)
            resultados_convertidos.append(rd)

        return resultados_convertidos
