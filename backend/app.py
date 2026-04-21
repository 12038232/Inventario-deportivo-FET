from flask import Flask
from flask_cors import CORS
from routes.productos import productos_bp
from routes.usuarios  import usuarios_bp

app = Flask(__name__)
app.secret_key = "inventario_deportivo_2024"   # cambia esto en producción

# Permite que el frontend (otro puerto) se comunique con el backend
CORS(app, supports_credentials=True)

# Registrar rutas
app.register_blueprint(productos_bp)
app.register_blueprint(usuarios_bp)

# Ruta de prueba para verificar que el servidor funciona
@app.route("/")
def index():
    return {"mensaje": "API Inventario Deportivo funcionando ✓"}

if __name__ == "__main__":
    app.run(debug=True, port=5000)