from datetime import datetime
from ..db import Database

class VentaRepo:
    def __init__(self, db: Database):
        self.db = db

    def crear_venta(self, id_cliente: int, id_usuario: int, items, fecha=None) -> int:
        if fecha is None:
            fecha = datetime.now().isoformat(timespec="seconds")

        with self.db.connect() as conn:
            precios = {}
            for (pid, _cant, override) in items:
                if override is not None:
                    precios[pid] = float(override)
                else:
                    row = conn.execute("SELECT precio FROM producto WHERE id_producto=?;", (pid,)).fetchone()
                    if not row:
                        raise ValueError(f"Producto {pid} no existe")
                    precios[pid] = float(row["precio"])

            total = sum(c * precios[pid] for (pid, c, _o) in items)
            cur = conn.execute(
                "INSERT INTO venta(fecha, total, id_cliente, id_usuario) VALUES(?, ?, ?, ?);",
                (fecha, total, id_cliente, id_usuario),
            )
            id_venta = cur.lastrowid

            for (pid, cant, _o) in items:
                precio_unitario = precios[pid]
                conn.execute(
                    "INSERT INTO detalle_venta(id_venta, id_producto, cantidad, precio_unitario) VALUES (?, ?, ?, ?);",
                    (id_venta, pid, cant, precio_unitario),
                )
                row = conn.execute("SELECT stock FROM producto WHERE id_producto=?;", (pid,)).fetchone()
                nuevo = row["stock"] - cant
                if nuevo < 0:
                    raise ValueError(f"Stock insuficiente para producto {pid}")
                conn.execute("UPDATE producto SET stock=? WHERE id_producto=?;", (nuevo, pid))

            return id_venta

    def obtener(self, id_venta: int):
        with self.db.connect() as conn:
            v = conn.execute("SELECT * FROM venta WHERE id_venta=?;", (id_venta,)).fetchone()
            if not v:
                raise ValueError("Venta no encontrada")
            detalles = conn.execute(
                '''
                SELECT d.*, p.nombre AS nombre_producto
                FROM detalle_venta d
                JOIN producto p ON p.id_producto = d.id_producto
                WHERE d.id_venta=?;
                ''',
                (id_venta,)
            ).fetchall()
            return {
                "venta": dict(v),
                "detalles": [dict(r) for r in detalles]
            }

    def listar(self):
        with self.db.connect() as conn:
            rows = conn.execute("SELECT * FROM venta ORDER BY fecha DESC;").fetchall()
            return [dict(r) for r in rows]

    def eliminar(self, id_venta: int):
        with self.db.connect() as conn:
            detalles = conn.execute("SELECT id_producto, cantidad FROM detalle_venta WHERE id_venta=?;", (id_venta,)).fetchall()
            for d in detalles:
                conn.execute(
                    "UPDATE producto SET stock = stock + ? WHERE id_producto=?;",
                    (d["cantidad"], d["id_producto"])
                )
            conn.execute("DELETE FROM venta WHERE id_venta=?;", (id_venta,))
