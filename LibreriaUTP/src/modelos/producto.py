from dataclasses import dataclass

@dataclass
class Producto:
    idproducto: int | None
    numero_serie: str
    nombre: str
    descripcion: str
    precio: float
    stock: int
    color: str
    dimensiones: str
    idcategoria: int