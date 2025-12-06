import tkinter as tk
from tkinter import ttk, messagebox
from src.funcionalidad.func_producto import FuncionalidadProducto


class MantenimientoProducto:
    def __init__(self, parent):
        self.func = FuncionalidadProducto()
        self.idcategoria_map = {}

        self.window = tk.Toplevel(parent)
        self.window.title("Mantenimiento de Productos")
        self.window.geometry("800x700")
        self.window.configure(bg="#6D8BFF")

        # Título
        title_frame = tk.Frame(self.window, bg="white", bd=4, relief="ridge")
        title_frame.pack(fill="x", pady=20, padx=20)

        tk.Label(
            title_frame,
            text="Mantenimiento de Productos",
            font=("Arial", 22, "bold"),
            bg="white"
        ).pack(pady=10)

        panel = tk.Frame(self.window, bg="white", bd=5, relief="ridge")
        panel.pack(pady=10, padx=30, fill="both", expand=True)

        form = tk.Frame(panel, bg="white")
        form.pack(pady=15)

        labels = [
            "N° Serie", "Nombre", "Descripción", "Precio",
            "Stock", "Color", "Dimensiones", "Categoría"
        ]

        self.entries = []

        for i, text in enumerate(labels[:-1]):  # los primeros 7
            tk.Label(form, text=text + ":", bg="white",
                     font=("Arial", 13, "bold")).grid(row=i, column=0, pady=8, sticky="e")

            entry = ttk.Entry(form, width=35)
            entry.grid(row=i, column=1, pady=8)
            self.entries.append(entry)

        # Estilo
        tk.Label(
            form,
            text="Categoría:",
            bg="white",
            font=("Arial", 13, "bold")
        ).grid(row=7, column=0, pady=8, sticky="e")

        self.cmb_categoria = ttk.Combobox(form, width=33, state="readonly")
        self.cmb_categoria.grid(row=7, column=1, pady=8)

        self.cargar_categorias()

        # Botones
        btn_frame = tk.Frame(panel, bg="white")
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="Buscar", width=16, command=self.buscar).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Registrar", width=16, command=self.registrar).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Modificar", width=16, command=self.modificar).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Eliminar", width=16, command=self.eliminar).grid(row=0, column=3, padx=5)

    # Auxiliar
    def cargar_categorias(self):
        categorias = self.func.obtener_categorias()
        nombres = []

        for cid, nombre in categorias:
            self.idcategoria_map[nombre] = cid
            nombres.append(nombre)

        self.cmb_categoria["values"] = nombres

    def limpiar(self):
        for e in self.entries:
            e.delete(0, tk.END)
        self.cmb_categoria.set("")

    # Buscar
    def buscar(self):
        numero_serie = self.entries[0].get()
        prod = self.func.buscar(numero_serie)

        if not prod:
            return

        datos = [
            prod.nombre, prod.descripcion, prod.precio, prod.stock,
            prod.color, prod.dimensiones
        ]

        for i, val in enumerate(datos):
            self.entries[i + 1].delete(0, tk.END)
            self.entries[i + 1].insert(0, val)

        # Categoría
        for nombre, cid in self.idcategoria_map.items():
            if cid == prod.idcategoria:
                self.cmb_categoria.set(nombre)
                break

    # Registrar
    def registrar(self):
        numero_serie = self.entries[0].get()
        nombre = self.entries[1].get()
        descripcion = self.entries[2].get()
        precio = self.entries[3].get()
        stock = self.entries[4].get()
        color = self.entries[5].get()
        dimensiones = self.entries[6].get()
        categoria_nombre = self.cmb_categoria.get()
        idcategoria = self.idcategoria_map.get(categoria_nombre)

        if self.func.registrar(
                numero_serie, nombre, descripcion, precio,
                stock, color, dimensiones, idcategoria
        ):
            self.limpiar()

    # Modificar
    def modificar(self):
        numero_serie = self.entries[0].get()
        nombre = self.entries[1].get()
        descripcion = self.entries[2].get()
        precio = self.entries[3].get()
        stock = self.entries[4].get()
        color = self.entries[5].get()
        dimensiones = self.entries[6].get()
        categoria_nombre = self.cmb_categoria.get()
        idcategoria = self.idcategoria_map.get(categoria_nombre)

        if self.func.modificar(
                numero_serie, nombre, descripcion, precio,
                stock, color, dimensiones, idcategoria
        ):
            self.limpiar()

    # Eliminar
    def eliminar(self):
        numero_serie = self.entries[0].get()

        if self.func.eliminar(numero_serie):
            self.limpiar()
