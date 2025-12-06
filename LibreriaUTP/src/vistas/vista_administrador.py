import tkinter as tk
from tkinter import messagebox
from src.controladores.controlador_administrador import ControladorAdministrador
from src.vistas.consulta_pedidos import ConsultaPedidosDeliveryView
from src.vistas.registrar_pedido import RegistrarPedidoView
from src.vistas.busqueda_pedidos import BusquedaPedidosView
from src.vistas.registrar_entrega import RegistrarEntregaView


class VistaAdministrador:
    def __init__(self, usuario):
        self.usuario = usuario
        self.controlador = ControladorAdministrador(usuario)

        self.window = tk.Tk()
        self.window.title("Panel Administrador - Librería UTP")
        self.window.geometry("750x500")
        self.window.configure(bg="#728EFF")

        datos = self.controlador.obtener_datos()

        # ========= TÍTULO =========
        lbl_header = tk.Label(
            self.window,
            text="PANEL DEL ADMINISTRADOR",
            font=("Arial", 20, "bold"),
            bg="#FFFFFF",
            fg="#000000",
            width=30,
            height=2
        )
        lbl_header.pack(pady=20)

        # ========= CONTENEDOR CENTRAL =========
        frame_central = tk.Frame(
            self.window,
            bg="#FFFFFF",
            width=420,
            height=350,
            highlightbackground="#000000",
            highlightthickness=1
        )
        frame_central.pack(expand=True)
        frame_central.pack_propagate(False)  # Mantiene tamaño fijo

        # ========= ESTILO DE BOTONES =========
        def crear_boton(texto, comando):
            return tk.Button(
                frame_central,
                text=texto,
                font=("Arial", 12, "bold"),
                bg="#83B3FF",
                fg="#000000",
                activebackground="#5A8DEB",
                width=30,
                height=2,
                relief="flat",
                command=comando
            )

        # ========= BOTONES =========
        btn1 = crear_boton(
            "📦 Consulta de Pedidos por Delivery",
            self.abrir_consulta_pedidos_delivery
        )
        btn1.pack(pady=10)

        btn2 = crear_boton(
            "🛒 Registrar Pedido",
            self.abrir_registrar_pedido
        )
        btn2.pack(pady=10)

        btn3 = crear_boton(
            "📍 Registrar Entrega de Pedido",
            self.abrir_registrar_entrega
        )
        btn3.pack(pady=10)

        btn4 = crear_boton(
            "🔍 Búsqueda de Pedidos",
            self.abrir_busqueda_pedidos
        )
        btn4.pack(pady=10)

        btn_mantenimiento = crear_boton(
            "⚙️  Mantenimiento",
            self.abrir_mantenimiento
        )
        btn_mantenimiento.pack(pady=10)

        # ========= Cerrar Sesión =========
        btn_logout = tk.Button(
            self.window,
            text="Cerrar Sesión",
            font=("Arial", 11, "bold"),
            bg="#FF6B6B",
            fg="white",
            activebackground="#E85050",
            width=15,
            height=1,
            command=self.cerrar_sesion
        )
        btn_logout.pack(pady=10)

        self.window.mainloop()

    # ===============================
    #      FUNCIONES DE ACCESO
    # ===============================
    def abrir_consulta_pedidos_delivery(self):
        ConsultaPedidosDeliveryView(self.usuario)

    def abrir_mantenimiento(self):
        from src.vistas.mantenimiento import Mantenimiento
        self.window.withdraw()
        Mantenimiento(self.window, self.controlador.admin)

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