from pprint import pprint
from pos.db import Database
from pos.models.usuario import Usuario
from pos.models.cliente import Cliente
from pos.models.producto import Producto
from pos.repos.usuario_repo import UsuarioRepo
from pos.repos.cliente_repo import ClienteRepo
from pos.repos.producto_repo import ProductoRepo
from pos.repos.venta_repo import VentaRepo

def ask_int(msg):
    while True:
        try:
            return int(input(msg).strip())
        except ValueError:
            print("Ingrese un número válido.")

def ask_float(msg):
    while True:
        try:
            return float(input(msg).strip())
        except ValueError:
            print("Ingrese un número (puede ser decimal).")

def dump(title, rows):
    print(f"\n=== {title} ===")
    if not rows:
        print("(sin registros)")
        return
    pprint([vars(r) for r in rows])



def menu_usuarios(repo: UsuarioRepo):
    while True:
        print("\n--- USUARIOS ---")
        print("1) Listar")
        print("2) Insertar")
        print("3) Actualizar")
        print("4) Eliminar")
        print("0) Volver")
        op = input("> ").strip()

        if op == "1":
            dump("Usuarios", repo.listar())
        elif op == "2":
            nombre = input("Nombre: ").strip()
            correo = input("Correo (único): ").strip()
            rol = input("Rol: ").strip()
            try:
                new_id = repo.crear(Usuario(None, nombre, correo, rol))
                print(f"Insertado con id {new_id}")

            except Exception as e:
                print("Error al insertar:", e)
        elif op == "3":
            dump("Usuarios (para elegir)", repo.listar())
            uid = ask_int("ID de usuario a actualizar: ")
            nombre = input("Nuevo nombre: ").strip()
            correo = input("Nuevo correo: ").strip()
            rol = input("Nuevo rol: ").strip()
            password = input("Nueva contraseña: ").strip()
            try:
                repo.actualizar(Usuario(uid, nombre, correo, rol, password))
                print("Actualizado.")

            except Exception as e:
                print("Error al actualizar:", e)
        elif op == "4":
            dump("Usuarios (para elegir)", repo.listar())
            uid = ask_int("ID de usuario a eliminar: ")
            try:
                repo.eliminar(uid)
                print("Eliminado.")
            except Exception as e:
                print("Error al eliminar:", e)
        elif op == "0":
            return
        else:
            print("Opción inválida.")

def menu_clientes(repo: ClienteRepo):
    while True:
        print("\n--- CLIENTES ---")
        print("1) Listar")
        print("2) Insertar")
        print("3) Actualizar")
        print("4) Eliminar")
        print("0) Volver")
        op = input("> ").strip()

        if op == "1":
            dump("Clientes", repo.listar())
        elif op == "2":
            nombre = input("Nombre: ").strip()
            correo = input("Correo (único): ").strip()
            telefono = input("Teléfono: ").strip()
            try:
                new_id = repo.crear(Cliente(None, nombre, correo, telefono))
                print(f"Insertado con id {new_id}")
            except Exception as e:
                print("Error al insertar:", e)
        elif op == "3":
            dump("Clientes (para elegir)", repo.listar())
            cid = ask_int("ID de cliente a actualizar: ")
            nombre = input("Nuevo nombre: ").strip()
            correo = input("Nuevo correo: ").strip()
            telefono = input("Nuevo teléfono: ").strip()
            try:
                repo.actualizar(Cliente(cid, nombre, correo, telefono))
                print("Actualizado.")
            except Exception as e:
                print("Error al actualizar:", e)
        elif op == "4":
            dump("Clientes (para elegir)", repo.listar())
            cid = ask_int("ID de cliente a eliminar: ")
            try:
                repo.eliminar(cid)
                print("Eliminado.")
            except Exception as e:
                print("Error al eliminar:", e)
        elif op == "0":
            return
        else:
            print("Opción inválida.")

def menu_productos(repo: ProductoRepo):
    while True:
        print("\n--- PRODUCTOS ---")
        print("1) Listar")
        print("2) Insertar")
        print("3) Actualizar")
        print("4) Eliminar")
        print("5) Ajustar stock (+/-)")
        print("0) Volver")
        op = input("> ").strip()

        if op == "1":
            dump("Productos", repo.listar())

        elif op == "2":
            nombre = input("Nombre: ").strip()
            precio = ask_float("Precio: ")
            stock = ask_int("Stock: ")
            codigo_barras = input("Código de barras (opcional, Enter para NULL): ").strip()
            iva = ask_float("IVA (porcentaje, ej. 0 o 19): ")
            if codigo_barras == "":
                codigo_barras = None
            try:
                new_id = repo.crear(Producto(None, nombre, precio, stock, codigo_barras, iva))
                print(f"Insertado con id {new_id}")
            except Exception as e:
                print("Error al insertar:", e)

        elif op == "3":
            dump("Productos (para elegir)", repo.listar())
            pid = ask_int("ID de producto a actualizar: ")
            nombre = input("Nuevo nombre: ").strip()
            precio = ask_float("Nuevo precio: ")
            stock = ask_int("Nuevo stock: ")
            codigo_barras = input("Nuevo código de barras (opcional, Enter para NULL): ").strip()
            iva = ask_float("Nuevo IVA (porcentaje, ej. 0 o 19): ")
            if codigo_barras == "":
                codigo_barras = None
            try:
                repo.actualizar(Producto(pid, nombre, precio, stock, codigo_barras, iva))
                print("Actualizado.")
            except Exception as e:
                print("Error al actualizar:", e)

        elif op == "4":
            dump("Productos (para elegir)", repo.listar())
            pid = ask_int("ID de producto a eliminar: ")
            try:
                repo.eliminar(pid)
                print("Eliminado.")
            except Exception as e:
                print("Error al eliminar:", e)

        elif op == "5":
            dump("Productos (para elegir)", repo.listar())
            pid = ask_int("ID de producto: ")
            delta = ask_int("Cantidad a sumar/restar (ej. -3 o 5): ")
            try:
                repo.ajustar_stock(pid, delta)
                print("Stock ajustado.")
            except Exception as e:
                print("Error al ajustar stock:", e)

        elif op == "0":
            return
        else:
            print("Opción inválida.")

def seed_data(usuario_repo, cliente_repo, producto_repo):
    if not usuario_repo.listar():
        usuarios = [
            Usuario(None, "Yiced", "Yiced@gmail.com", "administrador", "123" ),
            Usuario(None, "Julian", "Julian@gmail.com", "administrador", "123"),
            Usuario(None, "Carlos", "Carlos@gmail.com", "administrador", "123"),
            Usuario(None, "Gerente1", "empleado1@gmail.com", "gerente", "123"),
            Usuario(None, "Cajero1", "cajero1@gmail.com", "cajero", "123")
        ]
        for u in usuarios:
            usuario_repo.crear(u)

    if not cliente_repo.listar():
        clientes = [
            Cliente(None, "Juan Pérez", "juan@gmail.com", "123456789"),
            Cliente(None, "María López", "maria@gmail.com", "987654321"),
            Cliente(None, "Carlos Díaz", "carlos@gmail.com", "555555555"),
        ]
        for c in clientes:
            cliente_repo.crear(c)

    if not producto_repo.listar():
        productos = [
            Producto(None, "Arroz Blanco Diana 500g", 2200, 30, "7324234234", 0),
            Producto(None, "Enjuague Bucal LISTERINE 500ml", 34500, 15, None, 19)

        ]
        for p in productos:
            producto_repo.crear(p)


def main():
    db = Database("pos.db")
    db.init_schema()

    usuario_repo = UsuarioRepo(db)
    cliente_repo = ClienteRepo(db)
    producto_repo = ProductoRepo(db)
    venta_repo = VentaRepo(db)

    # seed default data if empty
    seed_data(usuario_repo, cliente_repo, producto_repo)

    while True:
        print("\n====== MENÚ SurtiPOS ======")
        print("1) Usuarios")
        print("2) Clientes")
        print("3) Productos")
       
        print("0) Salir")
        op = input("> ").strip()

        if op == "1":
            menu_usuarios(usuario_repo)
        elif op == "2":
            menu_clientes(cliente_repo)
        elif op == "3":
            menu_productos(producto_repo)
        elif op == "0":
            print("Hasta luego.")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
