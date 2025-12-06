from dataclasses import dataclass

@dataclass
class Categoria:
    idcategoria: int | None
    nombre: str
    descripcion: str