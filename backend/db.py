import mysql.connector
from mysql.connector import Error

# Cambia estos datos por los de tu MySQL Workbench
DB_CONFIG = {
    "host":     "127.0.0.1:3306",
    "user":     "root",
    "password": "1234",
    "database": "inventario_deportivo_FET_Database"
}

def get_connection():
    """Retorna una conexión activa a la base de datos."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error conectando a MySQL: {e}")
        return None