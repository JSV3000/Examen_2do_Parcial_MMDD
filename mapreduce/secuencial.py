#!/usr/bin/env python3
import csv
import sys
import time
from datetime import datetime
from collections import defaultdict

DIAS = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]

archivo_csv = sys.argv[1] if len(sys.argv) > 1 else "/data/input/ventas_125052894.csv"

inicio = time.time()
totales = defaultdict(int)

with open(archivo_csv, mode="r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        try:
            if not row or len(row) != 8 or row[0].strip() == "id":
                continue
            dt = datetime.strptime(row[1].strip(), "%Y-%m-%d %H:%M:%S")
            dia_semana = DIAS[dt.weekday()]
            cantidad = int(row[5].strip())
            metodo_pago = row[7].strip()
            totales[f"{metodo_pago}|{dia_semana}"] += cantidad
        except Exception:
            continue

fin = time.time()

for clave in sorted(totales.keys()):
    print(f"{clave}\t{totales[clave]}")

print(f"\n--- Tiempo de ejecucion secuencial: {fin - inicio:.4f} segundos ---", file=sys.stderr)