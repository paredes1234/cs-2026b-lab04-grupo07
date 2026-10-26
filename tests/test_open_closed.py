import sys
import os

# Agrega la raíz del proyecto al PATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.despues.factory import PagoFactory
from src.despues.servicio import *


def test_open_closed_agregar_nueva_variante_sin_modificar_servicio():
    # 1. Instanciamos la fábrica
    factory = PagoFactory()

    # 2. Creamos una nueva variante/adaptador para la prueba
    class NuevaVarianteAdapter:
        def procesar(self, datos):
            return "OK_NUEVA_VARIANTE"

    # 3. Registramos la nueva variante sin modificar la lógica del servicio (Open/Closed)
    nueva_variante = NuevaVarianteAdapter()
    factory.registrar("NUEVA_VARIANTE", nueva_variante)

    # 4. Verificaciones
    adaptador_obtenido = factory.obtener("NUEVA_VARIANTE")
    assert adaptador_obtenido.procesar({}) == "OK_NUEVA_VARIANTE"