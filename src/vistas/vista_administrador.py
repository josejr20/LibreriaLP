import tkinter as tk
from src.controladores.controlador_administrador import ControladorAdministrador

class VistaAdministrador:
    def __init__(self, usuario):
        self.controlador = ControladorAdministrador(usuario)

        self.window = tk.Tk()
        self.window.title("Panel Administrador - Librería UTP")
        self.window.geometry("600x400")
        self.window.configure(bg="#728EFF")

        datos = self.controlador.obtener_datos()

        # TÍTULO
        lbl_header = tk.Label(
            self.window,
            text="ADMINISTRADOR",
            font=("Arial", 20, "bold"),
            bg="#FFFFFF",
            fg="#000000",
            width=25,
            height=2
        )
        lbl_header.pack(pady=20)

        # cuadro inferior
        frame_opciones = tk.Frame(self.window, bg="white", width=300, height=200)
        frame_opciones.pack(pady=20)

        # botones
        tk.Button(frame_opciones, text="Gestión de Productos", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Button(frame_opciones, text="Reportes", font=("Arial", 12, "bold")).pack(pady=10)

        self.window.mainloop()