from flask import Flask
from routes.productos import productos_bp
from routes.usuarios import usuarios_bp

app = Flask(__name__)

# Registrar rutas
app.register_blueprint(productos_bp, url_prefix="/api/productos")
app.register_blueprint(usuarios_bp, url_prefix="/api/usuarios")

if __name__ == '__main__':
    app.run(debug=True)