"""Herramientas del agente. Cada una es una función pequeña, con descripción y parámetros explícitos.
Todas operan DENTRO del directorio de trabajo (sandbox).

E4 (Lab 10): se agregan mapa_repo() (estructura y firmas con ast) y una memoria de notas
(anotar / leer_notas) que se guarda en notas.md dentro del sandbox.
"""
import ast, os, pathlib, subprocess, re

MAX_NOTA = 300          # caracteres por nota: la pizarra debe ser breve
MAX_NOTAS = 20          # notas por tarea: evita que la memoria crezca sin control
# Salida de subprocesos en UTF-8: en Windows, sin esto, la decodificación depende de la configuración regional
# y un acento en la salida de pytest rompe la herramienta (UnicodeDecodeError) en lugar de dar una observación.
_TEXTO = {"capture_output": True, "text": True, "encoding": "utf-8", "errors": "replace",
          "env": {**os.environ, "PYTHONIOENCODING": "utf-8"}}


class Herramientas:
    def __init__(self, raiz: str, original: str | None = None, notas: str = "notas.md"):
        self.raiz = pathlib.Path(raiz).resolve()
        # La versión original para ver_cambios la fija el programa, no el modelo (mínimo privilegio).
        self.original = pathlib.Path(original).resolve() if original else (self.raiz / "../trabajo_original").resolve()
        self.archivo_notas = self._ruta(notas)

    # --- utilidades ---
    def _ruta(self, ruta: str) -> pathlib.Path:
        p = (self.raiz / ruta).resolve()
        if self.raiz not in p.parents and p != self.raiz:
            raise PermissionError(f"Ruta fuera del sandbox: {ruta}")
        return p

    def catalogo(self) -> dict:
        """Descripción de las herramientas que se envía al modelo (como en un MCP server)."""
        return {
            "listar_archivos": "listar_archivos(carpeta='.'): lista los archivos .py y .md",
            "leer_archivo": "leer_archivo(ruta): devuelve el contenido con números de línea",
            "buscar": "buscar(patron): busca una expresión regular en los archivos .py",
            "ejecutar_pruebas": "ejecutar_pruebas(): ejecuta pytest y devuelve el resumen",
            "editar_archivo": "editar_archivo(ruta, antes, despues): reemplaza un fragmento exacto (una sola vez)",
            "ver_cambios": "ver_cambios(): muestra el diff respecto de la versión original",
            "ejecutar_comando": "ejecutar_comando(comando): ejecuta un comando de shell (sujeto a la política)",
            "mapa_repo": ("mapa_repo(carpeta='src'): devuelve, por archivo .py de la carpeta, las clases y "
                          "funciones con su línea y su firma (parámetros, tipos y retorno), sin el cuerpo. "
                          "Úsela antes de leer archivos completos. Solo lectura."),
            "anotar": (f"anotar(texto): guarda una nota breve (máx. {MAX_NOTA} caracteres) en notas.md: "
                       "hipótesis, archivos revisados o lo que falta. Devuelve el número de la nota."),
            "leer_notas": "leer_notas(): devuelve las notas guardadas en notas.md durante esta tarea. Solo lectura.",
        }

    # --- herramientas ---
    def listar_archivos(self, carpeta="."):
        base = self._ruta(carpeta)
        return "\n".join(sorted(str(p.relative_to(self.raiz)) for p in base.rglob("*")
                                if p.suffix in (".py", ".md") and "__pycache__" not in p.parts))

    def leer_archivo(self, ruta):
        lineas = self._ruta(ruta).read_text(encoding="utf-8").splitlines()
        return "\n".join(f"{i:3d}| {l}" for i, l in enumerate(lineas, 1))

    def buscar(self, patron):
        rx, hallazgos = re.compile(patron), []
        for p in sorted(self.raiz.rglob("*.py")):
            for i, l in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                if rx.search(l):
                    hallazgos.append(f"{p.relative_to(self.raiz)}:{i}: {l.strip()}")
        return "\n".join(hallazgos) or "(sin resultados)"

    def ejecutar_pruebas(self):
        r = subprocess.run(["python", "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider"],
                           cwd=self.raiz, timeout=120, **_TEXTO)
        salida = (r.stdout + r.stderr).strip().splitlines()
        fallos = [l for l in salida if l.startswith(("FAILED", "E "))][:6]
        return "\n".join(fallos + salida[-1:])

    def editar_archivo(self, ruta, antes, despues):
        p = self._ruta(ruta)
        texto = p.read_text(encoding="utf-8")
        if texto.count(antes) != 1:
            return f"ERROR: el fragmento aparece {texto.count(antes)} veces; debe aparecer exactamente 1"
        p.write_text(texto.replace(antes, despues), encoding="utf-8")
        return f"OK: {ruta} modificado"

    def ver_cambios(self):
        import difflib
        salida = []
        for p in sorted(self.raiz.rglob("*.py")):
            rel = p.relative_to(self.raiz).as_posix(); q = self.original / rel
            a = q.read_text(encoding="utf-8").splitlines() if q.exists() else []
            salida += difflib.unified_diff(a, p.read_text(encoding="utf-8").splitlines(),
                                           f"a/{rel}", f"b/{rel}", lineterm="", n=1)
        return "\n".join(salida) or "(sin cambios)"

    def ejecutar_comando(self, comando):
        r = subprocess.run(comando, shell=True, cwd=self.raiz, timeout=60, **_TEXTO)
        return (r.stdout + r.stderr).strip()[-2000:]

    # --- E4: herramienta nueva ---
    def mapa_repo(self, carpeta="src"):
        base = self._ruta(carpeta)
        if not base.is_dir():
            return f"ERROR: {carpeta} no es una carpeta del sandbox"
        bloques = []
        for p in sorted(base.rglob("*.py")):
            if "__pycache__" in p.parts:
                continue
            rel = p.relative_to(self.raiz).as_posix()
            try:
                arbol = ast.parse(p.read_text(encoding="utf-8"))
            except SyntaxError as e:
                bloques.append(f"{rel}\n  (error de sintaxis en la línea {e.lineno})")
                continue
            lineas = [f"  {l}" for l in _firmas(arbol.body, nivel=0)]
            if lineas:
                bloques.append(rel + "\n" + "\n".join(lineas))
        return "\n".join(bloques) or "(sin clases ni funciones)"

    # --- E4: memoria de notas (pizarra de la tarea) ---
    def anotar(self, texto):
        if not isinstance(texto, str) or not texto.strip():
            return "ERROR: la nota debe ser un texto no vacío"
        if len(texto) > MAX_NOTA:
            return f"ERROR: la nota tiene {len(texto)} caracteres; el máximo es {MAX_NOTA}"
        actuales = self._notas()
        if len(actuales) >= MAX_NOTAS:
            return f"ERROR: ya hay {MAX_NOTAS} notas; resuma las anteriores en lugar de agregar más"
        n = len(actuales) + 1
        with open(self.archivo_notas, "a", encoding="utf-8") as f:
            f.write(f"- [{n}] {' '.join(texto.split())}\n")
        return f"OK: nota {n} guardada en notas.md"

    def leer_notas(self):
        notas = self._notas()
        return "\n".join(notas) if notas else "(sin notas)"

    def _notas(self) -> list:
        if not self.archivo_notas.exists():
            return []
        return [l for l in self.archivo_notas.read_text(encoding="utf-8").splitlines() if l.startswith("- [")]


def _firmas(nodos, nivel):
    """Devuelve 'línea: class X(bases)' y 'línea: def f(args) -> retorno' sin los cuerpos."""
    sangria, salida = "  " * nivel, []
    for n in nodos:
        if isinstance(n, ast.ClassDef):
            bases = ", ".join(ast.unparse(b) for b in n.bases)
            salida.append(f"{n.lineno:4d}: {sangria}class {n.name}" + (f"({bases})" if bases else ""))
            salida += _firmas(n.body, nivel + 1)
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            retorno = f" -> {ast.unparse(n.returns)}" if n.returns else ""
            salida.append(f"{n.lineno:4d}: {sangria}def {n.name}({ast.unparse(n.args)}){retorno}")
    return salida
