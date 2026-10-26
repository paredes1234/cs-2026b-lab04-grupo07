class PagoFactory:
    def __init__(self):
        self._adaptadores = {}

    def registrar(self, nombre_variante, adaptador):
        self._adaptadores[nombre_variante] = adaptador

    def obtener(self, nombre_variante):
        if nombre_variante not in self._adaptadores:
            raise ValueError(f"Variante '{nombre_variante}' no registrada")
        return self._adaptadores[nombre_variante]