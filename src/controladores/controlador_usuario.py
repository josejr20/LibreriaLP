from src.database.conexion import ConexionDB
from src.modelos.usuario import Usuario

class ControladorUsuario:
    def autenticar_usuario(self, usuario, contrasena):
        conexion = ConexionDB()
        db = conexion.conectar()
        
        if db is None:
            print("Error: no hay conexión")
            return None

        cursor = db.cursor()
        query = "SELECT usuario, contrasena, rol, nombres, apellidos, dni FROM usuarios WHERE usuario=%s AND contrasena=%s"
        cursor.execute(query, (usuario, contrasena))
        resultado = cursor.fetchone()

        if resultado:
            print("Usuario encontrado!")
            usuario_obj = Usuario(*resultado)
            conexion.cerrar_conexion()
            return usuario_obj
        else:
            print("Credenciales incorrectas")
            conexion.cerrar_conexion()
            return None