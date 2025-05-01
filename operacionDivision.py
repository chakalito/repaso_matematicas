from operacionBase import OperacionBase

class OperacionDivision(OperacionBase):
    """Clase para la operación de división."""

    def formatear_pregunta(self, operacion):
        a, b = operacion
        return f"¿Cuánto es {a * b} ÷ {a}?"

    def formatear_celda(self, operacion):
        a, b = operacion
        return f"{a * b} ÷ {a}"

    def calcular_respuesta(self, operacion):
        a, b = operacion
        return b

    def generar_operaciones(self):
        """Genera todas las combinaciones de división en el rango [inicio, fin)
           de modo que la división sea exacta."""
        return [(a, b) for a in range(self.inicio, self.fin) 
                        for b in range(self.inicio, self.fin)]
