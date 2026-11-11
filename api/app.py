import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify, request
import time

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        database=os.environ.get("POSTGRES_DB", "datamart_db"),
        user=os.environ.get("POSTGRES_USER", "datamart_user"),
        password=os.environ.get("POSTGRES_PASSWORD", "datamart_pass_secret"),
        port=os.environ.get("DB_PORT", "5432")
    )

def init_db():
    while True:
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS resultados_ventas (
                    id SERIAL PRIMARY KEY,
                    metodo_pago VARCHAR(50) NOT NULL,
                    dia_semana VARCHAR(20) NOT NULL,
                    unidades_vendidas BIGINT NOT NULL,
                    UNIQUE(metodo_pago, dia_semana)
                );
            """)
            conn.commit()
            cur.close()
            conn.close()
            print("Base de datos conectada y tabla verificada.")
            break
        except Exception as e:
            print(f"Esperando a que PostgreSQL este listo... ({e})")
            time.sleep(2)
            

@app.route("/resultados", methods=["GET"])
def obtener_resultados():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM resultados_ventas ORDER BY metodo_pago, dia_semana;")
    filas = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(filas), 200

@app.route("/resultados/<clave>", methods=["GET"])
def filtrar_resultados(clave):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        SELECT * FROM resultados_ventas 
        WHERE LOWER(metodo_pago) = LOWER(%s) OR LOWER(dia_semana) = LOWER(%s)
        ORDER BY metodo_pago, dia_semana;
    """, (clave, clave))
    filas = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(filas), 200

@app.route("/resultados", methods=["POST"])
def crear_o_actualizar_resultado():
    data = request.get_json()
    metodo_pago = data.get("metodo_pago")
    dia_semana = data.get("dia_semana")
    unidades = data.get("unidades_vendidas")

    if not metodo_pago or not dia_semana or unidades is None:
        return jsonify({"error": "Faltan campos requeridos (metodo_pago, dia_semana, unidades_vendidas)"}), 400

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        INSERT INTO resultados_ventas (metodo_pago, dia_semana, unidades_vendidas)
        VALUES (%s, %s, %s)
        ON CONFLICT (metodo_pago, dia_semana)
        DO UPDATE SET unidades_vendidas = EXCLUDED.unidades_vendidas
        RETURNING *;
    """, (metodo_pago, dia_semana, int(unidades)))
    nuevo = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(nuevo), 201

@app.route("/resultados/<int:id_registro>", methods=["DELETE"])
def eliminar_resultado(id_registro):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM resultados_ventas WHERE id = %s RETURNING id;", (id_registro,))
    eliminado = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not eliminado:
        return jsonify({"error": "Registro no encontrado"}), 404
    return jsonify({"mensaje": f"Registro {id_registro} eliminado correctamente"}), 200

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)