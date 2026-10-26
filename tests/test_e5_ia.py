"""E5: LLM simulado, respuestas válidas e inválidas, caché y guardrails."""
import pytest
from src.despues.ia import crear_normalizador, ProveedorLLM, ConCache, ConGuardrails, GuardrailSoloNombre, GuardrailCatalogo


ALIAS = {
    "papa amarila": "papa amarilla",
    "papa amarilla": "papa amarilla",
    "tomate": "tomate",
}


class ClienteLLMFalso:
    def __init__(self, salida):
        self.salida = salida
        self.llamadas = 0

    def completar(self, prompt):
        assert "Producto:" in prompt
        self.llamadas += 1
        return self.salida


def test_ia_normaliza_error_tipografico():
    llm = ClienteLLMFalso("papa amarilla")
    normalizador = crear_normalizador(llm, ALIAS)
    assert normalizador.normalizar_nombre("papa amarila") == "papa amarilla"


def test_decorator_cache_evitar_repetir_llamadas():
    llm = ClienteLLMFalso("papa amarilla")
    normalizador = crear_normalizador(llm, ALIAS)
    assert normalizador.normalizar_nombre("papa amarila") == "papa amarilla"
    assert normalizador.normalizar_nombre("PAPA   AMARILA") == "papa amarilla"
    assert llm.llamadas == 1
    assert normalizador.aciertos == 1


@pytest.mark.parametrize("invalida", [
    "papa amarilla S/ 3.50", "papa amarilla 2kg", "", "papa amarilla, promoción"
])
def test_guardrail_formato_bloquea_precios_y_respuestas_extra(invalida):
    llm = ClienteLLMFalso(invalida)
    normalizador = crear_normalizador(llm, ALIAS)
    with pytest.raises(ValueError, match="IA:"):
        normalizador.normalizar_nombre("papa amarila")


def test_guardrail_catalogo_impide_inventar_producto():
    normalizador = crear_normalizador(ClienteLLMFalso("cebolla blanca"), ALIAS)
    with pytest.raises(ValueError, match="inventó"):
        normalizador.normalizar_nombre("papa amarila")


def test_guardrail_rechaza_entrada_fuera_catalogo():
    normalizador = crear_normalizador(ClienteLLMFalso("papaya"), ALIAS)
    with pytest.raises(ValueError, match="fuera del catálogo"):
        normalizador.normalizar_nombre("papaya")


def test_respuesta_invalida_no_se_guarda_en_cache():
    llm = ClienteLLMFalso("papa amarilla S/ 3")
    normalizador = crear_normalizador(llm, ALIAS)
    with pytest.raises(ValueError):
        normalizador.normalizar_nombre("papa amarila")
    llm.salida = "papa amarilla"
    assert normalizador.normalizar_nombre("papa amarila") == "papa amarilla"
    assert llm.llamadas == 2


def test_strategy_permita_sustituir_proveedor():
    class ProveedorDeterminista(ProveedorLLM):
        def normalizar_nombre(self, nombre):
            return "tomate"
    proveedor = ConCache(ConGuardrails(ProveedorDeterminista(), GuardrailSoloNombre(GuardrailCatalogo(ALIAS))))
    assert proveedor.normalizar_nombre("tomate") == "tomate"
