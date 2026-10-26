class PoliticaReintentos:
    """Encapsula la estrategia de reintentos para operaciones propensas a fallo."""
    def __init__(self, max_reintentos: int = 1):
        self.max_reintentos = max_reintentos

    def ejecutar(self, funcion_operacion, *args, **kwargs):
        intento = 0
        monto = args[0] if args else kwargs.get("monto")
        token = args[1] if len(args) > 1 else kwargs.get("token")

        while intento < self.max_reintentos:
            try:
                return funcion_operacion(monto, token)
            except ConnectionError as e:
                intento += 1
                if intento >= self.max_reintentos:
                    raise RuntimeError(f"Error de red tras {self.max_reintentos} reintentos: {str(e)}")
            except ValueError as e:
                raise e