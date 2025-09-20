class Producto:
    def __init__(self, id_producto, nombre, precio, stock, codigo_barras=None, iva=0):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.codigo_barras = codigo_barras
        self.iva = iva
