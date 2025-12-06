from src.database.conexion import ConexionDB
from functools import reduce
from typing import List, Dict, Optional, Callable
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from decimal import Decimal

def calcular_subtotal(precio: float, cantidad: int) -> float:
    return round(float(precio) * cantidad, 2)

def calcular_igv(subtotal: float, tasa_igv: float = 0.18) -> float:
    return round(float(subtotal) * tasa_igv, 2)

def calcular_total(subtotal: float, igv: float) -> float:
    return round(float(subtotal) + float(igv), 2)

def validar_stock(producto: Dict, cantidad_solicitada: int) -> bool:
    stock_disponible = producto.get('stock', 0)
    print(f"Validando Stock: Producto = {producto['nombre']} | Stock disponible = {stock_disponible} | Cantidad solicitada = {cantidad_solicitada}")
    if stock_disponible >= cantidad_solicitada:
        return True
    return False

def aplicar_descuento(monto: float, porcentaje_descuento: float) -> float:
    descuento = float(monto) * (porcentaje_descuento / 100)
    return round(float(monto) - descuento, 2)

def filtrar_productos_disponibles(productos: List[Dict]) -> List[Dict]:
    return list(filter(lambda p: p.get('stock', 0) > 0, productos))

def mapear_productos_a_resumen(productos: List[Dict]) -> List[str]:
    return list(map(
        lambda p: f"{p['numero_serie']} - {p['nombre']} (S/ {float(p['precio']):.2f})",
        productos
    ))

def calcular_total_carrito(productos_carrito: List[Dict]) -> float:
    return float(reduce(
        lambda acc, prod: acc + float(prod.get('subtotal', 0)),
        productos_carrito,
        0.0
    ))

def aplicar_funcion_a_precios(productos: List[Dict], func: Callable) -> List[Dict]:
    return [{**p, 'precio': func(float(p['precio']))} for p in productos]

class ReglasNegocioPedidos:
    @staticmethod
    def puede_realizar_pedido(cliente: Dict, productos: List[Dict]) -> tuple:
        if not cliente or not cliente.get('idcliente'):
            return False, "Cliente no válido"
        if not productos or len(productos) == 0:
            return False, "No hay productos en el pedido"
        total = calcular_total_carrito(productos)
        if total <= 0:
            return False, "El monto total debe ser mayor a 0"
        return True, "Pedido válido"

    @staticmethod
    def determinar_prioridad_entrega(pedido: Dict) -> str:
        total = float(pedido.get('total', 0))
        if total > 500:
            return "ALTA"
        elif total > 200:
            return "MEDIA"
        else:
            return "BAJA"

    @staticmethod
    def aplicar_descuento_por_volumen(cantidad: int) -> float:
        if cantidad >= 10:
            return 10.0
        elif cantidad >= 5:
            return 5.0
        else:
            return 0.0

    @staticmethod
    def validar_fecha_entrega(fecha_pedido: str, fecha_entrega: str) -> tuple:
        try:
            f_pedido = datetime.strptime(fecha_pedido, "%Y-%m-%d")
            f_entrega = datetime.strptime(fecha_entrega, "%Y-%m-%d")
            if f_entrega < f_pedido:
                return False, "La fecha de entrega no puede ser anterior al pedido"
            if (f_entrega - f_pedido).days > 30:
                return False, "La fecha de entrega no puede ser mayor a 30 días"
            return True, "Fecha válida"
        except:
            return False, "Formato de fecha inválido"

class AnalizadorPedidos:
    @staticmethod
    def analizar_pedidos_con_pandas(pedidos: List[Dict]) -> Dict:
        if not pedidos:
            return {
                'total_pedidos': 0,
                'monto_total': 0,
                'monto_promedio': 0,
                'monto_maximo': 0,
                'monto_minimo': 0
            }
        df = pd.DataFrame(pedidos)
        if 'total' in df.columns:
            df['total'] = pd.to_numeric(df['total'], errors='coerce')
        estadisticas = {
            'total_pedidos': len(df),
            'monto_total': float(df['total'].sum() if 'total' in df.columns else 0),
            'monto_promedio': float(df['total'].mean() if 'total' in df.columns else 0),
            'monto_maximo': float(df['total'].max() if 'total' in df.columns else 0),
            'monto_minimo': float(df['total'].min() if 'total' in df.columns else 0),
            'desviacion_std': float(df['total'].std() if 'total' in df.columns else 0)
        }
        return estadisticas

    @staticmethod
    def calcular_metricas_numpy(montos: List[float]) -> Dict:
        if not montos:
            return {
                'media': 0,
                'mediana': 0,
                'percentil_25': 0,
                'percentil_75': 0
            }
        arr = np.array([float(m) for m in montos])
        return {
            'media': float(np.mean(arr)),
            'mediana': float(np.median(arr)),
            'percentil_25': float(np.percentile(arr, 25)),
            'percentil_75': float(np.percentile(arr, 75)),
            'varianza': float(np.var(arr)),
            'suma_total': float(np.sum(arr))
        }

    @staticmethod
    def pedidos_por_estado_pandas(pedidos: List[Dict]) -> pd.DataFrame:
        if not pedidos:
            return pd.DataFrame()
        df = pd.DataFrame(pedidos)
        if 'estado' in df.columns and 'total' in df.columns:
            df['total'] = pd.to_numeric(df['total'], errors='coerce')
            resumen = df.groupby('estado').agg({
                'total': ['count', 'sum', 'mean'],
                'numero_pedido': 'count'
            }).round(2)
            return resumen
        return pd.DataFrame()

class ControladorPedidos:
    def __init__(self):
        self.conexion = ConexionDB()
        self.reglas = ReglasNegocioPedidos()
        self.analizador = AnalizadorPedidos()

    def obtener_personal_delivery(self) -> List[Dict]:
        db = self.conexion.conectar()
        if db is None:
            return []
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM delivery"
        cursor.execute(query)
        resultado = cursor.fetchall()
        self.conexion.cerrar_conexion()
        return resultado

    def obtener_productos(self) -> List[Dict]:
        db = self.conexion.conectar()
        if db is None:
            return []
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM productos"
        cursor.execute(query)
        productos = cursor.fetchall()
        self.conexion.cerrar_conexion()
        # Convertir Decimal a float para evitar problemas
        productos_convertidos = []
        for p in productos:
            producto_dict = dict(p)
            if 'precio' in producto_dict and isinstance(producto_dict['precio'], Decimal):
                producto_dict['precio'] = float(producto_dict['precio'])
            productos_convertidos.append(producto_dict)
        return filtrar_productos_disponibles(productos_convertidos)

    def obtener_producto_por_serie(self, numero_serie: str) -> Optional[Dict]:
        db = self.conexion.conectar()
        if db is None:
            return None
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM productos WHERE numero_serie = %s"
        cursor.execute(query, (numero_serie,))
        resultado = cursor.fetchone()
        self.conexion.cerrar_conexion()
        # Convertir Decimal a float
        if resultado and 'precio' in resultado:
            if isinstance(resultado['precio'], Decimal):
                resultado['precio'] = float(resultado['precio'])
        return resultado

    def buscar_cliente_por_dni(self, dni: str) -> Optional[Dict]:
        db = self.conexion.conectar()
        if db is None:
            return None
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM clientes WHERE dni = %s"
        cursor.execute(query, (dni,))
        resultado = cursor.fetchone()
        self.conexion.cerrar_conexion()
        return resultado

    def obtener_delivery_por_dni(self, dni: str) -> Optional[Dict]:
        db = self.conexion.conectar()
        if db is None:
            return None
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM delivery WHERE dni = %s"
        cursor.execute(query, (dni,))
        resultado = cursor.fetchone()
        self.conexion.cerrar_conexion()
        return resultado

    def restar_stock_en_bd(self, idproducto: int, cantidad: int) -> tuple:
        """
        Resta el stock de un producto en la BD de manera inmediata.
        Retorna (exito: bool, mensaje: str)
        """
        db = self.conexion.conectar()
        if db is None:
            return False, "Error de conexión a la base de datos"
        
        try:
            cursor = db.cursor()
            
            # Verificar stock actual
            query_verificar = "SELECT stock FROM productos WHERE idproducto = %s"
            cursor.execute(query_verificar, (idproducto,))
            resultado = cursor.fetchone()
            
            if not resultado:
                self.conexion.cerrar_conexion()
                return False, "Producto no encontrado"
            
            stock_actual = resultado[0]
            if stock_actual < cantidad:
                self.conexion.cerrar_conexion()
                return False, f"Stock insuficiente. Disponible: {stock_actual}"
            
            # Restar stock
            query_update = "UPDATE productos SET stock = stock - %s WHERE idproducto = %s"
            cursor.execute(query_update, (cantidad, idproducto))
            db.commit()
            
            self.conexion.cerrar_conexion()
            return True, "Stock restado correctamente"
            
        except Exception as e:
            db.rollback()
            self.conexion.cerrar_conexion()
            return False, f"Error al restar stock: {str(e)}"


    def registrar_pedido(self, numero_pedido: str, fecha_pedido: str,
                        fecha_entrega: Optional[str], observaciones: str,
                        subtotal: float, igv: float, total: float,
                        idcliente: int, idusuario: int,
                        iddelivery: Optional[int], productos: List[Dict]) -> tuple:

        # Convertir todos los valores a float para evitar problemas con Decimal
        subtotal = float(subtotal)
        igv = float(igv)
        total = float(total)

        if fecha_entrega:
            fecha_valida, msg = self.reglas.validar_fecha_entrega(
                fecha_pedido, fecha_entrega
            )
            if not fecha_valida:
                return False, msg

        cliente = {'idcliente': idcliente}
        puede_realizar, razon = self.reglas.puede_realizar_pedido(cliente, productos)

        if not puede_realizar:
            return False, razon

        db = self.conexion.conectar()
        if db is None:
            return False, "Error de conexión a la base de datos"

        try:
            cursor = db.cursor()
            prioridad = self.reglas.determinar_prioridad_entrega({'total': total})

            query_pedido = """
                INSERT INTO pedidos 
                (numero_pedido, fecha_pedido, fecha_entrega, observaciones, 
                subtotal, igv, total, idcliente, idusuario, iddelivery, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'pendiente')
            """
            cursor.execute(query_pedido, (
                numero_pedido, fecha_pedido, fecha_entrega,
                f"{observaciones} [Prioridad: {prioridad}]",
                subtotal, igv, total, idcliente, idusuario, iddelivery
            ))

            idpedido = cursor.lastrowid

            query_detalle = """
                INSERT INTO detalle_pedido 
                (idpedido, idproducto, cantidad, precio_unit, subtotal)
                VALUES (%s, %s, %s, %s, %s)
            """

            detalles_preparados = list(map(
                lambda p: (
                    idpedido,
                    p['idproducto'],
                    p['cantidad'],
                    float(p['precio']),
                    float(p['subtotal'])
                ),
                productos
            ))
            
            # Registrar detalles (el stock, fue restado al agregar cada producto)
            for detalle in detalles_preparados:
                cursor.execute(query_detalle, detalle)

            db.commit()
            self.conexion.cerrar_conexion()
            return True, f"Pedido registrado exitosamente con prioridad {prioridad}"

        except Exception as e:
            print(f"Error al registrar pedido: {e}")
            db.rollback()
            self.conexion.cerrar_conexion()
            return False, f"Error al registrar pedido: {str(e)}"
        

    def buscar_pedidos_por_cliente(self, criterio: str, valor) -> List[Dict]:
        db = self.conexion.conectar()
        if db is None:
            return []
        cursor = db.cursor(dictionary=True)

        if criterio == "nombre":
            query = """
                SELECT p.*, c.nombres, c.apellidos, c.dni as dni_cliente
                FROM pedidos p
                INNER JOIN clientes c ON p.idcliente = c.idcliente
                WHERE c.nombres LIKE %s
                ORDER BY p.fecha_pedido DESC
            """
            cursor.execute(query, (f"%{valor}%",))
        elif criterio == "apellido":
            query = """
                SELECT p.*, c.nombres, c.apellidos, c.dni as dni_cliente
                FROM pedidos p
                INNER JOIN clientes c ON p.idcliente = c.idcliente
                WHERE c.apellidos LIKE %s
                ORDER BY p.fecha_pedido DESC
            """
            cursor.execute(query, (f"%{valor}%",))
        elif criterio == "rango_fechas":
            fecha_desde, fecha_hasta = valor
            query = """
                SELECT p.*, c.nombres, c.apellidos, c.dni as dni_cliente
                FROM pedidos p
                INNER JOIN clientes c ON p.idcliente = c.idcliente
                WHERE p.fecha_pedido BETWEEN %s AND %s
                ORDER BY p.fecha_pedido DESC
            """
            cursor.execute(query, (fecha_desde, fecha_hasta))

        resultado = cursor.fetchall()
        self.conexion.cerrar_conexion()
        
        # Convertir Decimal a float en los resultados
        resultados_convertidos = []
        for r in resultado:
            resultado_dict = dict(r)
            for key, value in resultado_dict.items():
                if isinstance(value, Decimal):
                    resultado_dict[key] = float(value)
            resultados_convertidos.append(resultado_dict)
        
        return resultados_convertidos

    def obtener_detalle_pedido(self, idpedido: int) -> List[Dict]:
        db = self.conexion.conectar()
        if db is None:
            return []
        cursor = db.cursor(dictionary=True)
        query = """
            SELECT dp.*, pr.nombre, pr.numero_serie
            FROM detalle_pedido dp
            INNER JOIN productos pr ON dp.idproducto = pr.idproducto
            WHERE dp.idpedido = %s
        """
        cursor.execute(query, (idpedido,))
        resultado = cursor.fetchall()
        self.conexion.cerrar_conexion()
        
        # Convertir Decimal a float en los resultados
        resultados_convertidos = []
        for r in resultado:
            resultado_dict = dict(r)
            for key, value in resultado_dict.items():
                if isinstance(value, Decimal):
                    resultado_dict[key] = float(value)
            resultados_convertidos.append(resultado_dict)
        
        return resultados_convertidos
    
    def registrar_entrega(self, idpedido, fecha_entrega, observaciones):
        db = self.conexion.conectar()
        if db is None:
            return False

        try:
            cursor = db.cursor()

            # Insertar entrega
            query_entrega = """
                INSERT INTO entregas (idpedido, fecha_entrega, observaciones)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query_entrega, (idpedido, fecha_entrega, observaciones))

            # Actualizar estado del pedido
            query_update = "UPDATE pedidos SET estado = 'entregado' WHERE idpedido = %s"
            cursor.execute(query_update, (idpedido,))

            db.commit()
            self.conexion.cerrar_conexion()
            return True

        except Exception as e:
            print(f"Error al registrar entrega: {e}")
            db.rollback()
            self.conexion.cerrar_conexion()
            return False

    def obtener_pedidos_pendientes_por_cliente(self, dni_cliente):
        db = self.conexion.conectar()
        if db is None:
            return []

        cursor = db.cursor(dictionary=True)
        query = """
            SELECT p.*, c.nombres, c.apellidos
            FROM pedidos p
            INNER JOIN clientes c ON p.idcliente = c.idcliente
            WHERE c.dni = %s AND p.estado != 'entregado'
            ORDER BY p.fecha_pedido DESC
        """
        cursor.execute(query, (dni_cliente,))
        resultado = cursor.fetchall()
        self.conexion.cerrar_conexion()
        return resultado

    def obtener_pedidos_por_delivery(self, dni_delivery):
        db = self.conexion.conectar()
        if db is None:
            return []

        cursor = db.cursor(dictionary=True)
        query = """
            SELECT p.*, c.nombres, c.apellidos, d.nombres as delivery_nombres, d.apellidos as delivery_apellidos
            FROM pedidos p
            INNER JOIN clientes c ON p.idcliente = c.idcliente
            INNER JOIN delivery d ON p.iddelivery = d.iddelivery
            WHERE d.dni = %s AND p.estado != 'entregado'
            ORDER BY p.fecha_pedido DESC
        """
        cursor.execute(query, (dni_delivery,))
        resultado = cursor.fetchall()
        self.conexion.cerrar_conexion()
        return resultado

    def actualizar_pedido(self, id_pedido, fecha_entrega, observaciones, estado):
        return self.modelo.actualizar_pedido(
            id_pedido, fecha_entrega, observaciones, estado
        )
