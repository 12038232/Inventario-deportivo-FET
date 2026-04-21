from werkzeug.security import generate_password_hash
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="inventario_deportivo"
)

cursor = conn.cursor()

password_plano = "admin123"
password_hash = generate_password_hash(password_plano)

cursor.execute("""
INSERT INTO usuarios (nombre, email, password, id_rol, activo)
VALUES (%s, %s, %s, %s, %s)
""", ("Admin", "admin@admin.com", password_hash, 1, 1))

conn.commit()
conn.close()

print("✅ Admin creado")