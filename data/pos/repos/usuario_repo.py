from ..db import Database
from ..models.usuario import Usuario

class UsuarioRepo:
    def __init__(self, db: Database):
        self.db = db

    def crear(self, u: Usuario) -> int:
        with self.db.connect() as conn:
            cur = conn.execute(
                "INSERT INTO usuario(nombre, correo, rol, password) VALUES (?, ?, ?, ?);",
                (u.nombre, u.correo, u.rol, u.password),
            )
            return cur.lastrowid

    def listar(self):
        with self.db.connect() as conn:
            rows = conn.execute("SELECT * FROM usuario;").fetchall()
            return [
                Usuario(
                    r["id_usuario"],
                    r["nombre"],
                    r["correo"],
                    r["rol"],
                    r["password"]
                )
                for r in rows
            ]

    def actualizar(self, u: Usuario) -> None:
        with self.db.connect() as conn:
            conn.execute(
                "UPDATE usuario SET nombre=?, correo=?, rol=?, password=? WHERE id_usuario=?;",
                (u.nombre, u.correo, u.rol, u.password, u.id_usuario),
            )

    def eliminar(self, id_usuario: int) -> None:
        with self.db.connect() as conn:
            conn.execute("DELETE FROM usuario WHERE id_usuario=?;", (id_usuario,))
