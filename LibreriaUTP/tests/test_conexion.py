import sys
import os

from src.database.conexion import ConexionDB


def test_conexion():
    db = ConexionDB()
    conexion = db.conectar()

    if conexion is not None:
        print("TEST OK: Conexión exitosa.")
        db.cerrar_conexion()
    else:
        print("TEST FAIL: Error en la conexión.")


if __name__ == "__main__":
    test_conexion()