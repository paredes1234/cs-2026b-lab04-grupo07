"""E6 (Lab 10): humano en el circuito. Un integrante aprueba o rechaza cada edición desde la consola.

Patrones aplicados (Koenigstein, 2026, cap. 2):
  - Aprobar o rechazar: la edición no se ejecuta hasta que la persona responde.
  - Revisar llamadas a herramientas: se muestra la ruta y el fragmento antes/después.
  - Validar la entrada humana: solo se acepta "s" o "n"; otra respuesta se vuelve a pedir y,
    si se agotan los intentos, la edición se rechaza (falla segura).
  - Revisar y editar (parcial): tras decidir, la persona puede dejar una observación que queda en el
    registro (por ejemplo, "aprobada, pero falta una prueba"); no cambia la edición.
"""
import json, time


class AprobadorConsola:
    def __init__(self, entrada=input, salida=print, max_intentos=3, registro=None, responsable="integrante",
                 pedir_observacion=False, origen="consola"):
        self.entrada, self.salida, self.max_intentos = entrada, salida, max_intentos
        self.pedir_observacion = pedir_observacion
        self.origen = origen                # "consola" o el archivo de respuestas transcritas
        self.registro = registro            # ruta .jsonl con cada decisión humana (evidencia para delegacion.md)
        self.responsable = responsable      # rol, no nombre: sin datos personales en las trazas
        self.decisiones = []

    def __call__(self, args: dict) -> bool:
        self.salida(self._resumen(args))
        intentos = []
        for _ in range(self.max_intentos):
            r = self.entrada("¿Aprueba esta edición? (s/n): ")
            intentos.append(r)
            if r == "s" or r == "n":
                obs = self.entrada("Observación (Enter para omitir): ").strip() if self.pedir_observacion else ""
                return self._guardar(args, r == "s", intentos, obs)
            self.salida(f"Respuesta no válida: {r!r}. Escriba solo s o n.")
        self.salida("Sin respuesta válida: la edición se rechaza por seguridad.")
        return self._guardar(args, False, intentos)

    def _resumen(self, args):
        antes, despues = args.get("antes", ""), args.get("despues", "")
        return ("\n===== EDICIÓN PROPUESTA POR EL AGENTE =====\n"
                f"Archivo: {args.get('ruta', '?')}\n"
                "--- antes\n" + "\n".join(f"- {l}" for l in str(antes).splitlines()) + "\n"
                "+++ después\n" + "\n".join(f"+ {l}" for l in str(despues).splitlines()))

    def _guardar(self, args, aprobado, intentos, observacion=""):
        d = {"t": round(time.time(), 3), "responsable": self.responsable, "origen": self.origen,
             "ruta": args.get("ruta"), "aprobado": aprobado, "respuestas": intentos,
             "observacion": observacion or None}
        self.decisiones.append(d)
        if self.registro:
            with open(self.registro, "a", encoding="utf-8") as f:
                f.write(json.dumps(d, ensure_ascii=False) + "\n")
        return aprobado
