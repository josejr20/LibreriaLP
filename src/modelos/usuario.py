from dataclasses import dataclass, field
import hashlib
import secrets
import re

@dataclass
class Usuario:
    usuario: str
    contrasena: str
    rol: str
    nombres: str
    apellidos: str
    dni: str
    contrasena_hash: str = field(default="", init=False)

    def nombre_completo(self) -> str:
        return f"{self.nombres} {self.apellidos}"

    def set_password(self, password: str) -> None:
        salt = secrets.token_hex(16)
        hash_hex = hashlib.sha256((salt + password).encode()).hexdigest()
        self.contrasena_hash = f"{salt}${hash_hex}"

    def verificar_contrasena(self, password: str) -> bool:
        
        if not self.contrasena_hash:
            return False
        
        salt, stored_hash = self.contrasena_hash.split("$", 1)
        hash_hex = hashlib.sha256((salt + password).encode()).hexdigest()
        return secrets.compare_digest(hash_hex, stored_hash)

    def validar(self):
        checks = [
            (lambda u: bool(u.usuario.strip()), "Usuario vacío"),
            (lambda u: u.rol in ("cliente", "empleado", "administrador"), "Rol inválido"),
            (lambda u: re.fullmatch(r"\d{8}", u.dni) is not None, "DNI inválido"),
        ]

        errores = [mensaje for (pred, mensaje) in checks if not pred(self)]
        return (len(errores) == 0, errores)