from dataclasses import dataclass

@dataclass
class Cliente:
    idcliente: int | None
    usuario: str
    contrasena: str
    dni: str
    nombres: str
    apellidos: str
    direccion: str
    distrito: str
    correo: str
    celular: str

    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"