import sqlite3

from flask import Flask, request, jsonify, session, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "clave-secreta-pfo2"  # necesaria para recordar quién inició sesión
DB_NAME = "usuarios.db"


def conectar():
    return sqlite3.connect(DB_NAME)


def crear_tabla():
    conn = conectar()
    conn.execute(
        """CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL
        )"""
    )
    conn.commit()
    conn.close()


@app.route("/registro", methods=["POST"])
def registro():
    data = request.get_json(silent=True) or {}
    usuario = data.get("usuario")
    contrasena = data.get("contraseña")

    if not usuario or not contrasena:
        return jsonify({"status": "error",
                        "message": "Faltan datos: usuario y contraseña."}), 400

    # se guarda su hash.
    hash_contrasena = generate_password_hash(contrasena)

    conn = conectar()
    try:
        conn.execute(
            "INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)",
            (usuario, hash_contrasena),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"status": "error",
                        "message": "El usuario ya existe."}), 409
    finally:
        conn.close()

    return jsonify({"status": "success", "message": "Usuario registrado."}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    usuario = data.get("usuario")
    contrasena = data.get("contraseña")

    if not usuario or not contrasena:
        return jsonify({"status": "error",
                        "message": "Faltan datos: usuario y contraseña."}), 400

    conn = conectar()
    fila = conn.execute(
        "SELECT contrasena FROM usuarios WHERE usuario = ?", (usuario,)
    ).fetchone()
    conn.close()

    # Se compara la contraseña ingresada contra el hash guardado.
    # El mensaje es el mismo si falla el usuario o la contraseña.
    if fila is None or not check_password_hash(fila[0], contrasena):
        return jsonify({"status": "error",
                        "message": "Usuario o contraseña incorrectos."}), 401

    session["usuario"] = usuario
    return jsonify({"status": "success", "message": f"Bienvenido, {usuario}."})


@app.route("/tareas", methods=["GET"])
def tareas():
    usuario = session.get("usuario")
    if usuario is None:
        return jsonify({"status": "error",
                        "message": "Primero hay que iniciar sesión."}), 401

    return render_template_string(
        """<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><title>Gestión de Tareas</title></head>
<body>
    <h1>¡Bienvenido, {{ usuario }}!</h1>
    <p>Este es tu sistema de gestión de tareas.</p>
</body>
</html>""",
        usuario=usuario,
    )


crear_tabla()

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)