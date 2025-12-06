from src.database.conexion import ConexionDB
from src.modelos.producto import Producto

class ControladorProducto:

    def registrar(self, p: Producto):
        conexion = ConexionDB()
        db = conexion.conectar()

        query = """
        INSERT INTO productos (numero_serie, nombre, descripcion, precio, stock, color, dimensiones, idcategoria)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor = db.cursor()
        cursor.execute(query, (
            p.numero_serie, p.nombre, p.descripcion, p.precio,
            p.stock, p.color, p.dimensiones, p.idcategoria
        ))
        db.commit()
        conexion.cerrar_conexion()
        return True

    def buscar(self, numero_serie):
        conexion = ConexionDB()
        db = conexion.conectar()

        cursor = db.cursor()
        cursor.execute("SELECT * FROM productos WHERE numero_serie=%s", (numero_serie,))
        fila = cursor.fetchone()
        conexion.cerrar_conexion()

        return Producto(*fila) if fila else None

    def modificar(self, p: Producto):
        conexion = ConexionDB()
        db = conexion.conectar()

        query = """
        UPDATE productos
        SET nombre=%s, descripcion=%s, precio=%s, stock=%s,
            color=%s, dimensiones=%s, idcategoria=%s
        WHERE numero_serie=%s
        """

        cursor = db.cursor()
        cursor.execute(query, (
            p.nombre, p.descripcion, p.precio, p.stock,
            p.color, p.dimensiones, p.idcategoria,
            p.numero_serie
        ))

        db.commit()
        conexion.cerrar_conexion()
        return True

    def eliminar(self, numero_serie):
        conexion = ConexionDB()
        db = conexion.conectar()

        cursor = db.cursor()
        cursor.execute("DELETE FROM productos WHERE numero_serie=%s", (numero_serie,))
        db.commit()
        conexion.cerrar_conexion()
        return True