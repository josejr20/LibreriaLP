import tkinter as tk
from tkinter import messagebox
from src.controladores.controlador_usuario import ControladorUsuario


class LoginView:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Librería UTP - Login")
        self.window.geometry("400x300")
        self.window.configure(bg="#728EFF")

        #  CUADRO CENTRAL 
        frame_cuadro = tk.Frame(
            self.window,
            bg="white",
            highlightbackground="#83B3FF",
            highlightthickness=4,
            bd=0
        )
        frame_cuadro.place(relx=0.5, rely=0.5, anchor="center")

        frame_cuadro_inner = tk.Frame(frame_cuadro, bg="white", padx=20, pady=20)
        frame_cuadro_inner.pack()

        # TÍTULO PRINCIPAL 
        lbl_titulo = tk.Label(
            frame_cuadro_inner,
            text="Bienvenido",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#000000"
        )
        lbl_titulo.pack(pady=(0, 15))

        # Usuario 
        lbl_usuario = tk.Label(
            frame_cuadro_inner,
            text="Usuario",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#000000",
            anchor="w"
        )
        lbl_usuario.pack(fill="x")

        self.txt_usuario = tk.Entry(frame_cuadro_inner, font=("Arial", 11), bg="#D9D9D9")
        self.txt_usuario.pack(fill="x", pady=5)

        # Contraseña 
        lbl_pass = tk.Label(
            frame_cuadro_inner,
            text="Contraseña",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#000000",
            anchor="w"
        )
        lbl_pass.pack(fill="x")

        self.txt_password = tk.Entry(frame_cuadro_inner, show="*", font=("Arial", 11), bg="#D9D9D9")
        self.txt_password.pack(fill="x", pady=5)

        # Bind Enter key para autenticar
        self.txt_password.bind("<Return>", lambda event: self.autenticar())

        # BOTÓN Ingresar
        btn_ingresar = tk.Button(
            frame_cuadro_inner,
            text="Ingresar",
            font=("Arial", 12, "bold"),
            bg="#B3D9FF",
            fg="#000000",
            activebackground="#FFB800",
            activeforeground="#000000",
            command=self.autenticar
        )
        btn_ingresar.pack(pady=15, fill="x")

        self.window.mainloop()

    def autenticar(self):
        usuario = self.txt_usuario.get()
        password = self.txt_password.get()

        controlador = ControladorUsuario()
        user = controlador.autenticar_usuario(usuario, password)

        if user:  
            self.window.destroy()

            if user.rol == "administrador":
                from src.vistas.vista_administrador import VistaAdministrador
                VistaAdministrador(user)
            elif user.rol == "empleado":
                from src.vistas.vista_empleado import VistaEmpleado
                VistaEmpleado(user)
            else:
                messagebox.showinfo("Acceso", "Rol no reconocido")
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")