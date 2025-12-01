import tkinter as tk
from tkinter import ttk, messagebox
from src.controladores.controlador_pedidos import ControladorPedidos

class BusquedaPedidosView:
    def __init__(self, usuario, modo_presentacion=False):
        self.usuario = usuario
        self.controlador = ControladorPedidos()
        self.modo_presentacion = modo_presentacion
        
        # Si es modo presentación, crear Toplevel en lugar de Tk
        if modo_presentacion:
            self.window = tk.Toplevel()
        else:
            self.window = tk.Tk()
        
        self.window.title("Búsqueda de Pedidos - Librería UTP")
        self.window.geometry("900x650")
        self.window.configure(bg="#728EFF")

        # Header
        frame_header = tk.Frame(self.window, bg="#FFFFFF", height=80)
        frame_header.pack(fill="x", padx=15, pady=15)
        frame_header.pack_propagate(False)

        lbl_icon = tk.Label(frame_header, text="🔍", font=("Arial", 24), bg="#FFFFFF")
        lbl_icon.pack(side="left", padx=20)

        lbl_titulo = tk.Label(
            frame_header,
            text="Búsqueda de Pedidos",
            font=("Arial", 20, "bold"),
            bg="#FFFFFF",
            fg="#000000"
        )
        lbl_titulo.pack(side="left")

        # Frame principal
        frame_principal = tk.Frame(self.window, bg="#728EFF")
        frame_principal.pack(fill="both", expand=True, padx=15, pady=10)

        # ===== CRITERIOS DE BÚSQUEDA =====
        frame_busqueda = tk.Frame(frame_principal, bg="#FFFFFF", relief="solid", bd=2)
        frame_busqueda.pack(fill="x", pady=10)

        lbl_busq_titulo = tk.Label(
            frame_busqueda,
            text="CRITERIOS DE BÚSQUEDA",
            font=("Arial", 12, "bold"),
            bg="#5A7FFF",
            fg="#FFFFFF",
            pady=5
        )
        lbl_busq_titulo.pack(fill="x")

        frame_busq_content = tk.Frame(frame_busqueda, bg="#FFFFFF", padx=15, pady=15)
        frame_busq_content.pack(fill="x")

        # Radio buttons para seleccionar criterio
        self.criterio_var = tk.StringVar(value="nombre")

        frame_radios = tk.Frame(frame_busq_content, bg="#FFFFFF")
        frame_radios.pack(fill="x", pady=5)

        tk.Radiobutton(
            frame_radios,
            text="Por Nombre del Cliente",
            variable=self.criterio_var,
            value="nombre",
            font=("Arial", 10),
            bg="#FFFFFF",
            command=self.cambiar_criterio
        ).pack(side="left", padx=10)

        tk.Radiobutton(
            frame_radios,
            text="Por Apellido del Cliente",
            variable=self.criterio_var,
            value="apellido",
            font=("Arial", 10),
            bg="#FFFFFF",
            command=self.cambiar_criterio
        ).pack(side="left", padx=10)

        tk.Radiobutton(
            frame_radios,
            text="Por Rango de Fechas",
            variable=self.criterio_var,
            value="rango_fechas",
            font=("Arial", 10),
            bg="#FFFFFF",
            command=self.cambiar_criterio
        ).pack(side="left", padx=10)

        # Frame para búsqueda por texto
        self.frame_texto = tk.Frame(frame_busq_content, bg="#FFFFFF")
        self.frame_texto.pack(fill="x", pady=10)

        tk.Label(self.frame_texto, text="Buscar:", font=("Arial", 10, "bold"), bg="#FFFFFF").pack(side="left")
        self.txt_buscar = tk.Entry(self.frame_texto, font=("Arial", 10), bg="#B3D9FF", width=30)
        self.txt_buscar.pack(side="left", padx=10)

        btn_buscar = tk.Button(
            self.frame_texto,
            text="Buscar",
            font=("Arial", 10, "bold"),
            bg="#4CAF50",
            fg="#FFFFFF",
            command=self.buscar_pedidos
        )
        btn_buscar.pack(side="left", padx=5)

        # Frame para búsqueda por rango de fechas
        self.frame_fechas = tk.Frame(frame_busq_content, bg="#FFFFFF")

        row_desde = tk.Frame(self.frame_fechas, bg="#FFFFFF")
        row_desde.pack(fill="x", pady=5)

        tk.Label(row_desde, text="Desde:", font=("Arial", 10, "bold"), bg="#FFFFFF").pack(side="left")
        self.txt_fecha_desde = tk.Entry(row_desde, font=("Arial", 10), bg="#B3D9FF", width=15)
        self.txt_fecha_desde.pack(side="left", padx=10)
        tk.Label(row_desde, text="(YYYY-MM-DD)", font=("Arial", 9, "italic"), bg="#FFFFFF", fg="#666").pack(side="left")

        row_hasta = tk.Frame(self.frame_fechas, bg="#FFFFFF")
        row_hasta.pack(fill="x", pady=5)

        tk.Label(row_hasta, text="Hasta:", font=("Arial", 10, "bold"), bg="#FFFFFF").pack(side="left", padx=(0,8))
        self.txt_fecha_hasta = tk.Entry(row_hasta, font=("Arial", 10), bg="#B3D9FF", width=15)
        self.txt_fecha_hasta.pack(side="left", padx=10)
        tk.Label(row_hasta, text="(YYYY-MM-DD)", font=("Arial", 9, "italic"), bg="#FFFFFF", fg="#666").pack(side="left")

        btn_buscar_fechas = tk.Button(
            self.frame_fechas,
            text="Buscar",
            font=("Arial", 10, "bold"),
            bg="#4CAF50",
            fg="#FFFFFF",
            command=self.buscar_pedidos
        )
        btn_buscar_fechas.pack(pady=10)

        # ===== LISTA DE PEDIDOS =====
        frame_lista = tk.Frame(frame_principal, bg="#FFFFFF", relief="solid", bd=2)
        frame_lista.pack(fill="both", expand=True, pady=10)

        lbl_lista_titulo = tk.Label(
            frame_lista,
            text="RESULTADOS DE BÚSQUEDA",
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
            columns=("numero", "fecha", "cliente", "estado", "total"),
            show="headings",
            height=10
        )
        self.tree_pedidos.heading("numero", text="N° Pedido")
        self.tree_pedidos.heading("fecha", text="Fecha")
        self.tree_pedidos.heading("cliente", text="Cliente")
        self.tree_pedidos.heading("estado", text="Estado")
        self.tree_pedidos.heading("total", text="Total")

        self.tree_pedidos.column("numero", width=150)
        self.tree_pedidos.column("fecha", width=120)
        self.tree_pedidos.column("cliente", width=250)
        self.tree_pedidos.column("estado", width=100)
        self.tree_pedidos.column("total", width=100)

        self.tree_pedidos.pack(side="left", fill="both", expand=True)

        scroll_tree = ttk.Scrollbar(frame_tree, orient="vertical", command=self.tree_pedidos.yview)
        scroll_tree.pack(side="right", fill="y")
        self.tree_pedidos.configure(yscrollcommand=scroll_tree.set)

        self.tree_pedidos.bind("<<TreeviewSelect>>", self.ver_detalle_pedido)

        # ===== DETALLE DEL PEDIDO =====
        frame_detalle = tk.Frame(frame_principal, bg="#FFFFFF", relief="solid", bd=2)
        frame_detalle.pack(fill="x", pady=10)

        lbl_det_titulo = tk.Label(
            frame_detalle,
            text="DETALLE DEL PEDIDO SELECCIONADO",
            font=("Arial", 12, "bold"),
            bg="#5A7FFF",
            fg="#FFFFFF",
            pady=5
        )
        lbl_det_titulo.pack(fill="x")

        frame_det_content = tk.Frame(frame_detalle, bg="#FFFFFF", padx=10, pady=10)
        frame_det_content.pack(fill="both", expand=True)

        self.txt_detalle = tk.Text(
            frame_det_content,
            font=("Arial", 10),
            bg="#F5F5F5",
            height=6,
            state="disabled"
        )
        self.txt_detalle.pack(fill="both", expand=True)

        # ===== BOTONES =====
        frame_botones = tk.Frame(frame_principal, bg="#728EFF")
        frame_botones.pack(pady=15)

        btn_volver = tk.Button(
            frame_botones,
            text="Volver",
            font=("Arial", 12, "bold"),
            bg="#FF5722",
            fg="#FFFFFF",
            width=15,
            command=self.volver
        )
        btn_volver.pack()

        # Solo ejecutar mainloop si NO es modo presentación
        if not modo_presentacion:
            self.window.mainloop()

    def cambiar_criterio(self):
        criterio = self.criterio_var.get()
        if criterio == "rango_fechas":
            self.frame_texto.pack_forget()
            self.frame_fechas.pack(fill="x", pady=10)
        else:
            self.frame_fechas.pack_forget()
            self.frame_texto.pack(fill="x", pady=10)

    def buscar_pedidos(self):
        criterio = self.criterio_var.get()
        
        if criterio == "nombre":
            valor = self.txt_buscar.get().strip()
            if not valor:
                messagebox.showwarning("Advertencia", "Ingrese el nombre a buscar")
                return
            pedidos = self.controlador.buscar_pedidos_por_cliente("nombre", valor)
            
        elif criterio == "apellido":
            valor = self.txt_buscar.get().strip()
            if not valor:
                messagebox.showwarning("Advertencia", "Ingrese el apellido a buscar")
                return
            pedidos = self.controlador.buscar_pedidos_por_cliente("apellido", valor)
            
        elif criterio == "rango_fechas":
            fecha_desde = self.txt_fecha_desde.get().strip()
            fecha_hasta = self.txt_fecha_hasta.get().strip()
            if not fecha_desde or not fecha_hasta:
                messagebox.showwarning("Advertencia", "Ingrese ambas fechas")
                return
            pedidos = self.controlador.buscar_pedidos_por_cliente("rango_fechas", (fecha_desde, fecha_hasta))

        # Limpiar tabla
        for item in self.tree_pedidos.get_children():
            self.tree_pedidos.delete(item)

        if not pedidos:
            messagebox.showinfo("Información", "No se encontraron pedidos con los criterios especificados")
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

    def ver_detalle_pedido(self, event):
        seleccion = self.tree_pedidos.selection()
        if not seleccion:
            return

        item = self.tree_pedidos.item(seleccion[0])
        idpedido = item['tags'][0]
        
        detalles = self.controlador.obtener_detalle_pedido(idpedido)
        
        self.txt_detalle.config(state="normal")
        self.txt_detalle.delete("1.0", tk.END)
        
        texto = f"Pedido N°: {item['values'][0]}\n"
        texto += f"Cliente: {item['values'][2]}\n"
        texto += f"Estado: {item['values'][3]}\n"
        texto += f"Total: {item['values'][4]}\n\n"
        texto += "Productos:\n"
        texto += "-" * 60 + "\n"
        
        for detalle in detalles:
            texto += f"• {detalle['nombre']} (Serie: {detalle['numero_serie']})\n"
            texto += f"  Cantidad: {detalle['cantidad']} x S/ {detalle['precio_unit']:.2f} = S/ {detalle['subtotal']:.2f}\n"
        
        self.txt_detalle.insert("1.0", texto)
        self.txt_detalle.config(state="disabled")

    def volver(self):
        self.window.destroy()
        # Solo abrir nueva ventana si NO es modo presentación
        if not self.modo_presentacion:
            from src.vistas.vista_empleado import VistaEmpleado
            VistaEmpleado(self.usuario)