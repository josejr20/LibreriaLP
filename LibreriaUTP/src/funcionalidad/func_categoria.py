from tkinter import messagebox
from src.controladores.controlador_categoria import ControladorCategoria
from src.modelos.categoria import Categoria

class FuncionalidadCategoria:
    def __init__(self):
        self.controller = ControladorCategoria()

    # Registrar
    def registrar(self, nombre, descripcion):
        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio.")
            return False

        categoria = Categoria(None, nombre, descripcion)

        try:
            self.controller.registrar(categoria)
            messagebox.showinfo("Éxito", "Categoría registrada correctamente.")
            return True
        except Exception as e:
            messagebox.showerror("Error SQL", str(e))
            return False

    # Buscar
    def buscar(self, nombre):
        if not nombre:
            messagebox.showerror("Error", "Ingrese un nombre para buscar.")
            return None

        try:
            categoria = self.controller.buscar(nombre)
        except Exception as e:
            messagebox.showerror("Error SQL", str(e))
            return None

        if not categoria:
            messagebox.showwarning("Aviso", "Categoría no encontrada.")
            return None

        return categoria

    # Modificar
    def modificar(self, idcategoria, nombre, descripcion):
        if not idcategoria:
            messagebox.showerror("Error", "Primero busque una categoría.")
            return False

        categoria = Categoria(idcategoria, nombre, descripcion)

        try:
            self.controller.modificar(categoria)
            messagebox.showinfo("Éxito", "Categoría modificada correctamente.")
            return True
        except Exception as e:
            messagebox.showerror("Error SQL", str(e))
            return False

    # Eliminar
    def eliminar(self, idcategoria):
        if not idcategoria:
            messagebox.showerror("Error", "Primero busque una categoría.")
            return False

        try:
            self.controller.eliminar(idcategoria)
            messagebox.showinfo("Éxito", "Categoría eliminada correctamente.")
            return True
        except Exception as e:
            messagebox.showerror("Error SQL", str(e))
            return False
