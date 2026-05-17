from flask import Flask, request, redirect, render_template_string, g
import sqlite3
import os

app = Flask(__name__)
DB_NAME = "database.db"

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_NAME)
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS registros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL
            )
        """)
        conn.commit()

@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM registros")
    datos = cursor.fetchall()
    html = """
    <h1>Reto 9: Conexión SGBD</h1>
    <form action="/add" method="POST">
        <input type="text" name="contenido" placeholder="Escribe algo..." required>
        <button type="submit">Guardar en BD</button>
    </form>
    <h2>Datos en la Base de Datos:</h2>
    <ul>
        {% for d in datos %}
            <li>{{ d[1] }}</li>
        {% endfor %}
    </ul>
    """
    return render_template_string(html, datos=datos)

@app.route('/add', methods=['POST'])
def add():
    contenido = request.form.get("contenido")
    if contenido:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO registros (contenido) VALUES (?)", (contenido,))
        conn.commit()
    return redirect('/')

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)