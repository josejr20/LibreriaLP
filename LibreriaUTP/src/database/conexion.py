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
                database=self.database,
                autocommit=False
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
    
    def ejecutar_query(self, query, parametros=None):
        """
        Ejecuta una query y retorna el resultado
        Útil para SELECT
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            if parametros:
                cursor.execute(query, parametros)
            else:
                cursor.execute(query)
            resultado = cursor.fetchall()
            cursor.close()
            return resultado
        except Error as e:
            print(f"Error al ejecutar query: {e}")
            return None
    
    def ejecutar_insert_update(self, query, parametros=None):
        """
        Ejecuta INSERT, UPDATE o DELETE
        Retorna True si tiene éxito
        """
        try:
            cursor = self.connection.cursor()
            if parametros:
                cursor.execute(query, parametros)
            else:
                cursor.execute(query)
            self.connection.commit()
            last_id = cursor.lastrowid
            cursor.close()
            return True, last_id
        except Error as e:
            print(f"Error al ejecutar insert/update: {e}")
            self.connection.rollback()
            return False, 0