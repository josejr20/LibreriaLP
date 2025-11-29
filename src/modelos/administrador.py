from dataclasses import dataclass
from src.modelos.usuario import Usuario

@dataclass
class Administrador:
    usuario: Usuario

    def obtener_nombre(self):
        return self.usuario.nombre_completo()