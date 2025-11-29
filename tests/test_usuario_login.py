from src.controladores.controlador_usuario import ControladorUsuario

def test_login():
    print("=== INICIANDO TEST LOGIN ===")
    controlador = ControladorUsuario()

    print("---- TEST LOGIN ADMIN ----")
    usuario_admin = controlador.autenticar_usuario("admin", "admin")
    if usuario_admin:
        print("OK: Login exitoso para ADMIN")
        print(f"Usuario: {usuario_admin.usuario} | Rol: {usuario_admin.rol}")
    else:
        print("FAIL: Admin no autenticado")

    print("\n---- TEST LOGIN EMPLEADO ----")
    usuario_worker = controlador.autenticar_usuario("worker", "worker")
    if usuario_worker:
        print("OK: Login exitoso para WORKER")
        print(f"Usuario: {usuario_worker.usuario} | Rol: {usuario_worker.rol}")
    else:
        print("FAIL: Empleado no autenticado")

    print("\n---- TEST CREDENCIALES INCORRECTAS ----")
    usuario_fake = controlador.autenticar_usuario("test", "123")
    if usuario_fake is None:
        print("OK: Credenciales incorrectas detectadas")
    else:
        print("FAIL: Error, se autentica usuario inválido")

if __name__ == "__main__":
    test_login()