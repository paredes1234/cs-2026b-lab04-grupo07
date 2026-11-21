"""E6 (Lab 10): humano en el circuito. Se simula la consola con respuestas predefinidas."""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parents[1]))
from agente.humano import AprobadorConsola
from agente.politica import Politica

EDICION = {"ruta": "src/despues/servicio.py", "antes": "a = 1", "despues": "a = 2"}


def aprobador(*respuestas, **kw):
    r = iter(respuestas)
    salida = []
    return AprobadorConsola(entrada=lambda _: next(r), salida=salida.append, **kw), salida


def test_s_aprueba_y_la_politica_permite_la_edicion():
    ap, _ = aprobador("s")
    assert Politica(aprobar_edicion=ap).evaluar("editar_archivo", EDICION, 1).permitido


def test_n_rechaza_y_la_politica_bloquea_la_edicion():
    ap, _ = aprobador("n")
    d = Politica(aprobar_edicion=ap).evaluar("editar_archivo", EDICION, 1)
    assert not d.permitido and d.motivo == "El revisor humano rechazó la edición"


def test_respuesta_invalida_se_vuelve_a_pedir():
    ap, salida = aprobador("si", "S", "s")
    assert ap(EDICION) is True
    assert sum("Respuesta no válida" in s for s in salida) == 2
    assert ap.decisiones[0]["respuestas"] == ["si", "S", "s"]


def test_sin_respuesta_valida_se_rechaza_por_seguridad():
    ap, salida = aprobador("y", "", "ok", max_intentos=3)
    assert ap(EDICION) is False
    assert "se rechaza por seguridad" in salida[-1]


def test_se_muestra_la_edicion_antes_de_preguntar():
    ap, salida = aprobador("n")
    ap(EDICION)
    assert "Archivo: src/despues/servicio.py" in salida[0] and "- a = 1" in salida[0] and "+ a = 2" in salida[0]


def test_lectura_no_pide_aprobacion():
    ap, _ = aprobador()                                   # sin respuestas: si se llamara, fallaría
    assert Politica(aprobar_edicion=ap).evaluar("leer_archivo", {"ruta": "x"}, 1).permitido


def test_la_ruta_protegida_se_bloquea_antes_de_molestar_al_humano():
    ap, _ = aprobador()
    assert not Politica(aprobar_edicion=ap).evaluar("editar_archivo", {"ruta": "tests/t.py"}, 1).permitido


def test_cada_decision_queda_registrada_sin_datos_personales(tmp_path):
    reg = tmp_path / "aprobaciones.jsonl"
    ap, _ = aprobador("s", registro=reg, responsable="integrante del grupo")
    ap(EDICION)
    d = json.loads(reg.read_text(encoding="utf-8"))
    assert d["aprobado"] is True and d["ruta"] == EDICION["ruta"] and d["responsable"] == "integrante del grupo"


def test_la_observacion_humana_queda_registrada_con_la_decision(tmp_path):
    reg = tmp_path / "aprobaciones.jsonl"
    ap, _ = aprobador("s", "Falta una prueba", registro=reg, pedir_observacion=True, origen="consola")
    assert ap(EDICION) is True
    d = json.loads(reg.read_text(encoding="utf-8"))
    assert d["observacion"] == "Falta una prueba" and d["origen"] == "consola"


def test_observacion_vacia_se_registra_como_ninguna():
    ap, _ = aprobador("n", "", pedir_observacion=True)
    assert ap(EDICION) is False and ap.decisiones[0]["observacion"] is None
