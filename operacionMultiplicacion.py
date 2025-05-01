from operacionBase import OperacionBase

class OperacionMultiplicacion(OperacionBase):
    """Clase para la operación de multiplicación."""

    def formatear_pregunta(self, operacion):
        a, b = operacion
        return f"¿Cuánto es {a} × {b}?"

    def formatear_celda(self, operacion):
        a, b = operacion
        return f"{a} × {b}"

    def calcular_respuesta(self, operacion):
        a, b = operacion
        return a * b

    def generar_operaciones(self):
        """Genera todas las combinaciones de multiplicación en el rango [inicio, fin) en forma triangular."""
        return [(a, b) for a in range(self.inicio, self.fin)
                        for b in range(a, self.fin)]

