#!/usr/bin/env python3
import sys

current_key = None
current_sum = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        key, val = line.split("\t", 1)
        unidades = int(val)
    except ValueError:
        continue

    if current_key == key:
        current_sum += unidades
    else:
        if current_key is not None:
            print(f"{current_key}\t{current_sum}")
        current_key = key
        current_sum = unidades

if current_key is not None:
    print(f"{current_key}\t{current_sum}")