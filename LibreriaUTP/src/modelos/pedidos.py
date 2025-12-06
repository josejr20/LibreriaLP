from src.database.conexion import ConexionDB


class ModeloPedidos:

    def actualizar_pedido(self, id_pedido, fecha_entrega, observaciones, estado):
        try:
            conn = ConexionDB().get_connection()
            cursor = conn.cursor()

            query = """
                UPDATE pedidos
                SET fecha_entrega = %s,
                    observaciones = %s,
                    estado = %s
                WHERE id_pedido = %s
            """

            cursor.execute(query, (fecha_entrega, observaciones, estado, id_pedido))
            conn.commit()

            cursor.close()
            conn.close()
            return True

        except Exception as e:
            print("Error al actualizar pedido:", e)
            return False
