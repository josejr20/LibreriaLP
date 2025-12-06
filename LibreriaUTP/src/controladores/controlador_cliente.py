from src.database.conexion import ConexionDB
from src.modelos.cliente import Cliente

class ControladorCliente:

    def registrar(self, cliente: Cliente):
        conexion = ConexionDB()
        db = conexion.conectar()
        if not db:
            return False

        query = """
            INSERT INTO clientes
            (usuario, contrasena, dni, nombres, apellidos, direccion, distrito, correo, celular)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor = db.cursor()
        cursor.execute(query, (
            cliente.usuario,
            cliente.contrasena,
            cliente.dni,
            cliente.nombres,
            cliente.apellidos,
            cliente.direccion,
            cliente.distrito,
            cliente.correo,
            cliente.celular
        ))

        db.commit()
        conexion.cerrar_conexion()
        return True

    # ----------------------------------------------------------

    def buscar(self, parametro):
        conexion = ConexionDB()
        db = conexion.conectar()
        if not db:
            return None

        cursor = db.cursor()

        # Si es posible DNI exacto
        if parametro.isdigit():
            cursor.execute("""
                SELECT idcliente, usuario, contrasena, dni, nombres, apellidos,
                        direccion, distrito, correo, celular
                FROM clientes
                WHERE dni = %s
                LIMIT 1
            """, (parametro,))
            fila = cursor.fetchone()
            if fila:
                conexion.cerrar_conexion()
                return Cliente(*fila)

        # Búsqueda parcial
        like = f"%{parametro}%"
        cursor.execute("""
            SELECT idcliente, usuario, contrasena, dni, nombres, apellidos,
                    direccion, distrito, correo, celular
            FROM clientes
            WHERE nombres LIKE %s OR apellidos LIKE %s OR dni LIKE %s
            ORDER BY nombres ASC
            LIMIT 1
        """, (like, like, like))

        fila = cursor.fetchone()
        conexion.cerrar_conexion()
        return Cliente(*fila) if fila else None

    # ----------------------------------------------------------

    def modificar(self, cliente: Cliente):
        conexion = ConexionDB()
        db = conexion.conectar()
        cursor = db.cursor()

        query = """
            UPDATE clientes
            SET usuario=%s, contrasena=%s, nombres=%s, apellidos=%s, direccion=%s,
                distrito=%s, correo=%s, celular=%s
            WHERE dni=%s
        """

        cursor.execute(query, (
            cliente.usuario,
            cliente.contrasena,
            cliente.nombres,
            cliente.apellidos,
            cliente.direccion,
            cliente.distrito,
            cliente.correo,
            cliente.celular,
            cliente.dni
        ))

        db.commit()
        conexion.cerrar_conexion()
        return True

    # ----------------------------------------------------------

    def eliminar(self, dni):
        conexion = ConexionDB()
        db = conexion.conectar()
        cursor = db.cursor()

        cursor.execute("DELETE FROM clientes WHERE dni=%s", (dni,))
        db.commit()
        conexion.cerrar_conexion()
        return True