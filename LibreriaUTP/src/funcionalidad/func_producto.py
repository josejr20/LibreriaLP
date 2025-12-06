from tkinter import messagebox
from src.controladores.controlador_producto import ControladorProducto
from src.controladores.controlador_categoria import ControladorCategoria
from src.modelos.producto import Producto


class FuncionalidadProducto:
    def __init__(self):
        self.controller = ControladorProducto()
        self.controller_categoria = ControladorCategoria()

    # Listar categorias
    def obtener_categorias(self):
        try:
            conexion = self.controller_categoria
            db = conexion = conexion
        except:
            pass

        conexion = self.controller_categoria
        db = conexion
        conexiondb = conexion

        try:
            import mysql.connector
            from src.database.conexion import ConexionDB

            con = ConexionDB()
            db = con.conectar()
            cursor = db.cursor()
            cursor.execute("SELECT idcategoria, nombre FROM categorias")
            datos = cursor.fetchall()
            con.cerrar_conexion()
            return datos
        except:
            messagebox.showerror("Error", "No se pudieron cargar las categorías.")
            return []

    # Registrar
    def registrar(self, numero_serie, nombre, descripcion, precio, stock, color, dimensiones, idcategoria):
        if not numero_serie or not nombre:
            messagebox.showerror("Error", "Número de serie y nombre son obligatorios.")
            return False

        if precio == "" or stock == "":
            messagebox.showerror("Error", "Precio y stock son obligatorios.")
            return False

        try:
            precio = float(precio)
            stock = int(stock)
        except:
            messagebox.showerror("Error", "Precio debe ser decimal y stock un número entero.")
            return False

        producto = Producto(
            None, numero_serie, nombre, descripcion, precio,
            stock, color, dimensiones, idcategoria
        )

        try:
            self.controller.registrar(producto)
            messagebox.showinfo("Éxito", "Producto registrado correctamente.")
            return True
        except Exception as e:
            messagebox.showerror("Error SQL", str(e))
            return False

    # Buscar
    def buscar(self, numero_serie):
        if not numero_serie:
            messagebox.showerror("Error", "Ingrese número de serie.")
            return None

        try:
            producto = self.controller.buscar(numero_serie)
        except Exception as e:
            messagebox.showerror("Error SQL", str(e))
            return None

        if not producto:
            messagebox.showwarning("Aviso", "Producto no encontrado.")
            return None

        return producto

    # Modificar
    def modificar(self, numero_serie, nombre, descripcion, precio, stock, color, dimensiones, idcategoria):
        if not numero_serie:
            messagebox.showerror("Error", "Debe buscar primero un producto.")
            return False

        try:
            precio = float(precio)
            stock = int(stock)
        except:
            messagebox.showerror("Error", "Precio debe ser decimal y stock un número entero.")
            return False

        producto = Producto(
            None, numero_serie, nombre, descripcion, precio,
            stock, color, dimensiones, idcategoria
        )

        try:
            self.controller.modificar(producto)
            messagebox.showinfo("Éxito", "Producto modificado correctamente.")
            return True
        except Exception as e:
            messagebox.showerror("Error SQL", str(e))
            return False

    # Eliminar
    def eliminar(self, numero_serie):
        if not numero_serie:
            messagebox.showerror("Error", "Ingrese número de serie para eliminar.")
            return False

        try:
            self.controller.eliminar(numero_serie)
            messagebox.showinfo("Éxito", "Producto eliminado.")
            return True
        except Exception as e:
            messagebox.showerror("Error SQL", str(e))
            return False
