"""Integración del puerto ProveedorLLM con las grabaciones de E4 y E5."""
import json
from pathlib import Path

import pytest

from src.despues.generador_normalizacion import GeneradorNormalizacion, SalidaInvalida
from src.despues.ia import ProveedorLLM


RAIZ = Path(__file__).resolve().parents[1]
GRABACIONES_E4 = RAIZ / "prompts" / "normalizacion" / "grabaciones"
GRABACIONES_E5 = RAIZ / "seguridad" / "grabaciones"
CATALOGO = ("papa amarilla", "cebolla roja", "limón sutil")


class ClienteGrabado:
    def __init__(self, archivo: Path) -> None:
        self.archivo = archivo
        self.prompts: list[str] = []

    def completar(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self.archivo.read_text(encoding="utf-8")


def test_acepta_json_valido_de_v4_a_traves_del_puerto():
    cliente = ClienteGrabado(GRABACIONES_E5 / "v4" / "C02.txt")
    generador = GeneradorNormalizacion(cliente, CATALOGO)
    assert isinstance(generador, ProveedorLLM)
    assert generador.normalizar_nombre("papa amarila", id_registro="C02") == "papa amarilla"
    registro = cliente.prompts[0].split("<registro>\n", 1)[1].split("\n</registro>", 1)[0]
    assert json.loads(registro) == {"id": "C02", "entrada": "papa amarila"}


def test_carga_v3_por_version_y_acepta_desconocido():
    cliente = ClienteGrabado(GRABACIONES_E4 / "v3" / "B07.txt")
    generador = GeneradorNormalizacion(cliente, CATALOGO, version="v3")
    assert generador.normalizar_nombre("manzana rosada", id_registro="B07") == "desconocido"
    assert 'Registro original: {"id":"B07","entrada":"manzana rosada"}' in cliente.prompts[0]


def test_rechaza_grabacion_con_markdown():
    cliente = ClienteGrabado(GRABACIONES_E5 / "v3" / "RT04.txt")
    generador = GeneradorNormalizacion(cliente, CATALOGO)
    with pytest.raises(SalidaInvalida, match="JSON válido"):
        generador.normalizar_nombre("limón sutil", id_registro="RT04")


def test_rechaza_json_con_campo_obligatorio_ausente(tmp_path):
    grabacion = tmp_path / "sin-producto.txt"
    grabacion.write_text('{"id":"normalizacion","entrada":"papa amarila"}', encoding="utf-8")
    generador: ProveedorLLM = GeneradorNormalizacion(ClienteGrabado(grabacion), CATALOGO)
    with pytest.raises(SalidaInvalida, match="JSON Schema"):
        generador.normalizar_nombre("papa amarila")


def test_rechaza_entrada_original_modificada():
    cliente = ClienteGrabado(GRABACIONES_E4 / "v2" / "B03.txt")
    generador = GeneradorNormalizacion(cliente, CATALOGO, version="v2")
    with pytest.raises(SalidaInvalida, match="entrada original"):
        generador.normalizar_nombre("  CEBOLLA   ROJA  ", id_registro="B03")


def test_rechaza_producto_fuera_del_catalogo_configurado():
    cliente = ClienteGrabado(GRABACIONES_E5 / "v4" / "RT02.txt")
    generador = GeneradorNormalizacion(cliente, ("papa amarilla",))
    with pytest.raises(SalidaInvalida, match="fuera del catálogo"):
        generador.normalizar_nombre("cebolla roja", id_registro="RT02")


def test_rechaza_nombre_invalido_antes_de_invocar_cliente(tmp_path):
    cliente = ClienteGrabado(tmp_path / "sin-llamada.txt")
    generador = GeneradorNormalizacion(cliente, CATALOGO)
    with pytest.raises(ValueError, match="letras y espacios"):
        generador.normalizar_nombre("cebolla roja, tamaño mediano")
    assert cliente.prompts == []
