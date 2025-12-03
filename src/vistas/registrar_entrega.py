
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from src.controladores.controlador_pedidos import ControladorPedidos

class RegistrarEntregaView:
    def __init__(self, usuario, modo_presentacion=False):
        self.usuario = usuario
        self.controlador = ControladorPedidos()
        self.pedido_seleccionado = None
        self.modo_presentacion = modo_presentacion
        
        # Si es modo presentación, crear Toplevel en lugar de Tk
        if modo_presentacion:
            self.window = tk.Toplevel()
        else:
            self.window = tk.Tk()
        
        self.window.title("Registrar Entrega - Librería UTP")
        self.window.geometry("800x600")
        self.window.configure(bg="#728EFF")

        # Header
        frame_header = tk.Frame(self.window, bg="#FFFFFF", height=80)
        frame_header.pack(fill="x", padx=15, pady=15)
        frame_header.pack_propagate(False)

        lbl_icon = tk.Label(frame_header, text="📦", font=("Arial", 24), bg="#FFFFFF")
        lbl_icon.pack(side="left", padx=20)

        lbl_titulo = tk.Label(
            frame_header,
            text="Registrar Entrega de Pedido",
            font=("Arial", 20, "bold"),
            bg="#FFFFFF",
            fg="#000000"
        )
        lbl_titulo.pack(side="left")

        # Frame principal
        frame_principal = tk.Frame(self.window, bg="#728EFF")
        frame_principal.pack(fill="both", expand=True, padx=15, pady=10)

        # ===== OPCIONES DE BÚSQUEDA =====
        frame_busqueda = tk.Frame(frame_principal, bg="#FFFFFF", relief="solid", bd=2)
        frame_busqueda.pack(fill="x", pady=10)

        lbl_busq_titulo = tk.Label(
            frame_busqueda,
            text="BUSCAR PEDIDO",
            font=("Arial", 12, "bold"),
            bg="#5A7FFF",
            fg="#FFFFFF",
            pady=5
        )
        lbl_busq_titulo.pack(fill="x")

        frame_busq_content = tk.Frame(frame_busqueda, bg="#FFFFFF", padx=15, pady=15)
        frame_busq_content.pack(fill="x")

        # Opción 1: Buscar por DNI Cliente
        frame_opcion1 = tk.LabelFrame(
            frame_busq_content,
            text="Opción 1: Buscar por DNI del Cliente",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            fg="#000000"
        )
        frame_opcion1.pack(fill="x", pady=10)

        row_cliente = tk.Frame(frame_opcion1, bg="#FFFFFF", padx=10, pady=10)
        row_cliente.pack(fill="x")

        tk.Label(row_cliente, text="DNI Cliente:", font=("Arial", 10), bg="#FFFFFF").pack(side="left")
        self.txt_dni_cliente = tk.Entry(row_cliente, font=("Arial", 10), bg="#B3D9FF", width=15)
        self.txt_dni_cliente.pack(side="left", padx=10)

        btn_buscar_cliente = tk.Button(
            row_cliente,
            text="Buscar Pedidos",
            font=("Arial", 10, "bold"),
            bg="#4CAF50",
            fg="#FFFFFF",
            command=self.buscar_por_cliente
        )
        btn_buscar_cliente.pack(side="left", padx=5)

        # Opción 2: Buscar por DNI Delivery
        frame_opcion2 = tk.LabelFrame(
            frame_busq_content,
            text="Opción 2: Buscar por DNI del Personal Delivery",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            fg="#000000"
        )
        frame_opcion2.pack(fill="x", pady=10)

        row_delivery = tk.Frame(frame_opcion2, bg="#FFFFFF", padx=10, pady=10)
        row_delivery.pack(fill="x")

        tk.Label(row_delivery, text="DNI Delivery:", font=("Arial", 10), bg="#FFFFFF").pack(side="left")
        self.txt_dni_delivery = tk.Entry(row_delivery, font=("Arial", 10), bg="#B3D9FF", width=15)
        self.txt_dni_delivery.pack(side="left", padx=10)

        btn_buscar_delivery = tk.Button(
            row_delivery,
            text="Buscar Pedidos",
            font=("Arial", 10, "bold"),
            bg="#4CAF50",
            fg="#FFFFFF",
            command=self.buscar_por_delivery
        )
        btn_buscar_delivery.pack(side="left", padx=5)

        # ===== LISTA DE PEDIDOS =====
        frame_lista = tk.Frame(frame_principal, bg="#FFFFFF", relief="solid", bd=2)
        frame_lista.pack(fill="both", expand=True, pady=10)

        lbl_lista_titulo = tk.Label(
            frame_lista,
            text="PEDIDOS ENCONTRADOS",
            font=("Arial", 12, "bold"),
            bg="#5A7FFF",
            fg="#FFFFFF",
            pady=5
        )
        lbl_lista_titulo.pack(fill="x")

        frame_tree = tk.Frame(frame_lista, bg="#FFFFFF", padx=10, pady=10)
        frame_tree.pack(fill="both", expand=True)

        self.tree_pedidos = ttk.Treeview(
            frame_tree,
            columns=("numero", "fecha_pedido", "cliente", "estado", "total"),
            show="headings",
            height=8
        )
        self.tree_pedidos.heading("numero", text="N° Pedido")
        self.tree_pedidos.heading("fecha_pedido", text="Fecha Pedido")
        self.tree_pedidos.heading("cliente", text="Cliente")
        self.tree_pedidos.heading("estado", text="Estado")
        self.tree_pedidos.heading("total", text="Total")

        self.tree_pedidos.column("numero", width=150)
        self.tree_pedidos.column("fecha_pedido", width=120)
        self.tree_pedidos.column("cliente", width=200)
        self.tree_pedidos.column("estado", width=100)
        self.tree_pedidos.column("total", width=100)

        self.tree_pedidos.pack(side="left", fill="both", expand=True)

        scroll_tree = ttk.Scrollbar(frame_tree, orient="vertical", command=self.tree_pedidos.yview)
        scroll_tree.pack(side="right", fill="y")
        self.tree_pedidos.configure(yscrollcommand=scroll_tree.set)

        self.tree_pedidos.bind("<<TreeviewSelect>>", self.seleccionar_pedido)

        # ===== DATOS DE ENTREGA =====
        frame_entrega = tk.Frame(frame_principal, bg="#FFFFFF", relief="solid", bd=2)
        frame_entrega.pack(fill="x", pady=10)

        lbl_ent_titulo = tk.Label(
            frame_entrega,
            text="DATOS DE ENTREGA",
            font=("Arial", 12, "bold"),
            bg="#5A7FFF",
            fg="#FFFFFF",
            pady=5
        )
        lbl_ent_titulo.pack(fill="x")

        frame_ent_content = tk.Frame(frame_entrega, bg="#FFFFFF", padx=15, pady=15)
        frame_ent_content.pack(fill="x")

        row_fecha = tk.Frame(frame_ent_content, bg="#FFFFFF")
        row_fecha.pack(fill="x", pady=5)

        tk.Label(row_fecha, text="Fecha de Entrega:", font=("Arial", 10, "bold"), bg="#FFFFFF").pack(side="left")
        self.txt_fecha_entrega = tk.Entry(row_fecha, font=("Arial", 10), bg="#B3D9FF", width=20)
        self.txt_fecha_entrega.pack(side="left", padx=10)
        self.txt_fecha_entrega.insert(0, datetime.now().strftime("%Y-%m-%d"))

        row_obs = tk.Frame(frame_ent_content, bg="#FFFFFF")
        row_obs.pack(fill="x", pady=5)

        tk.Label(row_obs, text="Observaciones:", font=("Arial", 10, "bold"), bg="#FFFFFF").pack(anchor="w")
        self.txt_observaciones = tk.Text(row_obs, font=("Arial", 10), bg="#B3D9FF", height=3)
        self.txt_observaciones.pack(fill="x", pady=5)

        # ===== BOTONES =====
        frame_botones = tk.Frame(frame_principal, bg="#728EFF")
        frame_botones.pack(pady=15)

        btn_registrar = tk.Button(
            frame_botones,
            text="✓ Registrar Entrega",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="#FFFFFF",
            width=18,
            command=self.registrar_entrega
        )
        btn_registrar.pack(side="left", padx=10)

        btn_volver = tk.Button(
            frame_botones,
            text="Volver",
            font=("Arial", 12, "bold"),
            bg="#FF5722",
            fg="#FFFFFF",
            width=15,
            command=self.volver
        )
        btn_volver.pack(side="left", padx=10)

        # Solo ejecutar mainloop si NO es modo presentación
        if not modo_presentacion:
            self.window.mainloop()

    def buscar_por_cliente(self):
        dni = self.txt_dni_cliente.get().strip()
        if not dni:
            messagebox.showwarning("Advertencia", "Ingrese el DNI del cliente")
            return

        pedidos = self.controlador.obtener_pedidos_pendientes_por_cliente(dni)
        self.mostrar_pedidos(pedidos)

    def buscar_por_delivery(self):
        dni = self.txt_dni_delivery.get().strip()
        if not dni:
            messagebox.showwarning("Advertencia", "Ingrese el DNI del delivery")
            return

        pedidos = self.controlador.obtener_pedidos_por_delivery(dni)
        self.mostrar_pedidos(pedidos)

    def mostrar_pedidos(self, pedidos):
        # Limpiar tabla
        for item in self.tree_pedidos.get_children():
            self.tree_pedidos.delete(item)

        if not pedidos:
            messagebox.showinfo("Información", "No se encontraron pedidos pendientes")
            return

        for pedido in pedidos:
            self.tree_pedidos.insert(
                "",
                "end",
                values=(
                    pedido['numero_pedido'],
                    pedido['fecha_pedido'],
                    f"{pedido['nombres']} {pedido['apellidos']}",
                    pedido['estado'],
                    f"S/ {pedido['total']:.2f}"
                ),
                tags=(pedido['idpedido'],)
            )

    def seleccionar_pedido(self, event):
        seleccion = self.tree_pedidos.selection()
        if seleccion:
            item = self.tree_pedidos.item(seleccion[0])
            idpedido = item['tags'][0]
            self.pedido_seleccionado = idpedido

    def registrar_entrega(self):
        if not self.pedido_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un pedido de la lista")
            return

        fecha_entrega = self.txt_fecha_entrega.get().strip()
        if not fecha_entrega:
            messagebox.showwarning("Advertencia", "Ingrese la fecha de entrega")
            return

        observaciones = self.txt_observaciones.get("1.0", tk.END).strip()

        resultado = self.controlador.registrar_entrega(
            self.pedido_seleccionado,
            fecha_entrega,
            observaciones
        )

        if resultado:
            messagebox.showinfo("Éxito", "Entrega registrada correctamente")
            # Limpiar campos
            self.txt_dni_cliente.delete(0, tk.END)
            self.txt_dni_delivery.delete(0, tk.END)
            self.txt_observaciones.delete("1.0", tk.END)
            for item in self.tree_pedidos.get_children():
                self.tree_pedidos.delete(item)
            self.pedido_seleccionado = None
        else:
            messagebox.showerror("Error", "No se pudo registrar la entrega")

    def volver(self):
        self.window.destroy()
        # Solo abrir nueva ventana si NO es modo presentación
        if not self.modo_presentacion:
            from src.vistas.vista_empleado import VistaEmpleado
            VistaEmpleado(self.usuario)