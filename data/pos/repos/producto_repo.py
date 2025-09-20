from ..db import Database
from ..models.producto import Producto

class ProductoRepo:
    def __init__(self, db: Database):
        self.db = db


    def _row_to_producto(self, r) -> Producto:
     
        cols = set(r.keys())
        codigo_barras = r["codigo_barras"] if "codigo_barras" in cols else None
        iva = r["iva"] if "iva" in cols else 0
        return Producto(
            r["id_producto"],
            r["nombre"],
            r["precio"],
            r["stock"],
            codigo_barras,
            iva,
        )

    # ---------- CRUD ----------
    def crear(self, p: Producto) -> int:
        """
        Inserta un producto. Requiere:
          - nombre (str)
          - precio (float >= 0)
          - stock (int >= 0)
          - codigo_barras (str | None)  -> UNIQUE si se define
          - iva (float, porcentaje; p.ej. 19, 0)
        """
        with self.db.connect() as conn:
           
            has_cols = set()
            for row in conn.execute("PRAGMA table_info(producto);").fetchall():
                has_cols.add(row["name"])

            if "codigo_barras" in has_cols and "iva" in has_cols:
                cur = conn.execute(
                    "INSERT INTO producto(nombre, precio, stock, codigo_barras, iva) VALUES (?, ?, ?, ?, ?);",
                    (p.nombre, p.precio, p.stock, p.codigo_barras, p.iva),
                )
            elif "codigo_barras" in has_cols:
                cur = conn.execute(
                    "INSERT INTO producto(nombre, precio, stock, codigo_barras) VALUES (?, ?, ?, ?);",
                    (p.nombre, p.precio, p.stock, p.codigo_barras),
                )
            elif "iva" in has_cols:
                cur = conn.execute(
                    "INSERT INTO producto(nombre, precio, stock, iva) VALUES (?, ?, ?, ?);",
                    (p.nombre, p.precio, p.stock, p.iva),
                )
            else:
                cur = conn.execute(
                    "INSERT INTO producto(nombre, precio, stock) VALUES (?, ?, ?);",
                    (p.nombre, p.precio, p.stock),
                )

            return cur.lastrowid

    def listar(self):
        with self.db.connect() as conn:
            rows = conn.execute("SELECT * FROM producto;").fetchall()
            return [self._row_to_producto(r) for r in rows]

    def actualizar(self, p: Producto) -> None:
        assert p.id_producto is not None, "id_producto requerido para actualizar"
        with self.db.connect() as conn:
           
            has_cols = set()
            for row in conn.execute("PRAGMA table_info(producto);").fetchall():
                has_cols.add(row["name"])

            if "codigo_barras" in has_cols and "iva" in has_cols:
                conn.execute(
                    "UPDATE producto SET nombre=?, precio=?, stock=?, codigo_barras=?, iva=? WHERE id_producto=?;",
                    (p.nombre, p.precio, p.stock, p.codigo_barras, p.iva, p.id_producto),
                )
            elif "codigo_barras" in has_cols:
                conn.execute(
                    "UPDATE producto SET nombre=?, precio=?, stock=?, codigo_barras=? WHERE id_producto=?;",
                    (p.nombre, p.precio, p.stock, p.codigo_barras, p.id_producto),
                )
            elif "iva" in has_cols:
                conn.execute(
                    "UPDATE producto SET nombre=?, precio=?, stock=?, iva=? WHERE id_producto=?;",
                    (p.nombre, p.precio, p.stock, p.iva, p.id_producto),
                )
            else:
                conn.execute(
                    "UPDATE producto SET nombre=?, precio=?, stock=? WHERE id_producto=?;",
                    (p.nombre, p.precio, p.stock, p.id_producto),
                )

    def eliminar(self, id_producto: int) -> None:
        with self.db.connect() as conn:
            conn.execute("DELETE FROM producto WHERE id_producto=?;", (id_producto,))

    def ajustar_stock(self, id_producto: int, delta: int) -> None:
        with self.db.connect() as conn:
            row = conn.execute(
                "SELECT stock FROM producto WHERE id_producto=?;",
                (id_producto,)
            ).fetchone()
            if not row:
                raise ValueError("Producto no encontrado")
            nuevo = row["stock"] + delta
            if nuevo < 0:
                raise ValueError("Stock insuficiente")
            conn.execute(
                "UPDATE producto SET stock=? WHERE id_producto=?;",
                (nuevo, id_producto)
            )
