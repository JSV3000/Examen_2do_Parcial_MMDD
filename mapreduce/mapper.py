#!/usr/bin/env python3
import sys
import csv
from datetime import datetime

DIAS = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]

reader = csv.reader(sys.stdin)

for row in reader:
    try:
        if not row or len(row) != 8:
            continue
        # Ignorar encabezado
        if row[0].strip() == "id":
            continue
        
        fecha_str = row[1].strip()
        cantidad = int(row[5].strip())
        metodo_pago = row[7].strip()
        
        dt = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
        dia_semana = DIAS[dt.weekday()]
        
        print(f"{metodo_pago}|{dia_semana}\t{cantidad}")
    except Exception:
        # Ignorar líneas mal formadas sin truncar el job
        continue