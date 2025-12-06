from src.database.conexion import ConexionDB
from src.modelos.categoria import Categoria

class ControladorCategoria:

    def registrar(self, categoria: Categoria):
        conexion = ConexionDB()
        db = conexion.conectar()

        query = "INSERT INTO categorias (nombre, descripcion) VALUES (%s, %s)"
        cursor = db.cursor()
        cursor.execute(query, (categoria.nombre, categoria.descripcion))
        db.commit()
        conexion.cerrar_conexion()
        return True

    def buscar(self, nombre):
        conexion = ConexionDB()
        db = conexion.conectar()

        cursor = db.cursor()
        cursor.execute("SELECT * FROM categorias WHERE nombre=%s", (nombre,))
        fila = cursor.fetchone()
        conexion.cerrar_conexion()

        return Categoria(*fila) if fila else None

    def modificar(self, categoria: Categoria):
        conexion = ConexionDB()
        db = conexion.conectar()

        query = "UPDATE categorias SET nombre=%s, descripcion=%s WHERE idcategoria=%s"
        cursor = db.cursor()
        cursor.execute(query, (categoria.nombre, categoria.descripcion, categoria.idcategoria))
        db.commit()
        conexion.cerrar_conexion()
        return True

    def eliminar(self, idcategoria):
        conexion = ConexionDB()
        db = conexion.conectar()

        cursor = db.cursor()
        cursor.execute("DELETE FROM categorias WHERE idcategoria=%s", (idcategoria,))
        db.commit()
        conexion.cerrar_conexion()
        return True