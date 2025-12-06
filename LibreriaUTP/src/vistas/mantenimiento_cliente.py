import tkinter as tk
from tkinter import ttk, messagebox
from src.controladores.controlador_cliente import ControladorCliente
from src.modelos.cliente import Cliente

class MantenimientoCliente:

    def __init__(self, parent):
        self.controller = ControladorCliente()

        self.window = tk.Toplevel(parent)
        self.window.title("Mantenimiento de Clientes")
        self.window.geometry("820x650")
        self.window.configure(bg="#6D8BFF")

        # --------------------------------------------------------
        # TITULO
        frame_title = tk.Frame(self.window, bg="white", bd=3, relief="ridge")
        frame_title.pack(fill="x", padx=20, pady=20)

        tk.Label(frame_title, text="Mantenimiento de Clientes",
                 bg="white", font=("Arial", 22, "bold")).pack(pady=10)

        # --------------------------------------------------------
        # PANEL PRINCIPAL
        panel = tk.Frame(self.window, bg="white", bd=4, relief="ridge")
        panel.pack(fill="both", expand=True, padx=30, pady=10)

        form = tk.Frame(panel, bg="white")
        form.pack(pady=10)

        labels = [
            "Usuario", "Contraseña", "DNI",
            "Nombres", "Apellidos", "Dirección",
            "Distrito", "Correo", "Celular"
        ]

        self.entries = []

        for i, t in enumerate(labels):
            tk.Label(form, text=t + ":", bg="white",
                     font=("Arial", 13, "bold")).grid(row=i, column=0, sticky="e", pady=7)

            entry = ttk.Entry(form, width=45)
            entry.grid(row=i, column=1, padx=10, pady=7)
            self.entries.append(entry)

        # --------------------------------------------------------
        # BOTONES
        btns = tk.Frame(panel, bg="white")
        btns.pack(pady=20)

        ttk.Button(btns, text="Buscar", width=18, command=self.buscar).grid(row=0, column=0, padx=6)
        ttk.Button(btns, text="Registrar", width=18, command=self.registrar).grid(row=0, column=1, padx=6)
        ttk.Button(btns, text="Modificar", width=18, command=self.modificar).grid(row=0, column=2, padx=6)
        ttk.Button(btns, text="Eliminar", width=18, command=self.eliminar).grid(row=0, column=3, padx=6)

    # --------------------------------------------------------
    # MÉTODOS AUXILIARES

    def limpiar(self):
        for e in self.entries:
            e.delete(0, tk.END)

    def obtener_cliente(self):
        valores = [e.get().strip() for e in self.entries]

        usuario, contrasena, dni, nombres, apellidos, direccion, distrito, correo, celular = valores

        if dni == "":
            messagebox.showerror("Error", "El DNI es obligatorio.")
            return None

        return Cliente(
            None, usuario, contrasena, dni, nombres,
            apellidos, direccion, distrito, correo, celular
        )

    # --------------------------------------------------------
    # CRUD TKINTER

    def buscar(self):
        parametro = self.entries[2].get().strip()  # ahora sí: DNI

        if not parametro:
            messagebox.showerror("Error", "Ingrese DNI o texto para buscar.")
            return

        c = self.controller.buscar(parametro)

        if not c:
            messagebox.showwarning("Aviso", "Cliente no encontrado.")
            return

        datos = [
            c.usuario, c.contrasena, c.dni, c.nombres, c.apellidos,
            c.direccion, c.distrito, c.correo, c.celular
        ]

        for i, val in enumerate(datos):
            self.entries[i].delete(0, tk.END)
            self.entries[i].insert(0, val)

    def registrar(self):
        cliente = self.obtener_cliente()
        if not cliente: return

        self.controller.registrar(cliente)
        messagebox.showinfo("Éxito", "Cliente registrado.")
        self.limpiar()

    def modificar(self):
        cliente = self.obtener_cliente()
        if not cliente: return

        self.controller.modificar(cliente)
        messagebox.showinfo("Éxito", "Cliente modificado.")
        self.limpiar()

    def eliminar(self):
        dni = self.entries[2].get().strip()

        if dni == "":
            messagebox.showerror("Error", "Ingrese un DNI para eliminar.")
            return

        self.controller.eliminar(dni)
        messagebox.showinfo("Éxito", "Cliente eliminado.")
        self.limpiar()