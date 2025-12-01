import mysql.connector
from mysql.connector import Error

class ConexionDB:
    def __init__(self, host="localhost", user="root", password="jose20", database="libreriautp"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def conectar(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            if self.connection.is_connected():
                print("Conexión exitosa a la base de datos")
                return self.connection

        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None

    def cerrar_conexion(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión cerrada")