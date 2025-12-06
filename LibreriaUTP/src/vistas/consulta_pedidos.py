import tkinter as tk
from tkinter import ttk, messagebox
from src.controladores.controlador_delivery import DeliveryController
from src.controladores.controlador_consulta import ControladorConsultaDelivery


COLOR_FONDO = "#728EFF"  
COLOR_BOTON = "#4CAF50"       
COLOR_BOTON_SEC = "#D21919"      
COLOR_TEXTO_BOTON = "white"      


class ConsultaPedidosDeliveryView:

    def __init__(self, usuario):
        self.usuario = usuario
        self.delivery_controller = DeliveryController()
        self.pedido_controller = ControladorConsultaDelivery()

        self.ventana = tk.Toplevel()
        self.ventana.title("Consulta de Pedidos Entregados por Personal Delivery")
        self.ventana.geometry("900x600")
        self.ventana.configure(bg=COLOR_FONDO)

        self._estilos_treeview()
        self.build_ui()

    # ---------------------------------------------------------
    #   ESTILOS TREEVIEW
    # ---------------------------------------------------------
    def _estilos_treeview(self):
        style = ttk.Style()

        style.theme_use("default")

        # Headers
        style.configure("Treeview.Heading",
                        background="#D5D9DE",
                        foreground="black",
                        font=("Arial", 11, "bold"))

        # Filas
        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="white")

        style.map("Treeview", background=[("selected", "#A4C2F4")])

    def build_ui(self):

        tk.Label(self.ventana, text="Buscar Personal Delivery",
                font=("Arial", 14, "bold"),
                bg=COLOR_FONDO).pack(pady=10)

        # --- BUSQUEDA ---
        frame_busqueda = tk.Frame(self.ventana, bg=COLOR_FONDO)
        frame_busqueda.pack(pady=5)

        tk.Label(frame_busqueda, text="Nombres / Apellidos / DNI: ",
                bg=COLOR_FONDO).pack(side=tk.LEFT)

        self.txt_busqueda = tk.Entry(frame_busqueda, width=40)
        self.txt_busqueda.pack(side=tk.LEFT, padx=5)

        tk.Button(frame_busqueda, text="Buscar",
                bg=COLOR_BOTON, fg=COLOR_TEXTO_BOTON,
                activebackground="#45A049",
                width=12,
                command=self.buscar_delivery).pack(side=tk.LEFT)

        # --- TREE PERSONAL ---
        tk.Label(self.ventana, text="Resultados del Personal Delivery:",
                font=("Arial", 12, "bold"),
                bg=COLOR_FONDO).pack(pady=10)

        self.tree_delivery = ttk.Treeview(self.ventana, columns=(
            "id", "nombre", "apellido", "dni"), show="headings", height=6)

        self.tree_delivery.heading("id", text="ID")
        self.tree_delivery.heading("nombre", text="Nombre")
        self.tree_delivery.heading("apellido", text="Apellido")
        self.tree_delivery.heading("dni", text="DNI")

        self.tree_delivery.column("id", width=60)
        self.tree_delivery.column("nombre", width=200)
        self.tree_delivery.column("apellido", width=200)
        self.tree_delivery.column("dni", width=100)

        self.tree_delivery.pack(pady=5)

        tk.Button(self.ventana, text="Seleccionar Personal",
                bg=COLOR_BOTON_SEC, fg=COLOR_TEXTO_BOTON,
                activebackground="#125AA0",
                width=20,
                command=self.seleccionar_personal).pack(pady=10)

        # --- BOTONES VISTA ENT/PEND ---
        frame_botones = tk.Frame(self.ventana, bg=COLOR_FONDO)
        frame_botones.pack(pady=5)

        tk.Button(frame_botones, text="Ver Entregados",
                bg=COLOR_BOTON, fg=COLOR_TEXTO_BOTON,
                activebackground="#45A049",
                width=15,
                command=self.mostrar_entregados).pack(side=tk.LEFT, padx=10)

        tk.Button(frame_botones, text="Ver Pendientes",
                bg=COLOR_BOTON, fg=COLOR_TEXTO_BOTON,
                activebackground="#125AA0",
                width=15,
                command=self.mostrar_pendientes).pack(side=tk.LEFT, padx=10)

        # --- TREE PEDIDOS ---
        tk.Label(self.ventana, text="Pedidos Entregados:",
                font=("Arial", 12, "bold"),
                bg=COLOR_FONDO).pack(pady=10)

        self.tree_pedidos = ttk.Treeview(self.ventana, columns=(
            "numero", "ped", "ent", "total", "obs"),
            show="headings", height=10)

        self.tree_pedidos.heading("numero", text="N° Pedido")
        self.tree_pedidos.heading("ped", text="Fecha Pedido")
        self.tree_pedidos.heading("ent", text="Fecha Entrega")
        self.tree_pedidos.heading("total", text="Total")
        self.tree_pedidos.heading("obs", text="Observaciones")

        self.tree_pedidos.column("numero", width=100)
        self.tree_pedidos.column("ped", width=120)
        self.tree_pedidos.column("ent", width=120)
        self.tree_pedidos.column("total", width=80)
        self.tree_pedidos.column("obs", width=300)

        self.tree_pedidos.pack(pady=5)

    # -----------------------------------------------------
    #   SELECCION ENT/PEND
    # -----------------------------------------------------
    def mostrar_entregados(self):
        if not hasattr(self, "iddelivery_actual"):
            messagebox.showwarning("Advertencia", "Seleccione un personal primero.")
            return
        self.cargar_pedidos_entregados(self.iddelivery_actual)

    def mostrar_pendientes(self):
        if not hasattr(self, "iddelivery_actual"):
            messagebox.showwarning("Advertencia", "Seleccione un personal primero.")
            return
        self.cargar_pedidos_pendientes(self.iddelivery_actual)

    # -----------------------------------------------------
    #   BUSCAR PERSONAL DELIVERY
    # -----------------------------------------------------
    def buscar_delivery(self):
        parametro = self.txt_busqueda.get().strip()

        if not parametro:
            messagebox.showwarning("Advertencia",
                                "Ingrese un parámetro de búsqueda.")
            return

        resultados = self.delivery_controller.buscar_delivery(parametro)

        for fila in self.tree_delivery.get_children():
            self.tree_delivery.delete(fila)

        if not resultados:
            messagebox.showinfo("Sin resultados",
                                "No se encontró personal delivery.")
            return

        for d in resultados:
            self.tree_delivery.insert("", tk.END,
                                    values=(d["iddelivery"], d["nombres"], d["apellidos"], d["dni"]))

    # -----------------------------------------------------
    #   SELECCIONAR PERSONAL
    # -----------------------------------------------------
    def seleccionar_personal(self):
        item = self.tree_delivery.selection()
        if not item:
            messagebox.showwarning("Advertencia", "Seleccione un personal.")
            return

        datos = self.tree_delivery.item(item)["values"]
        iddelivery = datos[0]

        self.iddelivery_actual = iddelivery
        self.cargar_pedidos_entregados(iddelivery)

    # -----------------------------------------------------
    #   CARGAR PEDIDOS
    # -----------------------------------------------------
    def cargar_pedidos_entregados(self, iddelivery):
        pedidos = self.pedido_controller.obtener_pedidos_entregados_por_delivery(iddelivery)

        for fila in self.tree_pedidos.get_children():
            self.tree_pedidos.delete(fila)

        if not pedidos:
            messagebox.showinfo("Sin resultados",
                                "Este personal no tiene pedidos entregados.")
            return

        for p in pedidos:
            self.tree_pedidos.insert("", tk.END, values=(
                p["numero_pedido"],
                p["fecha_pedido"],
                p["fecha_entrega"],
                p["total"],
                p["observaciones"]
            ))

    def cargar_pedidos_pendientes(self, iddelivery):
        pedidos = self.pedido_controller.obtener_pedidos_pendientes_por_delivery(iddelivery)

        for fila in self.tree_pedidos.get_children():
            self.tree_pedidos.delete(fila)

        if not pedidos:
            messagebox.showinfo("Sin resultados",
                                "Este personal no tiene pedidos pendientes.")
            return

        for p in pedidos:
            self.tree_pedidos.insert("", tk.END, values=(
                p["numero_pedido"],
                p["fecha_pedido"],
                p["fecha_entrega"],
                p["total"],
                p["observaciones"]
            ))