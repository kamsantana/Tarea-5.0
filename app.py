from flask import Flask
import psycopg2
import os

app = Flask(__name__)
VERSION = "2.0.0"

def obtener_conexion():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        database="empresa",
        user="admin",
        password="admin123"
    )

@app.route("/")
def inicio():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Actividad 3: Crear la tabla si no existe de forma automática
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes(
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100)
            );
        """)
        conexion.commit()

        # Actividad 5: Listar los clientes registrados
        cursor.execute("SELECT id, nombre FROM clientes;")
        clientes = cursor.fetchall()

        # Obtener versión de la BD
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()[0]

        cursor.close()
        conexion.close()

        # Generar lista en HTML
        lista_html = "".join([f"<li>ID: {c[0]} - Nombre: {c[1]}</li>" for c in clientes])
        if not lista_html:
            lista_html = "<li>No hay clientes registrados aún. ¡Insértalos desde pgAdmin!</li>"

        return f"""
        <h1>Aplicación Flask</h1>
        <h2>Versión {VERSION}</h2>
        <p><strong>Conexión exitosa a PostgreSQL</strong></p>
        <p>Version DB: {db_version}</p>
        <hr>
        <h3>Lista de Clientes (Actividad 5):</h3>
        <ul>
            {lista_html}
        </ul>
        """
    except Exception as e:
        return f"<h1>Error de Conexión</h1><p>{str(e)}</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)