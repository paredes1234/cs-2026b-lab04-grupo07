"""Matriz de probabilidad e impacto de los riesgos de atam-lite.md.
Uso (desde la raíz del repo):  python fitness/matriz_riesgos.py
Salida: docs/architecture/matriz-riesgos.png
"""
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# id: (probabilidad 1-5, impacto 1-5)  -> ajusten a su criterio y a atam-lite.md
RIESGOS = {
    "R1": (3, 5),   # un endpoint omite el filtro mercado_id
    "R2": (3, 4),   # el proveedor no soporta clave de idempotencia
    "R3": (2, 3),   # la conciliación del worker se atrasa
    "R4": (2, 4),   # un solo VPS (punto único de falla)
    "R5": (3, 2),   # regla de mercado que no es un parámetro
}
CRITICA = 12  # probabilidad x impacto >= 12 -> zona crítica

fig, ax = plt.subplots(figsize=(6.4, 5.6))
for p in range(1, 6):
    for i in range(1, 6):
        v = p * i
        color = "#f4b6b0" if v >= CRITICA else "#fbe3a6" if v >= 6 else "#cfe8cf"
        ax.add_patch(plt.Rectangle((p - .5, i - .5), 1, 1, color=color, ec="white", lw=2))

celdas = defaultdict(list)
for rid, (p, i) in RIESGOS.items():
    celdas[(p, i)].append(rid)
for (p, i), ids in celdas.items():
    ax.text(p, i, "\n".join(ids), ha="center", va="center", fontsize=11, fontweight="bold")

ax.set_xlim(.5, 5.5); ax.set_ylim(.5, 5.5)
ax.set_xticks(range(1, 6)); ax.set_yticks(range(1, 6))
ax.set_xlabel("Probabilidad (1 a 5)"); ax.set_ylabel("Impacto (1 a 5)")
ax.set_title("Matriz de riesgos ATAM-lite: San Camilo en Línea (Lab 08)\nrojo = zona crítica (P x I ≥ 12)", fontsize=10)

# Asegurar el directorio y guardar usando el objeto Path
output_dir = Path("docs/architecture")
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "matriz-riesgos.png"

fig.tight_layout()
fig.savefig(output_path, dpi=160)
print(f"OK: {output_path}")