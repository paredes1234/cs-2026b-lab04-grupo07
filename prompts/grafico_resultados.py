"""E8 (Lab 09): gráfico de tasas de aprobación por versión, leído de los reportes de promptfoo.

Uso (desde la raíz):  python prompts/grafico_resultados.py
Escribe prompts/resultados.png. Requiere Pillow.
"""
import json
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).resolve().parent
TAREAS = {"Tarea A · criterios": RAIZ / "criterios" / "resultados.json",
          "Tarea B · normalización": RAIZ / "normalizacion" / "resultados.json"}
COLORES = {"v1": (192, 57, 43), "v2": (230, 126, 34), "v3": (39, 174, 96)}
META = 85


def tasas(ruta):
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    r = datos.get("results", datos)
    filas = r.get("results", r) if isinstance(r, dict) else r
    por = defaultdict(list)
    for f in filas:
        por[((f.get("prompt") or {}).get("label") or "").partition(":")[0]].append(bool(f.get("success")))
    return {v: (sum(x), len(x)) for v, x in sorted(por.items())}


def fuente(tam, negrita=False):
    for nombre in (("segoeuib.ttf" if negrita else "segoeui.ttf"),
                   ("DejaVuSans-Bold.ttf" if negrita else "DejaVuSans.ttf")):
        try:
            return ImageFont.truetype(nombre, tam)
        except OSError:
            continue
    return ImageFont.load_default()


def main():
    W, H, izq, base, arriba = 820, 440, 70, 360, 70
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    f, fb = fuente(15), fuente(17, True)
    d.text((W / 2, 24), "Tasa de aprobación por versión del prompt (promptfoo, respuestas grabadas)",
           font=fb, fill="black", anchor="mm")
    esc = (base - arriba) / 100
    for k in range(0, 101, 20):
        y = base - k * esc
        d.line([izq, y, W - 30, y], fill=(225, 225, 225))
        d.text((izq - 8, y), f"{k} %", font=f, fill="black", anchor="rm")
    y_meta = base - META * esc
    for x in range(izq, W - 30, 12):
        d.line([x, y_meta, x + 6, y_meta], fill=(200, 0, 0), width=2)
    d.text((izq + 6, y_meta - 12), f"meta {META} %", font=f, fill=(200, 0, 0), anchor="lm")
    ancho_grupo = (W - 30 - izq) / len(TAREAS)
    for g, (tarea, ruta) in enumerate(TAREAS.items()):
        t = tasas(ruta)
        x0 = izq + g * ancho_grupo + 40
        barra = (ancho_grupo - 80) / len(t)
        for i, (v, (ok, n)) in enumerate(t.items()):
            tasa = 100 * ok / n
            xa, xb = x0 + i * barra + 8, x0 + (i + 1) * barra - 8
            d.rectangle([xa, base - tasa * esc, xb, base], fill=COLORES.get(v, (120, 120, 120)))
            d.text(((xa + xb) / 2, base - tasa * esc - 12), f"{ok}/{n}", font=fb, fill="black", anchor="mm")
            d.text(((xa + xb) / 2, base + 14), v, font=f, fill="black", anchor="mm")
        d.text((x0 + (ancho_grupo - 80) / 2, base + 40), tarea, font=fb, fill="black", anchor="mm")
    d.line([izq, base, W - 30, base], fill="black", width=2)
    img.save(RAIZ / "resultados.png")
    print(RAIZ / "resultados.png")


if __name__ == "__main__":
    main()
