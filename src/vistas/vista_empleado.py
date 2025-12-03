import tkinter as tk
from tkinter import messagebox
from src.vistas.registrar_pedido import RegistrarPedidoView
from src.vistas.registrar_entrega import RegistrarEntregaView
from src.vistas.busqueda_pedidos import BusquedaPedidosView

class VistaEmpleado:
    def __init__(self, usuario):
        self.usuario = usuario
        self.window = tk.Tk()
        self.window.title("Panel Empleado - Librería UTP")
        self.window.geometry("400x320")
        self.window.configure(bg="#728EFF")

        frame_header = tk.Frame(self.window, bg="#FFFFFF", height=80)
        frame_header.pack(fill="x", padx=10, pady=10)
        frame_header.pack_propagate(False)

        lbl_icon = tk.Label(
            frame_header,
            text="👤",
            font=("Arial", 24),
            bg="#FFFFFF",
            fg="#000000"
        )
        lbl_icon.pack(side="left", padx=20)

        lbl_titulo = tk.Label(
            frame_header,
            text="Empleado",
            font=("Arial", 20, "bold"),
            bg="#FFFFFF",
            fg="#000000"
        )
        lbl_titulo.pack(side="left")

        frame_menu = tk.Frame(self.window, bg="#E8F0FF", width=110)
        frame_menu.pack(side="left", fill="y", padx=(10, 0), pady=(0, 10))

        btn_registrar_pedido = tk.Button(
            frame_menu,
            text="🛒 Registrar Pedido",
            font=("Arial", 11, "bold"),
            bg="#B3D9FF",
            fg="#000000",
            activebackground="#83B3FF",
            width=25,
            height=2,
            relief="flat",
            command=self.abrir_registrar_pedido
        )
        btn_registrar_pedido.pack(pady=10, padx=10)

        btn_registrar_entrega = tk.Button(
            frame_menu,
            text="⚫ Registrar Entrega de Pedido",
            font=("Arial", 11, "bold"),
            bg="#E8F0FF",
            fg="#000000",
            activebackground="#B3D9FF",
            width=25,
            height=2,
            relief="flat",
            command=self.abrir_registrar_entrega
        )
        btn_registrar_entrega.pack(pady=10, padx=10)

        btn_busqueda = tk.Button(
            frame_menu,
            text="🔍 Búsqueda de Pedidos",
            font=("Arial", 11, "bold"),
            bg="#E8F0FF",
            fg="#000000",
            activebackground="#B3D9FF",
            width=25,
            height=2,
            relief="flat",
            command=self.abrir_busqueda_pedidos
        )
        btn_busqueda.pack(pady=10, padx=10)

        self.frame_principal = tk.Frame(self.window, bg="#728EFF")
        self.frame_principal.pack(side="right", fill="both", expand=True, padx=10, pady=(0, 10))

        btn_cerrar = tk.Button(
            self.frame_principal,
            text="🚪 Cerrar Sesión",
            font=("Arial", 10, "bold"),
            bg="#FF6B6B",
            fg="#FFFFFF",
            activebackground="#FF5252",
            command=self.cerrar_sesion
        )
        btn_cerrar.pack(side="bottom", pady=10)

        self.window.mainloop()

    def abrir_registrar_pedido(self):
        RegistrarPedidoView(self.usuario, modo_presentacion=True)

    def abrir_registrar_entrega(self):
        RegistrarEntregaView(self.usuario, modo_presentacion=True)

    def abrir_busqueda_pedidos(self):
        BusquedaPedidosView(self.usuario, modo_presentacion=True)

    def cerrar_sesion(self):
        respuesta = messagebox.askyesno("Cerrar Sesión", "¿Está seguro que desea cerrar sesión?")
        if respuesta:
            self.window.destroy()
            from src.vistas.login import LoginView
            LoginView()