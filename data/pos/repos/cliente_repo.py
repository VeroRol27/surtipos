from ..db import Database
from ..models.cliente import Cliente

class ClienteRepo:
    def __init__(self, db: Database):
        self.db = db

    def crear(self, c: Cliente) -> int:
        with self.db.connect() as conn:
            cur = conn.execute(
                "INSERT INTO cliente(nombre, correo, telefono) VALUES (?, ?, ?);",
                (c.nombre, c.correo, c.telefono),
            )
            return cur.lastrowid

    def listar(self):
        with self.db.connect() as conn:
            rows = conn.execute("SELECT * FROM cliente;").fetchall()
            return [Cliente(r["id_cliente"], r["nombre"], r["correo"], r["telefono"]) for r in rows]

    def actualizar(self, c: Cliente) -> None:
        with self.db.connect() as conn:
            conn.execute(
                "UPDATE cliente SET nombre=?, correo=?, telefono=? WHERE id_cliente=?;",
                (c.nombre, c.correo, c.telefono, c.id_cliente),
            )

    def eliminar(self, id_cliente: int) -> None:
        with self.db.connect() as conn:
            conn.execute("DELETE FROM cliente WHERE id_cliente=?;", (id_cliente,))
