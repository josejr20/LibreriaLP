import tkinter as tk
from tkinter import messagebox
from src.vistas.registrar_entrega import RegistrarEntregaView
from src.vistas.registrar_pedido import RegistrarPedidoView
from src.vistas.busqueda_pedidos import BusquedaPedidosView

class VistaEmpleado:
    def __init__(self, usuario):
        self.usuario = usuario
        self.window = tk.Tk()
        self.window.title("Panel Empleado - Librería UTP")
        self.window.geometry("600x420")  # <--- MAS ALTURA PARA QUE TODO ENTRE
        self.window.configure(bg="#728EFF")

        # ============================
        # ENCABEZADO
        # ============================
        frame_header = tk.Frame(self.window, bg="#FFFFFF")
        frame_header.pack(fill="x", padx=20, pady=(20, 10))

        lbl_titulo = tk.Label(
            frame_header,
            text="PANEL DEL EMPLEADO",
            font=("Arial", 20, "bold"),
            bg="#FFFFFF",
            fg="#000000",
            height=2
        )
        lbl_titulo.pack(fill="x")

        # ============================
        # CUADRO BLANCO CENTRADO
        # ============================
        frame_menu = tk.Frame(self.window, bg="#FFFFFF", width=350, height=240)
        frame_menu.pack(pady=5)
        frame_menu.pack_propagate(False)  # <--- NECESARIO PARA QUE NO SE EXPANDA

        estilo_btn = {
            "font": ("Arial", 12, "bold"),
            "bg": "#83B3FF",
            "fg": "#000000",
            "activebackground": "#B3D9FF",
            "relief": "flat",
            "width": 25,
            "height": 2
        }

        tk.Button(
            frame_menu,
            text="🛒 Registrar Pedido",
            command=self.abrir_registrar_pedido,
            **estilo_btn
        ).pack(pady=8)

        tk.Button(
            frame_menu,
            text="📦 Registrar Entrega",
            command=self.abrir_registrar_entrega,
            **estilo_btn
        ).pack(pady=8)

        tk.Button(
            frame_menu,
            text="🔍 Búsqueda de Pedidos",
            command=self.abrir_busqueda_pedidos,
            **estilo_btn
        ).pack(pady=8)

        # ============================
        # BOTÓN DE CERRAR SESIÓN (FUERA)
        # ============================
        btn_cerrar = tk.Button(
            self.window,
            text="🚪 Cerrar Sesión",
            font=("Arial", 11, "bold"),
            bg="#FF6B6B",
            fg="#FFFFFF",
            activebackground="#FF5252",
            width=18,
            height=1,
            relief="flat",
            command=self.cerrar_sesion
        )
        btn_cerrar.pack(pady=15)   # <--- AHORA SIEMPRE VISIBLE

        self.window.mainloop()

    # ============================
    # FUNCIONES
    # ============================
    def abrir_registrar_pedido(self):
        RegistrarPedidoView(self.usuario, modo_presentacion=True)

    def abrir_registrar_entrega(self):
        RegistrarEntregaView(self.usuario, modo_presentacion=True)

    def abrir_busqueda_pedidos(self):
        BusquedaPedidosView(self.usuario, modo_presentacion=True)

    def cerrar_sesion(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro que desea cerrar sesión?"):
            self.window.destroy()
            from src.vistas.login import LoginView
            LoginView()