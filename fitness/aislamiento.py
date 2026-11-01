"""E2 Lab 08: prototipo cuantitativo de aislamiento entre mercados.

IMPORTANTE: no es una prueba de la API ni de la base de datos de producción.
Se emplean registros sintéticos en SQLite :memory: para comparar una lectura
sin alcance de mercado frente a otra con alcance del mercado autenticado.

Reproducir desde la raíz del repositorio:
    python -m fitness.aislamiento --intentos 100 --semilla 2026
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import sqlite3
from pathlib import Path

MERCADOS = ("SAN_CAMILO", "ALTIPLANO", "RIO_SECO")
PEDIDOS_SINTETICOS = tuple(
    (f"{prefijo}-{numero:03d}", mercado, f"Pedido sintético {numero}")
    for mercado, prefijo in (
        ("SAN_CAMILO", "SC"), ("ALTIPLANO", "AL"), ("RIO_SECO", "RS")
    )
    for numero in range(1, 5)
)


def crear_bd_sintetica() -> sqlite3.Connection:
    """Base temporal sin datos reales de clientes o comerciantes."""
    conn = sqlite3.connect(":memory:")
    conn.execute("""
        CREATE TABLE pedidos (
            id TEXT PRIMARY KEY,
            mercado_id TEXT NOT NULL,
            descripcion TEXT NOT NULL
        )
    """)
    conn.executemany(
        "INSERT INTO pedidos (id, mercado_id, descripcion) VALUES (?, ?, ?)",
        PEDIDOS_SINTETICOS,
    )
    conn.commit()
    return conn


def consulta_antes(conn: sqlite3.Connection, pedido_id: str, mercado_solicitante: str):
    """Ejemplo deliberadamente vulnerable: ignora el mercado solicitante."""
    return conn.execute(
        "SELECT id, mercado_id, descripcion FROM pedidos WHERE id = ?",
        (pedido_id,),
    ).fetchone()


def consulta_despues(conn: sqlite3.Connection, pedido_id: str, mercado_solicitante: str):
    """Lectura limitada al mercado de la sesión autenticada (supuesto del prototipo)."""
    return conn.execute(
        "SELECT id, mercado_id, descripcion FROM pedidos "
        "WHERE id = ? AND mercado_id = ?",
        (pedido_id, mercado_solicitante),
    ).fetchone()


def ejecutar_escenario(intentos: int = 100, semilla: int = 2026) -> tuple[dict, list[dict]]:
    """Mide cuántos registros de otros mercados quedan expuestos.

    Cada intento usa un pedido que existe, pero pertenece a un mercado distinto
    del solicitante. El resultado es reproducible mediante la semilla fija.
    """
    if intentos <= 0:
        raise ValueError("El número de intentos debe ser mayor que cero")

    aleatorio = random.Random(semilla)
    ids_por_mercado = {
        mercado: [pedido[0] for pedido in PEDIDOS_SINTETICOS if pedido[1] == mercado]
        for mercado in MERCADOS
    }
    conn = crear_bd_sintetica()
    filas = []
    expuestos_antes = 0
    expuestos_despues = 0
    for indice in range(1, intentos + 1):
        mercado_solicitante = aleatorio.choice(MERCADOS)
        mercado_objetivo = aleatorio.choice(
            [m for m in MERCADOS if m != mercado_solicitante]
        )
        pedido_id = aleatorio.choice(ids_por_mercado[mercado_objetivo])
        previo = consulta_antes(conn, pedido_id, mercado_solicitante)
        posterior = consulta_despues(conn, pedido_id, mercado_solicitante)
        expuesto_antes = int(previo is not None and previo[1] != mercado_solicitante)
        expuesto_despues = int(posterior is not None and posterior[1] != mercado_solicitante)
        expuestos_antes += expuesto_antes
        expuestos_despues += expuesto_despues
        filas.append({
            "intento": indice,
            "mercado_solicitante": mercado_solicitante,
            "mercado_del_pedido": mercado_objetivo,
            "pedido_id_sintetico": pedido_id,
            "expuesto_antes": expuesto_antes,
            "expuesto_despues": expuesto_despues,
        })

    # Control positivo: la solución no debe denegar pedidos del propio mercado.
    accesos_legitimos = 0
    accesos_legitimos_aprobados = 0
    for pedido_id, mercado, _ in PEDIDOS_SINTETICOS:
        accesos_legitimos += 1
        if consulta_despues(conn, pedido_id, mercado) is not None:
            accesos_legitimos_aprobados += 1
    conn.close()
    resumen = {
        "escenario": "QA08-05",
        "medida": "Registros de otro mercado expuestos en 100 intentos cruzados",
        "intentos_cruzados": intentos,
        "semilla": semilla,
        "mercados": list(MERCADOS),
        "pedidos_sinteticos": len(PEDIDOS_SINTETICOS),
        "expuestos_antes": expuestos_antes,
        "expuestos_despues": expuestos_despues,
        "accesos_legitimos": accesos_legitimos,
        "accesos_legitimos_aprobados": accesos_legitimos_aprobados,
        "objetivo_cumplido_en_prototipo": expuestos_despues == 0 and intentos >= 100,
        "alcance": "Prototipo SQLite en memoria; NO validación de seguridad en producción",
    }
    return resumen, filas


def escribir_evidencias(resumen: dict, filas: list[dict], carpeta: Path) -> None:
    carpeta.mkdir(parents=True, exist_ok=True)
    (carpeta / "resultados-aislamiento.json").write_text(
        json.dumps(resumen, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    with (carpeta / "intentos-aislamiento.csv").open(
        "w", newline="", encoding="utf-8"
    ) as archivo:
        writer = csv.DictWriter(archivo, fieldnames=list(filas[0]))
        writer.writeheader()
        writer.writerows(filas)

    # SVG vectorial sin dependencias: se abre en navegador, Inkscape o LibreOffice.
    total = resumen["intentos_cruzados"]
    antes = resumen["expuestos_antes"]
    despues = resumen["expuestos_despues"]
    ancho_antes = 540 * antes / total
    ancho_despues = 540 * despues / total
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="980" height="330" viewBox="0 0 980 330">
      <rect width="980" height="330" fill="white"/>
      <text x="36" y="48" font-family="sans-serif" font-size="25" font-weight="bold" fill="#222">QA08-05 · Aislamiento entre mercados</text>
      <text x="36" y="78" font-family="sans-serif" font-size="15" fill="#555">Registros ajenos expuestos en {total} intentos de acceso cruzado (prototipo sintético)</text>
      <line x1="258" y1="265" x2="805" y2="265" stroke="#999" stroke-width="2"/>
      <text x="36" y="135" font-family="sans-serif" font-size="19" fill="#222">Antes (sin filtro)</text>
      <rect x="258" y="103" width="{ancho_antes:.1f}" height="50" rx="5" fill="#c35a53"/>
      <text x="{270 + ancho_antes:.1f}" y="135" font-family="sans-serif" font-size="21" font-weight="bold" fill="#333">{antes}</text>
      <text x="36" y="224" font-family="sans-serif" font-size="19" fill="#222">Después (con filtro)</text>
      <rect x="258" y="192" width="{ancho_despues:.1f}" height="50" rx="5" fill="#398872"/>
      <line x1="258" y1="191" x2="258" y2="243" stroke="#398872" stroke-width="3"/>
      <text x="273" y="224" font-family="sans-serif" font-size="21" font-weight="bold" fill="#333">{despues}</text>
      <text x="258" y="294" font-family="sans-serif" font-size="13" fill="#555">0</text>
      <text x="785" y="294" font-family="sans-serif" font-size="13" fill="#555">{total}</text>
      <text x="36" y="317" font-family="sans-serif" font-size="12" fill="#666">Solo demuestra la consulta simulada; no prueba seguridad de API ni controles reales de sesión.</text>
    </svg>'''
    (carpeta / "aislamiento.svg").write_text(svg + "\n", encoding="utf-8")

    # PNG opcional para pegar directamente en informes, si matplotlib está instalado.
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return
    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.barh(["Antes: sin filtro", "Después: con filtro"], [antes, despues])
    ax.set_xlim(0, max(total, 1) * 1.15)
    ax.set_xlabel(f"Registros ajenos expuestos ({total} intentos)")
    ax.set_title("QA08-05 · Accesos cruzados entre mercados · prototipo")
    ax.invert_yaxis()
    for pos, numero in enumerate((antes, despues)):
        ax.text(numero + 1, pos, str(numero), va="center")
    fig.tight_layout()
    fig.savefig(carpeta / "aislamiento.png", dpi=160)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="QA08-05: aislamiento entre mercados")
    parser.add_argument("--intentos", type=int, default=100)
    parser.add_argument("--semilla", type=int, default=2026)
    parser.add_argument("--salida", type=Path, default=Path("docs/architecture/add"))
    argumentos = parser.parse_args()
    resumen, filas = ejecutar_escenario(argumentos.intentos, argumentos.semilla)
    escribir_evidencias(resumen, filas, argumentos.salida)
    print("=== LAB 08 E2: QA08-05, 3 mercados ===")
    print(f"Intentos cruzados: {resumen['intentos_cruzados']}")
    print(f"Antes (sin alcance de mercado): {resumen['expuestos_antes']} registros expuestos")
    print(f"Después (filtrado por mercado): {resumen['expuestos_despues']} registros expuestos")
    print(f"Accesos legítimos admitidos: {resumen['accesos_legitimos_aprobados']}/{resumen['accesos_legitimos']}")
    print("Cumple QA08-05 en el prototipo:" , "SÍ" if resumen["objetivo_cumplido_en_prototipo"] else "NO")
    print(f"Evidencias guardadas en: {argumentos.salida}")
    if resumen["intentos_cruzados"] != 100:
        print("Aviso: el árbol E1 exige exactamente 100 intentos; esta ejecución es complementaria")


if __name__ == "__main__":
    main()
