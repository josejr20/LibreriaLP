from src.modelos.administrador import Administrador

class ControladorAdministrador:
    def __init__(self, usuario):
        self.admin = Administrador(usuario)

    def obtener_datos(self):
        return {
            "usuario": self.admin.usuario.usuario,
            "nombre": self.admin.obtener_nombre(),
            "rol": self.admin.usuario.rol
        }