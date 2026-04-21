from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash
from db import get_connection
from werkzeug.security import generate_password_hash

usuarios_bp = Blueprint("usuarios", __name__)

# ── POST /api/login ────────────────────────────────────────
@usuarios_bp.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    email    = data.get("email", "")
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Email y contraseña son obligatorios"}), 400

    conn = get_connection()
    if not conn:
        return jsonify({"error": "Sin conexión a la base de datos"}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT u.id, u.nombre, u.email, u.password, r.nombre AS rol
        FROM usuarios u
        JOIN roles r ON u.id_rol = r.id
        WHERE u.email = %s AND u.activo = 1
    """, (email,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()

    if not usuario or not check_password_hash(usuario["password"], password):
        return jsonify({"error": "Credenciales incorrectas"}), 401

    # Guardar en sesión
    session["usuario_id"]  = usuario["id"]
    session["usuario_nombre"] = usuario["nombre"]
    session["rol"]         = usuario["rol"]

    return jsonify({
        "mensaje": "Login exitoso",
        "usuario": {
            "id":     usuario["id"],
            "nombre": usuario["nombre"],
            "email":  usuario["email"],
            "rol":    usuario["rol"]
        }
    }), 200


# ── POST /api/register ────────────────────────────────
@usuarios_bp.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    nombre   = data.get("nombre", "")
    email    = data.get("email", "")
    password = data.get("password", "")

    if not nombre or not email or not password:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    conn = get_connection()
    if not conn:
        return jsonify({"error": "Sin conexión a la base de datos"}), 500

    cursor = conn.cursor(dictionary=True)

    # Verificar si el usuario ya existe
    cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
    existe = cursor.fetchone()

    if existe:
        cursor.close()
        conn.close()
        return jsonify({"error": "El usuario ya existe"}), 400

    # Encriptar contraseña
    password_hash = generate_password_hash(password)

    # Insertar usuario (rol 2 = usuario normal)
    cursor.execute("""
        INSERT INTO usuarios (nombre, email, password, id_rol)
        VALUES (%s, %s, %s, %s)
    """, (nombre, email, password_hash, 2))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Usuario registrado"}), 201



# ── POST /api/logout ───────────────────────────────────────
@usuarios_bp.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"mensaje": "Sesión cerrada"}), 200


# ── GET /api/categorias ────────────────────────────────────
# Las categorías las necesita el frontend para el formulario de producto
@usuarios_bp.route("/api/categorias", methods=["GET"])
def get_categorias():
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Sin conexión a la base de datos"}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre FROM categorias ORDER BY nombre")
    categorias = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(categorias), 200