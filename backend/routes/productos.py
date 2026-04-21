from flask import Blueprint, request, jsonify
from db import get_connection

productos_bp = Blueprint('productos', __name__)

# 🔍 Obtener productos
@productos_bp.route('/', methods=['GET'])
def obtener_productos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM productos")
    data = cursor.fetchall()

    conn.close()
    return jsonify(data)

# ➕ Crear producto
@productos_bp.route('/', methods=['POST'])
def crear_producto():
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO productos (nombre_producto, descripcion, stock, precio, id_categoria)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        data['nombre'],
        data['descripcion'],
        data['stock'],
        data['precio'],
        data['categoria']
    ))

    conn.commit()
    conn.close()

    return jsonify({"mensaje": "Producto creado"})