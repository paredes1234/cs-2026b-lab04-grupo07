import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agente.contrato import validar_decision

HERRAMIENTAS = {
    "listar_archivos",
    "leer_archivo",
    "editar_archivo",
    "buscar",
    "ejecutar_pruebas",
    "ejecutar_comando",
}


def test_rechaza_campo_extra():
    decision = {
        "pensamiento": "Revisar archivos",
        "accion": "listar_archivos",
        "args": {},
        "campo_extra": "no permitido"
    }
    valido, motivo = validar_decision(decision, HERRAMIENTAS)
    assert valido is False


def test_rechaza_args_como_texto():
    decision = {
        "pensamiento": "Leer archivo",
        "accion": "leer_archivo",
        "args": "archivo.py"
    }
    valido, motivo = validar_decision(decision, HERRAMIENTAS)
    assert valido is False


def test_rechaza_accion_vacia():
    decision = {
        "pensamiento": "Ejecutar acción",
        "accion": "",
        "args": {}
    }
    valido, motivo = validar_decision(decision, HERRAMIENTAS)
    assert valido is False


def test_rechaza_pensamiento_vacio():
    decision = {
        "pensamiento": "",
        "accion": "listar_archivos",
        "args": {}
    }
    valido, motivo = validar_decision(decision, HERRAMIENTAS)
    assert valido is False