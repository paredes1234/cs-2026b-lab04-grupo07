"""E4 (Lab 10): pruebas de la herramienta mapa_repo() y de la memoria de notas. No usan ningún LLM."""
import sys, pathlib, pytest
sys.path.insert(0, str(pathlib.Path(__file__).parents[1]))
from agente.herramientas import Herramientas, MAX_NOTA, MAX_NOTAS
from agente.contrato import validar_decision
from agente.politica import Politica, SOLO_LECTURA

CODIGO = '''
class Servicio(Base):
    def confirmar_y_pagar(self, pedido_id: str, monto: float, tipo_pago: str = "YAPE") -> dict:
        x = 1
        return {}

def ayudante(a, *args, **kw):
    pass
'''


@pytest.fixture
def h(tmp_path):
    (tmp_path / "src" / "despues").mkdir(parents=True)
    (tmp_path / "src" / "despues" / "servicio.py").write_text(CODIGO, encoding="utf-8")
    (tmp_path / "src" / "roto.py").write_text("def f(:\n", encoding="utf-8")
    return Herramientas(tmp_path)


def test_mapa_repo_devuelve_firmas_con_linea_y_tipos(h):
    mapa = h.mapa_repo()
    assert "src/despues/servicio.py" in mapa
    assert "2: class Servicio(Base)" in mapa
    assert '3:   def confirmar_y_pagar(self, pedido_id: str, monto: float, tipo_pago: str=\'YAPE\') -> dict' in mapa
    assert "def ayudante(a, *args, **kw)" in mapa


def test_mapa_repo_no_incluye_cuerpos(h):
    assert "x = 1" not in h.mapa_repo() and "return {}" not in h.mapa_repo()


def test_mapa_repo_informa_error_de_sintaxis_sin_romperse(h):
    assert "src/roto.py\n  (error de sintaxis en la línea 1)" in h.mapa_repo()


def test_mapa_repo_respeta_el_sandbox(h):
    with pytest.raises(PermissionError):
        h.mapa_repo("../..")
    assert h.mapa_repo("src/despues/servicio.py").startswith("ERROR")


def test_notas_se_guardan_en_notas_md_y_se_leen(h):
    assert h.leer_notas() == "(sin notas)"
    assert h.anotar("Hipótesis: monto llega como float") == "OK: nota 1 guardada en notas.md"
    h.anotar("Revisado:\n src/despues/servicio.py")               # los saltos de línea se compactan
    assert h.leer_notas() == "- [1] Hipótesis: monto llega como float\n- [2] Revisado: src/despues/servicio.py"
    assert (h.raiz / "notas.md").exists()


@pytest.mark.parametrize("texto", ["", "   ", None, "x" * (MAX_NOTA + 1)])
def test_anotar_rechaza_notas_vacias_o_largas(h, texto):
    assert h.anotar(texto).startswith("ERROR")
    assert h.leer_notas() == "(sin notas)"


def test_anotar_limita_el_numero_de_notas(h):
    for i in range(MAX_NOTAS):
        h.anotar(f"nota {i}")
    assert h.anotar("una más").startswith("ERROR")


def test_herramientas_nuevas_estan_en_el_catalogo_y_el_contrato_las_acepta(h):
    cat = h.catalogo()
    assert {"mapa_repo", "anotar", "leer_notas"} <= set(cat)
    assert validar_decision({"pensamiento": "mapa", "accion": "mapa_repo", "args": {"carpeta": "src"}}, set(cat))[0]


def test_revisor_puede_leer_notas_pero_no_anotar():
    revisor = Politica(herramientas_permitidas=set(SOLO_LECTURA))
    assert revisor.evaluar("leer_notas", {}, 1).permitido
    assert revisor.evaluar("mapa_repo", {}, 1).permitido
    assert not revisor.evaluar("anotar", {"texto": "x"}, 1).permitido
    assert not revisor.evaluar("editar_archivo", {"ruta": "src/a.py"}, 1).permitido


def test_ver_cambios_ya_no_acepta_una_ruta_elegida_por_el_modelo(h, tmp_path):
    with pytest.raises(TypeError):
        h.ver_cambios(original="../../")
