import tkinter as tk
from tkinter import ttk, messagebox
from src.controladores.controlador_pedidos import ControladorPedidos

class BusquedaPedidosView:
    def __init__(self, usuario, modo_presentacion=False):
        self.usuario = usuario
        self.controlador = ControladorPedidos()
        self.modo_presentacion = modo_presentacion
        
        if modo_presentacion:
            self.window = tk.Toplevel()
        else:
            self.window = tk.Tk()
        
        self.window.title("Búsqueda de Pedidos - Librería UTP")
        self.window.geometry("900x650")
        self.window.minsize(750, 550)
        self.window.resizable(True, True)
        self.window.configure(bg="#f0f0f0")

        frame_header = tk.Frame(self.window, bg="#4A63D8", height=70)
        frame_header.pack(fill="x", padx=0, pady=0)
        frame_header.pack_propagate(False)

        lbl_icon = tk.Label(frame_header, text="🔍", font=("Arial", 24), bg="#4A63D8")
        lbl_icon.pack(side="left", padx=20, pady=8)

        lbl_titulo = tk.Label(
            frame_header,
            text="Búsqueda de Pedidos",
            font=("Arial", 18, "bold"),
            bg="#4A63D8",
            fg="#FFFFFF"
        )
        lbl_titulo.pack(side="left")

        frame_principal = tk.Frame(self.window, bg="#f0f0f0")
        frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

        frame_busqueda = tk.Frame(frame_principal, bg="#FFFFFF", relief="solid", bd=1)
        frame_busqueda.pack(fill="x", pady=(0, 15))

        lbl_busq_titulo = tk.Label(
            frame_busqueda,
            text="CRITERIOS DE BÚSQUEDA",
            font=("Arial", 13, "bold"),
            bg="#4A63D8",
            fg="#FFFFFF",
            pady=10
        )
        lbl_busq_titulo.pack(fill="x")

        frame_busq_content = tk.Frame(frame_busqueda, bg="#FFFFFF", padx=20, pady=15)
        frame_busq_content.pack(fill="both", expand=True)

        self.criterio_var = tk.StringVar(value="nombre")

        frame_radios = tk.Frame(frame_busq_content, bg="#FFFFFF")
        frame_radios.pack(fill="x", pady=(0, 15))

        tk.Radiobutton(
            frame_radios,
            text="Por Nombre del Cliente",
            variable=self.criterio_var,
            value="nombre",
            font=("Arial", 11),
            bg="#FFFFFF",
            activebackground="#f0f0f0",
            command=self.cambiar_criterio
        ).pack(side="left", padx=10)

        tk.Radiobutton(
            frame_radios,
            text="Por Apellido del Cliente",
            variable=self.criterio_var,
            value="apellido",
            font=("Arial", 11),
            bg="#FFFFFF",
            activebackground="#f0f0f0",
            command=self.cambiar_criterio
        ).pack(side="left", padx=10)

        tk.Radiobutton(
            frame_radios,
            text="Por Rango de Fechas",
            variable=self.criterio_var,
            value="rango_fechas",
            font=("Arial", 11),
            bg="#FFFFFF",
            activebackground="#f0f0f0",
            command=self.cambiar_criterio
        ).pack(side="left", padx=10)

        self.frame_texto = tk.Frame(frame_busq_content, bg="#FFFFFF")
        self.frame_texto.pack(fill="x", pady=10)

        tk.Label(self.frame_texto, text="Buscar:", font=("Arial", 11, "bold"), bg="#FFFFFF").pack(side="left", padx=(0, 10))
        self.txt_buscar = tk.Entry(self.frame_texto, font=("Arial", 11), bg="#E8F4F8", width=30, relief="solid", bd=1)
        self.txt_buscar.pack(side="left", padx=5)

        btn_buscar = tk.Button(
            self.frame_texto,
            text="🔍 Buscar",
            font=("Arial", 11, "bold"),
            bg="#26A65B",
            fg="#FFFFFF",
            padx=20,
            pady=5,
            cursor="hand2",
            relief="solid",
            bd=1,
            command=self.buscar_pedidos
        )
        btn_buscar.pack(side="left", padx=5)

        self.frame_fechas = tk.Frame(frame_busq_content, bg="#FFFFFF")

        row_desde = tk.Frame(self.frame_fechas, bg="#FFFFFF")
        row_desde.pack(fill="x", pady=5)

        tk.Label(row_desde, text="Desde:", font=("Arial", 11, "bold"), bg="#FFFFFF").pack(side="left", padx=(0, 10))
        self.txt_fecha_desde = tk.Entry(row_desde, font=("Arial", 11), bg="#E8F4F8", width=15, relief="solid", bd=1)
        self.txt_fecha_desde.pack(side="left", padx=5)
        tk.Label(row_desde, text="(YYYY-MM-DD)", font=("Arial", 9, "italic"), bg="#FFFFFF", fg="#666").pack(side="left", padx=5)

        row_hasta = tk.Frame(self.frame_fechas, bg="#FFFFFF")
        row_hasta.pack(fill="x", pady=5)

        tk.Label(row_hasta, text="Hasta:", font=("Arial", 11, "bold"), bg="#FFFFFF").pack(side="left", padx=(0, 10))
        self.txt_fecha_hasta = tk.Entry(row_hasta, font=("Arial", 11), bg="#E8F4F8", width=15, relief="solid", bd=1)
        self.txt_fecha_hasta.pack(side="left", padx=5)
        tk.Label(row_hasta, text="(YYYY-MM-DD)", font=("Arial", 9, "italic"), bg="#FFFFFF", fg="#666").pack(side="left", padx=5)

        btn_buscar_fechas = tk.Button(
            self.frame_fechas,
            text="🔍 Buscar",
            font=("Arial", 11, "bold"),
            bg="#26A65B",
            fg="#FFFFFF",
            padx=20,
            pady=5,
            cursor="hand2",
            relief="solid",
            bd=1,
            command=self.buscar_pedidos
        )
        btn_buscar_fechas.pack(pady=10)

        frame_contenedor = tk.Frame(frame_principal, bg="#f0f0f0")
        frame_contenedor.pack(fill="both", expand=True, pady=(0, 15))

        frame_lista = tk.Frame(frame_contenedor, bg="#FFFFFF", relief="solid", bd=1)
        frame_lista.pack(side="left", fill="both", expand=True, padx=(0, 10))

        lbl_lista_titulo = tk.Label(
            frame_lista,
            text="RESULTADOS DE BÚSQUEDA",
            font=("Arial", 13, "bold"),
            bg="#4A63D8",
            fg="#FFFFFF",
            pady=10
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

        self.tree_pedidos.column("numero", width=105)
        self.tree_pedidos.column("fecha", width=74)
        self.tree_pedidos.column("cliente", width=100)
        self.tree_pedidos.column("estado", width=70)
        self.tree_pedidos.column("total", width=70)

        self.tree_pedidos.pack(side="left", fill="both", expand=True)

        scroll_tree = ttk.Scrollbar(frame_tree, orient="vertical", command=self.tree_pedidos.yview)
        scroll_tree.pack(side="right", fill="y")
        self.tree_pedidos.configure(yscrollcommand=scroll_tree.set)

        self.tree_pedidos.bind("<<TreeviewSelect>>", self.ver_detalle_pedido)

        frame_detalle = tk.Frame(frame_contenedor, bg="#FFFFFF", relief="solid", bd=1)
        frame_detalle.pack(side="right", fill="y", padx=(10, 0))
        frame_detalle.config(width=260)

        lbl_det_titulo = tk.Label(
            frame_detalle,
            text="DETALLE DEL PEDIDO",
            font=("Arial", 13, "bold"),
            bg="#4A63D8",
            fg="#FFFFFF",
            pady=10
        )
        lbl_det_titulo.pack(fill="x")

        frame_det_content = tk.Frame(frame_detalle, bg="#FFFFFF", padx=10, pady=10)
        frame_det_content.pack(fill="both", expand=True)

        self.txt_detalle = tk.Text(
            frame_det_content,
            font=("Courier", 10),
            bg="#F5F5F5",
            fg="#333333",
            state="disabled",
            relief="solid",
            bd=1,
            padx=10,
            pady=10
        )
        self.txt_detalle.pack(fill="both", expand=True)

        frame_botones = tk.Frame(frame_principal, bg="#f0f0f0")
        frame_botones.pack(pady=0)

        btn_volver = tk.Button(
            frame_botones,
            text="← Volver",
            font=("Arial", 12, "bold"),
            bg="#FF6B6B",
            fg="#FFFFFF",
            width=15,
            padx=20,
            pady=10,
            cursor="hand2",
            relief="solid",
            bd=1,
            command=self.volver
        )
        btn_volver.pack()

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
            self.txt_detalle.config(state="normal")
            self.txt_detalle.delete("1.0", tk.END)
            self.txt_detalle.config(state="disabled")
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
                tags=(str(pedido['idpedido']),)
            )

    def ver_detalle_pedido(self, event):
        seleccion = self.tree_pedidos.selection()
        if not seleccion:
            return

        try:
            item = self.tree_pedidos.item(seleccion[0])
            idpedido = int(item['tags'][0])
            
            detalles = self.controlador.obtener_detalle_pedido(idpedido)
            
            self.txt_detalle.config(state="normal")
            self.txt_detalle.delete("1.0", tk.END)
            
            # Crear formato como boleta
            texto = "DETALLE DE PEDIDO\n\n"
            texto += f"Pedido: {item['values'][0]}\n"
            texto += f"Cliente: {item['values'][2]}\n"
            texto += f"Estado: {item['values'][3]}\n"
            texto += f"Total: {item['values'][4]}\n\n"
            texto += "PRODUCTOS:\n"
            
            if detalles:
                for i, detalle in enumerate(detalles, 1):
                    precio_unit = float(detalle['precio_unit'])
                    subtotal = float(detalle['subtotal'])
                    texto += f"\n{i}. {detalle['nombre']}\n"
                    texto += f"   Serie: {detalle['numero_serie']}\n"
                    texto += f"   Cantidad: {detalle['cantidad']} x S/ {precio_unit:.2f}\n"
                    texto += f"   Subtotal: S/ {subtotal:.2f}\n"
            else:
                texto += "\nNo hay productos en este pedido.\n"
            
            
            self.txt_detalle.insert("1.0", texto)
            self.txt_detalle.config(state="disabled")
        except Exception as e:
            print(f"Error al obtener detalle del pedido: {e}")
            messagebox.showerror("Error", f"Error al obtener detalle: {str(e)}")

    def volver(self):
        self.window.destroy()
        # Solo abrir nueva ventana si NO es modo presentación
        if not self.modo_presentacion:
            from src.vistas.vista_empleado import VistaEmpleado
            VistaEmpleado(self.usuario)
