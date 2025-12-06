import tkinter as tk
from tkinter import ttk, messagebox
from src.funcionalidad.func_categoria import FuncionalidadCategoria


class MantenimientoCategoria:
    def __init__(self, parent):
        self.func = FuncionalidadCategoria()
        self.id_actual = None

        self.window = tk.Toplevel(parent)
        self.window.title("Mantenimiento de Categorías")
        self.window.geometry("700x500")
        self.window.configure(bg="#6D8BFF")

        # Título
        title_frame = tk.Frame(self.window, bg="white", bd=4, relief="ridge")
        title_frame.pack(fill="x", pady=20, padx=20)

        tk.Label(
            title_frame,
            text="Mantenimiento de Categorías",
            font=("Arial", 22, "bold"),
            bg="white"
        ).pack(pady=10)

        # Panel principal
        panel = tk.Frame(self.window, bg="white", bd=5, relief="ridge")
        panel.pack(pady=10, padx=30, fill="both", expand=True)

        # Formulario
        form = tk.Frame(panel, bg="white")
        form.pack(pady=20)

        tk.Label(form, text="Nombre:", bg="white", font=("Arial", 13, "bold")).grid(row=0, column=0, pady=10, sticky="e")
        tk.Label(form, text="Descripción:", bg="white", font=("Arial", 13, "bold")).grid(row=1, column=0, pady=10, sticky="e")

        self.txt_nombre = ttk.Entry(form, width=40)
        self.txt_descripcion = ttk.Entry(form, width=40)

        self.txt_nombre.grid(row=0, column=1, pady=10)
        self.txt_descripcion.grid(row=1, column=1, pady=10)

        # Botones
        btn_frame = tk.Frame(panel, bg="white")
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="Buscar", width=18, command=self.buscar).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Registrar", width=18, command=self.registrar).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Modificar", width=18, command=self.modificar).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Eliminar", width=18, command=self.eliminar).grid(row=0, column=3, padx=5)

    # Auxilar
    def limpiar(self):
        self.txt_nombre.delete(0, tk.END)
        self.txt_descripcion.delete(0, tk.END)
        self.id_actual = None

    # Buscar
    def buscar(self):
        nombre = self.txt_nombre.get()

        categoria = self.func.buscar(nombre)
        if not categoria:
            return

        # Se guarda el id para modificar / eliminar
        self.id_actual = categoria.idcategoria

        # Cargar descripción
        self.txt_descripcion.delete(0, tk.END)
        self.txt_descripcion.insert(0, categoria.descripcion)

    # Registrar
    def registrar(self):
        nombre = self.txt_nombre.get()
        descripcion = self.txt_descripcion.get()

        if self.func.registrar(nombre, descripcion):
            self.limpiar()

    # Modificar
    def modificar(self):
        nombre = self.txt_nombre.get()
        descripcion = self.txt_descripcion.get()

        if self.func.modificar(self.id_actual, nombre, descripcion):
            self.limpiar()

    # Eliminar
    def eliminar(self):
        if self.func.eliminar(self.id_actual):
            self.limpiar()
