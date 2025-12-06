import tkinter as tk
from tkinter import ttk
from src.controladores.controlador_administrador import ControladorAdministrador

from src.vistas.mantenimiento_cliente import MantenimientoCliente
from src.vistas.mantenimiento_categoria import MantenimientoCategoria
from src.vistas.mantenimiento_producto import MantenimientoProducto


class Mantenimiento:
    def __init__(self, ventana_padre, usuario):
        self.ventana_padre = ventana_padre
        self.controlador = ControladorAdministrador(usuario)


        #Toplevel no queremos crear un segundo Tk()
        self.window = tk.Toplevel()
        self.window.title("Panel Administrador - Librería UTP")
        self.window.geometry("850x600")
        self.window.configure(bg="#6D8BFF")

        self.window.protocol("WM_DELETE_WINDOW", self.volver)

        # Encabezado
        header_frame = tk.Frame(self.window, bg="white", bd=3, relief="ridge")
        header_frame.pack(fill="x", pady=20, padx=20)

        lbl_header = tk.Label( header_frame, text="Panel del Administrador", font=("Arial", 24, "bold"), bg="white"
        )
        lbl_header.pack(pady=10)


        # Opciones
        tk.Label(
            self.window, text="Seleccione una opción", font=("Arial", 16, "bold"), bg="#6D8BFF", fg="white"
        ).pack(pady=5)

        # Panel
        panel = tk.Frame(self.window, bg="white", bd=5, relief="ridge")
        panel.pack(pady=20, padx=40, fill="both", expand=True)

        # Estilos botones
        btn_style = {
            "font": ("Arial", 14, "bold"),
            "bg": "#E8E8E8",
            "fg": "#000",
            "width": 28,
            "height": 2,
            "bd": 2,
            "relief": "raised",
            "cursor": "hand2"
        }

        # Botones
        tk.Button(
            panel, text=" Mantenimiento de Clientes", command=self.abrir_clientes, **btn_style
        ).pack(pady=15)

        tk.Button(
            panel, text=" Mantenimiento de Categorías", command=self.abrir_categorias, **btn_style
        ).pack(pady=15)

        tk.Button(
            panel, text=" Mantenimiento de Productos", command=self.abrir_productos, **btn_style
        ).pack(pady=15)

        # Volver
        tk.Button(
            self.window,
            text="Volver",
            font=("Arial", 13, "bold"),
            bg="#E8E8E8",
            fg="black",
            width=15,
            cursor="hand2",
            command=self.volver
        ).pack(pady=15)

    def abrir_clientes(self):

        MantenimientoCliente(self.window)

    def abrir_categorias(self):
        MantenimientoCategoria(self.window)

    def abrir_productos(self):
        MantenimientoProducto(self.window)

    def volver(self):
        self.window.destroy()
        self.ventana_padre.deiconify()