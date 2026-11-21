"""El 'cerebro' del agente es intercambiable (patrón Strategy del Lab 07).

Protocolo: el modelo recibe el historial y devuelve un JSON con
  {"pensamiento": "...", "accion": "<herramienta>", "args": {...}}   o
  {"pensamiento": "...", "final": "<respuesta para el usuario>"}
"""
import json, os


class ModeloGrabado:
    """Reproduce decisiones grabadas de un asistente de IA (trayectoria JSON).
    Las herramientas se ejecutan de verdad; solo las decisiones vienen de la grabación."""
    def __init__(self, archivo):
        self._decisiones = json.load(open(archivo, encoding="utf-8"))
        self._i = 0

    def decidir(self, historial: list) -> dict:
        d = self._decisiones[self._i]
        self._i += 1
        return d


class ModeloAnthropic:
    """Proveedor real (opcional). Requiere ANTHROPIC_API_KEY y el paquete anthropic."""
    def __init__(self, modelo="claude-sonnet-4-5", sistema=""):
        import anthropic
        self._cliente, self._modelo, self._sistema = anthropic.Anthropic(), modelo, sistema

    def decidir(self, historial: list) -> dict:
        r = self._cliente.messages.create(model=self._modelo, max_tokens=1024, system=self._sistema,
                                          messages=historial, temperature=0)
        return json.loads(r.content[0].text)


class ModeloInteractivo:
    """Permite operar el agente paso a paso ingresando cada decisión JSON por consola."""
    def __init__(self, archivo: str = "trayectorias/issue_01.json"):
        os.makedirs(os.path.dirname(archivo) or ".", exist_ok=True)
        self._archivo = archivo
        self._decisiones = []

    def decidir(self, historial: list) -> dict:
        print("\n===== CONTEXTO PARA EL ASISTENTE =====")
        for mensaje in historial:
            print(f"\n{mensaje['role'].upper()}:")
            print(mensaje["content"])

        print("\n===== PEGUE LA RESPUESTA JSON =====")
        d = json.loads(input("> "))

        self._decisiones.append(d)

        with open(self._archivo, "w", encoding="utf-8") as f:
            json.dump(
                self._decisiones,
                f,
                ensure_ascii=False,
                indent=1
            )

        return d