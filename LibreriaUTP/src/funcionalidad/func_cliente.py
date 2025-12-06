from src.controladores.controlador_cliente import ControladorCliente
from src.modelos.cliente import Cliente

class FuncionalidadCliente:

    def __init__(self):
        self.ctrl = ControladorCliente()

    def registrar(self, cliente: Cliente):
        return self.ctrl.registrar(cliente)

    def buscar(self, parametro):
        return self.ctrl.buscar(parametro)

    def modificar(self, cliente: Cliente):
        return self.ctrl.modificar(cliente)

    def eliminar(self, dni):
        return self.ctrl.eliminar(dni)