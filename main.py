from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os


app = Flask(__name__, static_folder="static", template_folder=".")


DB_PATH = os.path.join("data", "pos.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn



@app.route("/")
def index():

    return send_from_directory(".", "1_inicio-sesion.html")

@app.route("/<path:filename>")
def serve_file(filename):
    return send_from_directory(".", filename)


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    usuario = data.get("usuario")
    password = data.get("password")

    if not usuario or not password:
        return jsonify({"success": False, "message": "Faltan datos"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuario WHERE correo = ?", (usuario,))
    row = cur.fetchone()
    conn.close()

    if row and row["password"] == password:
        return jsonify({"success": True, "message": "Login exitoso"})
    else:
        return jsonify({"success": False, "message": "Usuario o contraseña incorrectos"}), 401



@app.route("/products.js")
def products_js():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_producto, nombre, precio, iva FROM producto")
    rows = cur.fetchall()
    conn.close()

    productos = []
    for i, r in enumerate(rows, start=1):
        key = f"c{i}"
        productos.append(
            f'"{key}": {{ name: "{r["nombre"]}", price: {r["precio"]}, iva: {r["iva"]} }}'
        )

    js_code = "const products = {\n  " + ",\n  ".join(productos) + "\n};"
    return js_code, 200, {"Content-Type": "application/javascript"}


if __name__ == "__main__":
    app.run(debug=True)
