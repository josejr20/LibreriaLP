import tkinter as tk
from tkinter import messagebox
from src.controladores.controlador_pedidos import ControladorPedidos


class VentanaEditarEntrega(tk.Toplevel):
    def __init__(self, parent, idpedido):
        super().__init__(parent)
        self.title("Registrar Entrega")
        self.idpedido = idpedido
        self.controlador = ControladorPedidos()

        tk.Label(self, text="Fecha de Entrega (YYYY-MM-DD):").pack()
        self.entry_fecha = tk.Entry(self)
        self.entry_fecha.pack()

        tk.Label(self, text="Observaciones:").pack()
        self.entry_obs = tk.Entry(self)
        self.entry_obs.pack()

        btn_guardar = tk.Button(self, text="Guardar", command=self.guardar)
        btn_guardar.pack(pady=10)

    def guardar(self):
        fecha = self.entry_fecha.get()
        obs = self.entry_obs.get()

        exito = self.controlador.registrar_entrega(self.idpedido, fecha, obs)

        if exito:
            messagebox.showinfo("Éxito", "Entrega registrada correctamente.")
            self.destroy()
        else:
            messagebox.showerror("Error", "No se pudo registrar la entrega.")
