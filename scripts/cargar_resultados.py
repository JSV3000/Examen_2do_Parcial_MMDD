import os
import sys
import psycopg2

RUTA_ARCHIVO = sys.argv[1] if len(sys.argv) > 1 else "/data/output/resultado/part-00000"

def cargar():
    if not os.path.exists(RUTA_ARCHIVO):
        print(f"Error: No se encontro el archivo {RUTA_ARCHIVO}")
        sys.exit(1)

    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        database=os.environ.get("POSTGRES_DB", "datamart_db"),
        user=os.environ.get("POSTGRES_USER", "datamart_user"),
        password=os.environ.get("POSTGRES_PASSWORD", "datamart_pass_secret"),
        port=os.environ.get("DB_PORT", "5432")
    )
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

    insertados = 0
    with open(RUTA_ARCHIVO, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            clave, valor = line.split("\t")
            metodo_pago, dia_semana = clave.split("|")
            unidades = int(valor)

            cur.execute("""
                INSERT INTO resultados_ventas (metodo_pago, dia_semana, unidades_vendidas)
                VALUES (%s, %s, %s)
                ON CONFLICT (metodo_pago, dia_semana)
                DO UPDATE SET unidades_vendidas = EXCLUDED.unidades_vendidas;
            """, (metodo_pago, dia_semana, unidades))
            insertados += 1

    conn.commit()
    cur.close()
    conn.close()
    print(f"Carga exitosa: {insertados} registros insertados/actualizados en la base de datos.")

if __name__ == "__main__":
    cargar()