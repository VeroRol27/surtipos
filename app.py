from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import sqlite3
import os


BASE_DIR = os.path.dirname(__file__)
FRONTEND_DIR = BASE_DIR  
DB_PATH = os.path.join(BASE_DIR, "database", "pos", "surtipos.db")

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)


@app.route("/")
def index():
    
    return send_from_directory(FRONTEND_DIR, "1_inicio-sesion.html")


@app.route("/<path:filename>")
def serve_file(filename):
    return send_from_directory(FRONTEND_DIR, filename)



if __name__ == "__main__":
    app.run(debug=True)
