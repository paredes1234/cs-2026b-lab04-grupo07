"""E4 Lab 08, iteración 2: Monte Carlo de cobros con timeouts del proveedor (QA08-04).

IMPORTANTE: proveedor simulado; no se llama a Yape ni a ninguna pasarela real.
Un timeout puede ser "temprano" (el proveedor no cobró) o "tardío" (cobró, pero
la respuesta se perdió). Solo el tardío produce cobros duplicados al reintentar.

Tácticas comparadas:
  - reintentos:   lo que hace hoy confirmar_y_pagar() (src/despues/servicio.py):
                  reintenta ante ConnectionError sin clave de idempotencia.
  - sin_reintento: ante timeout marca el pedido como fallido y no reintenta.
  - idempotente:  registra el intento como PENDIENTE (outbox), envía una clave
                  de idempotencia (pedido_id) y, tras un timeout, consulta el
                  estado del cobro antes de reintentar.

Reproducir desde la raíz del repositorio:
    python -m fitness.cobros --pedidos 100 --timeouts 10 --semilla 2026
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

TACTICAS = ("reintentos", "sin_reintento", "idempotente")
MAX_INTENTOS = 3


class ProveedorSimulado:
    """Proveedor de pago con timeouts. Guarda cada cargo real que aplica."""

    def __init__(self, rnd: random.Random, p_tardio: float, p_timeout_reintento: float):
        self.rnd = rnd
        self.p_tardio = p_tardio
        self.p_timeout_reintento = p_timeout_reintento
        self.cargos: dict[str, int] = {}          # pedido_id -> cargos aplicados
        self.por_clave: set[str] = set()          # claves de idempotencia ya cobradas

    def cobrar(self, pedido_id: str, intento: int, forzar_timeout: bool,
               clave: str | None = None) -> bool:
        """True si responde; lanza TimeoutError si la respuesta no llega.

        El primer intento falla solo si el escenario lo fuerza (10 de 100);
        los reintentos fallan con probabilidad p_timeout_reintento.
        """
        if intento == 0:
            timeout = forzar_timeout
        else:
            timeout = self.rnd.random() < self.p_timeout_reintento
        if timeout and self.rnd.random() >= self.p_tardio:
            raise TimeoutError("timeout temprano: no se aplicó el cargo")
        if clave is None or clave not in self.por_clave:
            self.cargos[pedido_id] = self.cargos.get(pedido_id, 0) + 1
            if clave is not None:
                self.por_clave.add(clave)
        if timeout:
            raise TimeoutError("timeout tardío: el cargo se aplicó, la respuesta se perdió")
        return True

    def consultar(self, clave: str) -> bool:
        """Supuesto: el proveedor permite consultar un cobro por su referencia."""
        return clave in self.por_clave


def _cobrar_con_reintentos(prov, pedido_id, primer_timeout):
    for intento in range(MAX_INTENTOS):
        try:
            return prov.cobrar(pedido_id, intento, primer_timeout)
        except TimeoutError:
            continue
    return False


def _cobrar_sin_reintento(prov, pedido_id, primer_timeout):
    try:
        return prov.cobrar(pedido_id, 0, primer_timeout)
    except TimeoutError:
        return False


def _cobrar_idempotente(prov, pedido_id, primer_timeout, outbox):
    outbox[pedido_id] = "PENDIENTE"                 # se registra antes de llamar
    for intento in range(MAX_INTENTOS):
        try:
            prov.cobrar(pedido_id, intento, primer_timeout, clave=pedido_id)
            outbox[pedido_id] = "PAGADO"
            return True
        except TimeoutError:
            if prov.consultar(pedido_id):           # verificar antes de reintentar
                outbox[pedido_id] = "PAGADO"
                return True
    return False                                     # queda PENDIENTE para conciliar


def simular(tactica: str, pedidos: int = 100, timeouts: int = 10, semilla: int = 2026,
            p_tardio: float = 0.5, p_timeout_reintento: float = 0.10) -> dict:
    """Lote de pedidos; en `timeouts` de ellos el primer intento no recibe respuesta."""
    if tactica not in TACTICAS:
        raise ValueError(f"Táctica desconocida: {tactica}")
    if not 0 <= timeouts <= pedidos:
        raise ValueError("timeouts debe estar entre 0 y pedidos")
    rnd = random.Random(semilla)
    con_timeout = set(rnd.sample(range(pedidos), timeouts))
    prov = ProveedorSimulado(rnd, p_tardio, p_timeout_reintento)
    outbox: dict[str, str] = {}
    confirmados = 0
    for i in range(pedidos):
        pedido_id = f"PED-{i:03d}"
        if tactica == "reintentos":
            ok = _cobrar_con_reintentos(prov, pedido_id, i in con_timeout)
        elif tactica == "sin_reintento":
            ok = _cobrar_sin_reintento(prov, pedido_id, i in con_timeout)
        else:
            ok = _cobrar_idempotente(prov, pedido_id, i in con_timeout, outbox)
        confirmados += ok
        if not ok:
            outbox.setdefault(pedido_id, "FALLIDO")
    duplicados = sum(n - 1 for n in prov.cargos.values() if n > 1)
    # Cobro huérfano: el cliente pagó, pero el sistema registra el pedido como fallido.
    huerfanos = sum(1 for p, n in prov.cargos.items() if n and outbox.get(p) == "FALLIDO")
    return {
        "tactica": tactica,
        "pedidos": pedidos,
        "timeouts_primer_intento": timeouts,
        "confirmados": confirmados,
        "cobros_duplicados": duplicados,
        "cobros_huerfanos": huerfanos,
        "pendientes_conciliacion": sum(1 for e in outbox.values() if e == "PENDIENTE"),
    }


def montecarlo(tactica: str, corridas: int = 1000, **kwargs) -> dict:
    """Repite la simulación con semillas 0..corridas-1 y resume los duplicados."""
    corridas_r = [simular(tactica, semilla=s, **kwargs) for s in range(corridas)]
    dups = [r["cobros_duplicados"] for r in corridas_r]
    huer = [r["cobros_huerfanos"] for r in corridas_r]
    dups_ord = sorted(dups)
    return {
        "tactica": tactica,
        "corridas": corridas,
        "duplicados_promedio": sum(dups) / corridas,
        "duplicados_p95": dups_ord[int(0.95 * corridas) - 1],
        "duplicados_max": max(dups),
        "corridas_con_duplicados": sum(1 for d in dups if d),
        "huerfanos_promedio": sum(huer) / corridas,
        "pendientes_promedio": sum(r["pendientes_conciliacion"] for r in corridas_r) / corridas,
    }


def sensibilidad(tactica: str, corridas: int = 200) -> list[dict]:
    """Duplicados promedio según la fracción de timeouts tardíos (supuesto clave)."""
    return [
        {"p_tardio": p, **{k: v for k, v in montecarlo(tactica, corridas, p_tardio=p).items()
                          if k in ("duplicados_promedio", "duplicados_max")}}
        for p in (0.0, 0.25, 0.5, 0.75, 1.0)
    ]


def grafico_svg(resumen: list[dict]) -> str:
    """Barras de duplicados promedio por táctica (sin dependencias externas)."""
    ancho, alto, base, escala = 520, 260, 210, 30
    colores = {"reintentos": "#c0392b", "sin_reintento": "#7f8c8d", "idempotente": "#27ae60"}
    partes = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{ancho}" height="{alto}" '
              'font-family="sans-serif" font-size="12">',
              '<rect width="100%" height="100%" fill="white"/>',
              '<text x="260" y="20" text-anchor="middle" font-size="14">'
              'QA08-04: cobros duplicados por lote de 100 pedidos (1000 corridas)</text>',
              f'<line x1="60" y1="{base}" x2="500" y2="{base}" stroke="black"/>']
    for i, r in enumerate(resumen):
        x, h = 90 + i * 140, r["duplicados_promedio"] * escala
        partes += [f'<rect x="{x}" y="{base - h:.1f}" width="80" height="{h:.1f}" '
                   f'fill="{colores[r["tactica"]]}"/>',
                   f'<text x="{x + 40}" y="{base - h - 6:.1f}" text-anchor="middle">'
                   f'{r["duplicados_promedio"]:.2f} (máx {r["duplicados_max"]})</text>',
                   f'<text x="{x + 40}" y="{base + 18}" text-anchor="middle">{r["tactica"]}</text>']
    partes += ['<text x="260" y="250" text-anchor="middle" fill="#555">'
               'Meta QA08-04: 0 duplicados. Supuesto: 50 % de los timeouts son tardíos.</text>',
               '</svg>']
    return "\n".join(partes)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pedidos", type=int, default=100)
    parser.add_argument("--timeouts", type=int, default=10)
    parser.add_argument("--semilla", type=int, default=2026)
    parser.add_argument("--salida", type=Path, default=Path("docs/architecture/add"))
    args = parser.parse_args()

    lote = [simular(t, args.pedidos, args.timeouts, args.semilla) for t in TACTICAS]
    resumen = [montecarlo(t, pedidos=args.pedidos, timeouts=args.timeouts) for t in TACTICAS]
    sens = {t: sensibilidad(t) for t in ("reintentos", "idempotente")}

    for r in lote:
        print(f"{r['tactica']:14s} confirmados={r['confirmados']:3d}  duplicados={r['cobros_duplicados']}  "
              f"huerfanos={r['cobros_huerfanos']}  pendientes={r['pendientes_conciliacion']}")
    for r in resumen:
        print(f"{r['tactica']:14s} 1000 corridas: promedio={r['duplicados_promedio']:.2f}  "
              f"p95={r['duplicados_p95']}  max={r['duplicados_max']}  "
              f"corridas_con_duplicados={r['corridas_con_duplicados']}")

    args.salida.mkdir(parents=True, exist_ok=True)
    (args.salida / "resultados-cobros.json").write_text(
        json.dumps({"semilla": args.semilla, "lote": lote, "montecarlo": resumen,
                    "sensibilidad_p_tardio": sens}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    (args.salida / "cobros.svg").write_text(grafico_svg(resumen) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
