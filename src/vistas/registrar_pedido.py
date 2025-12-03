import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from src.controladores.controlador_pedidos import ControladorPedidos

class RegistrarPedidoView:
    def __init__(self, usuario, modo_presentacion=False):
        self.usuario = usuario
        self.controlador = ControladorPedidos()
        self.productos_seleccionados = []
        self.modo_presentacion = modo_presentacion
        
        # Si es modo presentación, crear Toplevel en lugar de Tk
        # crea una ventana hija en lugar de una nueva ventana principal
        if modo_presentacion:
            self.window = tk.Toplevel()
        else:
            self.window = tk.Tk()
        
        self.window.title("Registrar Pedido - Librería UTP")
        # Ventana redimensionable y con tamaño mínimo
        self.window.geometry("900x700")
        self.window.minsize(700, 600)
        self.window.resizable(True, True)
        self.window.configure(bg="#728EFF")

        frame_header = tk.Frame(self.window, bg="#FFFFFF", height=80)
        frame_header.pack(fill="x", padx=15, pady=15)
        frame_header.pack_propagate(False)

        lbl_icon = tk.Label(frame_header, text="🛒", font=("Arial", 24), bg="#FFFFFF")
        lbl_icon.pack(side="left", padx=20)

        lbl_titulo = tk.Label(
            frame_header,
            text="Registrar Pedido",
            font=("Arial", 20, "bold"),
            bg="#FFFFFF",
            fg="#000000"
        )
        lbl_titulo.pack(side="left")

        # Canvas con contenido scrollable responsive
        self.canvas = tk.Canvas(self.window, bg="#728EFF", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        frame_scrollable = tk.Frame(self.canvas, bg="#728EFF")

        self.canvas_window = self.canvas.create_window((0, 0), window=frame_scrollable, anchor="nw")

        frame_scrollable.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfigure(self.canvas_window, width=e.width)
        )

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True, padx=15)
        scrollbar.pack(side="right", fill="y")
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        frame_cabecera = tk.Frame(frame_scrollable, bg="#FFFFFF", relief="solid", bd=2)
        frame_cabecera.pack(fill="x", pady=10, padx=10)

        lbl_cab_titulo = tk.Label(
            frame_cabecera,
            text="DATOS DE CABECERA",
            font=("Arial", 12, "bold"),
            bg="#5A7FFF",
            fg="#FFFFFF",
            pady=5
        )
        lbl_cab_titulo.pack(fill="x")

        frame_cab_content = tk.Frame(frame_cabecera, bg="#FFFFFF", padx=10, pady=10)
        frame_cab_content.pack(fill="x")

        row1 = tk.Frame(frame_cab_content, bg="#FFFFFF")
        row1.pack(fill="x", pady=5)

        tk.Label(row1, text="Número Pedido:", font=("Arial", 10, "bold"), bg="#FFFFFF").pack(side="left")
        self.txt_num_pedido = tk.Entry(row1, font=("Arial", 10), bg="#B3D9FF", width=20)
        self.txt_num_pedido.pack(side="left", padx=10)
        self.txt_num_pedido.insert(0, self.generar_numero_pedido())

        tk.Label(row1, text="Fecha Pedido:", font=("Arial", 10, "bold"), bg="#FFFFFF").pack(side="left", padx=(20,0))
        self.txt_fecha_pedido = tk.Entry(row1, font=("Arial", 10), bg="#B3D9FF", width=15)
        self.txt_fecha_pedido.pack(side="left", padx=10)
        self.txt_fecha_pedido.insert(0, datetime.now().strftime("%Y-%m-%d"))

        row2 = tk.Frame(frame_cab_content, bg="#FFFFFF")
        row2.pack(fill="x", pady=5)

        tk.Label(row2, text="Fecha Entrega:", font=("Arial", 10, "bold"), bg="#FFFFFF").pack(side="left")
        self.txt_fecha_entrega = tk.Entry(row2, font=("Arial", 10), bg="#B3D9FF", width=20)
        self.txt_fecha_entrega.pack(side="left", padx=10)

        tk.Label(row2, text="Personal Delivery:", font=("Arial", 10, "bold"), bg="#FFFFFF").pack(side="left", padx=(20,0))
        self.combo_delivery = ttk.Combobox(row2, font=("Arial", 10), width=18, state="readonly")
        self.combo_delivery.pack(side="left", padx=10)
        self.cargar_personal_delivery()

        row3 = tk.Frame(frame_cab_content, bg="#FFFFFF")
        row3.pack(fill="x", pady=5)

        tk.Label(row3, text="Observaciones:", font=("Arial", 10, "bold"), bg="#FFFFFF").pack(anchor="w")
        self.txt_observaciones = tk.Text(row3, font=("Arial", 10), bg="#B3D9FF", height=3)
        self.txt_observaciones.pack(fill="x", pady=5)

        frame_cliente = tk.Frame(frame_scrollable, bg="#FFFFFF", relief="solid", bd=2)
        frame_cliente.pack(fill="x", pady=10, padx=10)

        lbl_cli_titulo = tk.Label(
            frame_cliente,
            text="DATOS DE CLIENTE",
            font=("Arial", 12, "bold"),
            bg="#5A7FFF",
            fg="#FFFFFF",
            pady=5
        )
        lbl_cli_titulo.pack(fill="x")

        frame_cli_content = tk.Frame(frame_cliente, bg="#FFFFFF", padx=10, pady=10)
        frame_cli_content.pack(fill="x")

        row_buscar = tk.Frame(frame_cli_content, bg="#FFFFFF")
        row_buscar.pack(fill="x", pady=5)

        tk.Label(row_buscar, text="DNI Cliente:", font=("Arial", 10, "bold"), bg="#FFFFFF").pack(side="left")
        self.txt_dni_cliente = tk.Entry(row_buscar, font=("Arial", 10), bg="#B3D9FF", width=15)
        self.txt_dni_cliente.pack(side="left", padx=10)

        btn_buscar_cliente = tk.Button(
            row_buscar,
            text="Buscar",
            font=("Arial", 10, "bold"),
            bg="#4CAF50",
            fg="#FFFFFF",
            command=self.buscar_cliente
        )
        btn_buscar_cliente.pack(side="left", padx=5)

        self.lbl_cliente_info = tk.Label(
            frame_cli_content,
            text="Seleccione un cliente...",
            font=("Arial", 10),
            bg="#FFFFFF",
            fg="#666666",
            justify="left"
        )
        self.lbl_cliente_info.pack(anchor="w", pady=10)

        frame_producto = tk.Frame(frame_scrollable, bg="#FFFFFF", relief="solid", bd=2)
        frame_producto.pack(fill="x", pady=10, padx=10)

        lbl_prod_titulo = tk.Label(
            frame_producto,
            text="DATOS DE PRODUCTO",
            font=("Arial", 12, "bold"),
            bg="#5A7FFF",
            fg="#FFFFFF",
            pady=5
        )
        lbl_prod_titulo.pack(fill="x")

        frame_prod_content = tk.Frame(frame_producto, bg="#FFFFFF", padx=10, pady=10)
        frame_prod_content.pack(fill="x")

        row_prod = tk.Frame(frame_prod_content, bg="#FFFFFF")
        row_prod.pack(fill="x", pady=5)

        tk.Label(row_prod, text="Producto:", font=("Arial", 10, "bold"), bg="#FFFFFF").pack(side="left")
        self.combo_producto = ttk.Combobox(row_prod, font=("Arial", 10), width=30, state="readonly")
        self.combo_producto.pack(side="left", padx=10)
        self.cargar_productos()

        tk.Label(row_prod, text="Cantidad:", font=("Arial", 10, "bold"), bg="#FFFFFF").pack(side="left", padx=(10,0))
        self.txt_cantidad = tk.Entry(row_prod, font=("Arial", 10), bg="#B3D9FF", width=10)
        self.txt_cantidad.pack(side="left", padx=10)

        btn_agregar = tk.Button(
            row_prod,
            text="Agregar",
            font=("Arial", 10, "bold"),
            bg="#2196F3",
            fg="#FFFFFF",
            command=self.agregar_producto
        )
        btn_agregar.pack(side="left", padx=5)

        frame_lista_prod = tk.Frame(frame_prod_content, bg="#FFFFFF")
        frame_lista_prod.pack(fill="both", expand=True, pady=10)

        self.tree_productos = ttk.Treeview(
            frame_lista_prod,
            columns=("producto", "cantidad", "precio", "subtotal"),
            show="headings",
            height=6
        )
        self.tree_productos.heading("producto", text="Producto")
        self.tree_productos.heading("cantidad", text="Cantidad")
        self.tree_productos.heading("precio", text="Precio Unit.")
        self.tree_productos.heading("subtotal", text="Subtotal")

        self.tree_productos.column("producto", width=250)
        self.tree_productos.column("cantidad", width=80)
        self.tree_productos.column("precio", width=100)
        self.tree_productos.column("subtotal", width=100)

        self.tree_productos.pack(side="left", fill="both", expand=True)

        scroll_tree = ttk.Scrollbar(frame_lista_prod, orient="vertical", command=self.tree_productos.yview)
        scroll_tree.pack(side="right", fill="y")
        self.tree_productos.configure(yscrollcommand=scroll_tree.set)

        frame_totales = tk.Frame(frame_scrollable, bg="#FFFFFF", relief="solid", bd=2)
        frame_totales.pack(fill="x", pady=10, padx=10)

        frame_tot_content = tk.Frame(frame_totales, bg="#FFFFFF", padx=10, pady=10)
        frame_tot_content.pack(fill="x")

        row_tot = tk.Frame(frame_tot_content, bg="#FFFFFF")
        row_tot.pack(fill="x")

        tk.Label(row_tot, text="IGV:", font=("Arial", 11, "bold"), bg="#B3D9FF", width=12).pack(side="left", padx=5)
        self.lbl_igv = tk.Label(row_tot, text="S/ 0.00", font=("Arial", 11), bg="#B3D9FF", width=15)
        self.lbl_igv.pack(side="left", padx=5)

        tk.Label(row_tot, text="SUBTOTAL:", font=("Arial", 11, "bold"), bg="#B3D9FF", width=12).pack(side="left", padx=5)
        self.lbl_subtotal = tk.Label(row_tot, text="S/ 0.00", font=("Arial", 11), bg="#B3D9FF", width=15)
        self.lbl_subtotal.pack(side="left", padx=5)

        tk.Label(row_tot, text="TOTAL:", font=("Arial", 11, "bold"), bg="#B3D9FF", width=12).pack(side="left", padx=5)
        self.lbl_total = tk.Label(row_tot, text="S/ 0.00", font=("Arial", 11), bg="#B3D9FF", width=15)
        self.lbl_total.pack(side="left", padx=5)

        frame_botones = tk.Frame(frame_scrollable, bg="#728EFF")
        frame_botones.pack(pady=20)

        btn_registrar = tk.Button(
            frame_botones,
            text="⚫ Registrar",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="#FFFFFF",
            width=15,
            command=self.registrar_pedido
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

        self.cliente_seleccionado = None

        if not modo_presentacion:
            self.window.mainloop()

    def generar_numero_pedido(self):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"PED-{timestamp}"

    def cargar_personal_delivery(self):
        personal = self.controlador.obtener_personal_delivery()
        valores = [f"{p['dni']} - {p['nombres']} {p['apellidos']}" for p in personal]
        self.combo_delivery['values'] = valores

    def cargar_productos(self):
        productos = self.controlador.obtener_productos()
        valores = [f"{p['numero_serie']} - {p['nombre']} (S/ {p['precio']})" for p in productos]
        self.combo_producto['values'] = valores

    def buscar_cliente(self):
        dni = self.txt_dni_cliente.get().strip()
        if not dni:
            messagebox.showwarning("Advertencia", "Ingrese el DNI del cliente")
            return

        cliente = self.controlador.buscar_cliente_por_dni(dni)
        if cliente:
            self.cliente_seleccionado = cliente
            info = f"Código: {cliente['idcliente']}\n"
            info += f"Nombres: {cliente['nombres']} {cliente['apellidos']}\n"
            info += f"Dirección: {cliente['direccion']}, {cliente['distrito']}\n"
            info += f"Correo: {cliente['correo']} | Celular: {cliente['celular']}"
            self.lbl_cliente_info.config(text=info, fg="#000000")
        else:
            messagebox.showerror("Error", "Cliente no encontrado")
            self.cliente_seleccionado = None

    def agregar_producto(self):
        if not self.combo_producto.get():
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            return

        try:
            cantidad = int(self.txt_cantidad.get())
            if cantidad <= 0:
                raise ValueError
        except:
            messagebox.showwarning("Advertencia", "Ingrese una cantidad válida (número entero positivo)")
            return

        producto_str = self.combo_producto.get()
        numero_serie = producto_str.split(" - ")[0]
        producto = self.controlador.obtener_producto_por_serie(numero_serie)

        if not producto:
            messagebox.showerror("Error", "Producto no encontrado")
            return

        # Verificar stock actual del producto
        stock_disponible = producto.get('stock', 0)
        if cantidad > stock_disponible:
            messagebox.showwarning(
                "Stock Insuficiente",
                f"Producto: {producto['nombre']}\n"
                f"Stock disponible: {stock_disponible}\n"
                f"Cantidad solicitada: {cantidad}\n\n"
                f"No hay suficiente stock para esta operación."
            )
            return

        # Verificar que no se agregue el mismo producto dos veces con cantidades insuficientes
        cantidad_ya_agregada = 0
        for prod in self.productos_seleccionados:
            if prod['idproducto'] == producto['idproducto']:
                cantidad_ya_agregada += prod['cantidad']
        
        cantidad_total_solicitada = cantidad_ya_agregada + cantidad
        if cantidad_total_solicitada > stock_disponible:
            messagebox.showwarning(
                "Stock Insuficiente",
                f"Producto: {producto['nombre']}\n"
                f"Stock disponible: {stock_disponible}\n"
                f"Ya agregado: {cantidad_ya_agregada}\n"
                f"Intenta agregar: {cantidad}\n"
                f"Total solicitado: {cantidad_total_solicitada}\n\n"
                f"La cantidad total excede el stock disponible."
            )
            return

        # Restar stock inmediatamente en la BD
        exito, mensaje = self.controlador.restar_stock_en_bd(producto['idproducto'], cantidad)
        if not exito:
            messagebox.showerror("Error", f"No se pudo restar el stock: {mensaje}")
            return

        subtotal = float(producto['precio']) * cantidad
        self.productos_seleccionados.append({
            'idproducto': producto['idproducto'],
            'nombre': producto['nombre'],
            'cantidad': cantidad,
            'precio': float(producto['precio']),
            'subtotal': subtotal
        })

        self.tree_productos.insert(
            "",
            "end",
            values=(
                producto['nombre'],
                cantidad,
                f"S/ {float(producto['precio']):.2f}",
                f"S/ {subtotal:.2f}"
            )
        )

        self.actualizar_totales()
        self.txt_cantidad.delete(0, tk.END)
        messagebox.showinfo(
            "Producto Agregado",
            f"{producto['nombre']}\nCantidad: {cantidad}\nStock restante: {stock_disponible - cantidad}"
        )

    def actualizar_totales(self):
        subtotal = sum(p['subtotal'] for p in self.productos_seleccionados)
        igv = subtotal * 0.18
        total = subtotal + igv

        self.lbl_subtotal.config(text=f"S/ {subtotal:.2f}")
        self.lbl_igv.config(text=f"S/ {igv:.2f}")
        self.lbl_total.config(text=f"S/ {total:.2f}")

    def registrar_pedido(self):
        if not self.cliente_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un cliente")
            return

        if not self.productos_seleccionados:
            messagebox.showwarning("Advertencia", "Agregue al menos un producto")
            return

        if not self.combo_delivery.get():
            messagebox.showwarning("Advertencia", "Seleccione personal de delivery")
            return

        # Obtener datos
        numero_pedido = self.txt_num_pedido.get()
        fecha_pedido = self.txt_fecha_pedido.get()
        fecha_entrega = self.txt_fecha_entrega.get() or None
        observaciones = self.txt_observaciones.get("1.0", tk.END).strip()
    
        delivery_str = self.combo_delivery.get()
        dni_delivery = delivery_str.split(" - ")[0]
        delivery = self.controlador.obtener_delivery_por_dni(dni_delivery)

        # Calcular totales
        subtotal = float(sum(p['subtotal'] for p in self.productos_seleccionados))
        igv = float(subtotal * 0.18)
        total = float(subtotal + igv)

        # El stock, fue restado al agregar cada producto
        # Solo se registra el pedido en la BD
        exito, mensaje = self.controlador.registrar_pedido(
            numero_pedido=numero_pedido,
            fecha_pedido=fecha_pedido,
            fecha_entrega=fecha_entrega,
            observaciones=observaciones,
            subtotal=subtotal,
            igv=igv,
            total=total,
            idcliente=self.cliente_seleccionado['idcliente'],
            idusuario=getattr(self.usuario, 'idusuario', 1),
            iddelivery=delivery['iddelivery'] if delivery else None,
            productos=self.productos_seleccionados
        )

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            if not self.modo_presentacion:
                self.volver()
            else:
                self.limpiar_formulario()
        else:
            messagebox.showerror("Error", mensaje)

    def limpiar_formulario(self):
        # Limpiar productos seleccionados
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)
        self.productos_seleccionados = []
        
        # Resetear totales
        self.actualizar_totales()
        
        # Limpiar campos
        self.txt_dni_cliente.delete(0, tk.END)
        self.lbl_cliente_info.config(text="Seleccione un cliente...", fg="#666666")
        self.cliente_seleccionado = None
        self.txt_observaciones.delete("1.0", tk.END)
        self.txt_cantidad.delete(0, tk.END)
        
        # Generar nuevo número de pedido
        self.txt_num_pedido.delete(0, tk.END)
        self.txt_num_pedido.insert(0, self.generar_numero_pedido())

    def volver(self):
        self.window.destroy()
        if not self.modo_presentacion:
            from src.vistas.vista_empleado import VistaEmpleado
            VistaEmpleado(self.usuario)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
