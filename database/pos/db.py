import sqlite3
from pathlib import Path

DEFAULT_DB = Path(__file__).resolve().parent.parent / "data" / "pos.db"

class Database:
    def __init__(self, path=None):
        self.path = str(path or DEFAULT_DB)
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)

    def connect(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def init_schema(self):
        ddl = [
            '''
            CREATE TABLE IF NOT EXISTS usuario (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                correo TEXT NOT NULL UNIQUE,
                rol TEXT NOT NULL
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS cliente (
                id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                correo TEXT NOT NULL UNIQUE,
                telefono TEXT NOT NULL
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS producto (
                id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL CHECK(precio >= 0),
                stock INTEGER NOT NULL CHECK(stock >= 0),
                codigo_barras TEXT UNIQUE,             
                iva REAL NOT NULL DEFAULT 0            
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS venta (
                id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                total REAL NOT NULL CHECK(total >= 0),
                id_cliente INTEGER NOT NULL,
                id_usuario INTEGER NOT NULL,
                FOREIGN KEY(id_cliente) REFERENCES cliente(id_cliente),
                FOREIGN KEY(id_usuario) REFERENCES usuario(id_usuario)
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS detalle_venta (
                id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
                id_venta INTEGER NOT NULL,
                id_producto INTEGER NOT NULL,
                cantidad INTEGER NOT NULL CHECK(cantidad > 0),
                precio_unitario REAL NOT NULL CHECK(precio_unitario >= 0),
                FOREIGN KEY(id_venta) REFERENCES venta(id_venta) ON DELETE CASCADE,
                FOREIGN KEY(id_producto) REFERENCES producto(id_producto)
            );
            ''',
        ]
        with self.connect() as conn:
            for stmt in ddl:
                conn.execute(stmt)
            conn.commit()
