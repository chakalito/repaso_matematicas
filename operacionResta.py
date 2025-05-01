from operacionBase import OperacionBase

class OperacionResta(OperacionBase):
    """Clase para la operación de resta."""

    def formatear_pregunta(self, operacion):
        a, b = operacion
        return f"¿Cuánto es {b} - {a}?"

    def formatear_celda(self, operacion):
        a, b = operacion
        return f"{b} - {a}"

    def calcular_respuesta(self, operacion):
        a, b = operacion
        return b - a

    def generar_operaciones(self):
        """Genera todas las combinaciones de resta en el rango [inicio, fin)
           que aseguran un resultado no negativo."""
        return [(a, b) for a in range(self.inicio, self.fin) 
                        for b in range(a, self.fin)]
