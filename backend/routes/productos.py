from flask import Blueprint, request, jsonify
from db import get_connection

productos_bp = Blueprint("productos", __name__)

# ── GET /api/productos ─────────────────────────────────────
# Devuelve todos los productos activos
@productos_bp.route("/api/productos", methods=["GET"])
def get_productos():
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Sin conexión a la base de datos"}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.id, p.nombre, p.descripcion, p.precio, p.stock, p.stock_minimo,
               c.nombre AS categoria
        FROM productos p
        JOIN categorias c ON p.id_categoria = c.id
        WHERE p.activo = 1
        ORDER BY p.nombre
    """)
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(productos), 200


# ── GET /api/productos/<id> ────────────────────────────────
# Devuelve un producto por su id
@productos_bp.route("/api/productos/<int:id>", methods=["GET"])
def get_producto(id):
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Sin conexión a la base de datos"}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.id, p.nombre, p.descripcion, p.precio, p.stock, p.stock_minimo,
               p.id_categoria, c.nombre AS categoria
        FROM productos p
        JOIN categorias c ON p.id_categoria = c.id
        WHERE p.id = %s AND p.activo = 1
    """, (id,))
    producto = cursor.fetchone()
    cursor.close()
    conn.close()

    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify(producto), 200


# ── POST /api/productos ────────────────────────────────────
# Crea un nuevo producto
@productos_bp.route("/api/productos", methods=["POST"])
def crear_producto():
    data = request.get_json()

    # Validación básica de campos obligatorios
    campos = ["nombre", "precio", "stock", "id_categoria"]
    for campo in campos:
        if campo not in data or data[campo] == "":
            return jsonify({"error": f"El campo '{campo}' es obligatorio"}), 400

    conn = get_connection()
    if not conn:
        return jsonify({"error": "Sin conexión a la base de datos"}), 500

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO productos (nombre, descripcion, precio, stock, stock_minimo, id_categoria)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        data["nombre"],
        data.get("descripcion", ""),
        data["precio"],
        data["stock"],
        data.get("stock_minimo", 5),
        data["id_categoria"]
    ))
    conn.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"mensaje": "Producto creado", "id": nuevo_id}), 201


# ── PUT /api/productos/<id> ────────────────────────────────
# Actualiza un producto existente
@productos_bp.route("/api/productos/<int:id>", methods=["PUT"])
def actualizar_producto(id):
    data = request.get_json()

    conn = get_connection()
    if not conn:
        return jsonify({"error": "Sin conexión a la base de datos"}), 500

    cursor = conn.cursor()
    cursor.execute("""
        UPDATE productos
        SET nombre       = %s,
            descripcion  = %s,
            precio       = %s,
            stock        = %s,
            stock_minimo = %s,
            id_categoria = %s
        WHERE id = %s AND activo = 1
    """, (
        data["nombre"],
        data.get("descripcion", ""),
        data["precio"],
        data["stock"],
        data.get("stock_minimo", 5),
        data["id_categoria"],
        id
    ))
    conn.commit()
    filas = cursor.rowcount
    cursor.close()
    conn.close()

    if filas == 0:
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify({"mensaje": "Producto actualizado"}), 200


# ── DELETE /api/productos/<id> ─────────────────────────────
# Borrado suave: solo marca activo = 0, no borra el registro
@productos_bp.route("/api/productos/<int:id>", methods=["DELETE"])
def eliminar_producto(id):
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Sin conexión a la base de datos"}), 500

    cursor = conn.cursor()
    cursor.execute("UPDATE productos SET activo = 0 WHERE id = %s", (id,))
    conn.commit()
    filas = cursor.rowcount
    cursor.close()
    conn.close()

    if filas == 0:
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify({"mensaje": "Producto eliminado"}), 200


# ── GET /api/productos/stock-bajo ─────────────────────────
# Productos con stock <= stock_minimo (usa la vista que creamos en el SQL)
@productos_bp.route("/api/productos/stock-bajo", methods=["GET"])
def stock_bajo():
    conn = get_connection()
    if not conn:
        return jsonify({"error": "Sin conexión a la base de datos"}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vista_stock_bajo")
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultado), 200