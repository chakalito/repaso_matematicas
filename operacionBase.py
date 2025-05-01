from abc import ABC, abstractmethod

class OperacionBase(ABC):
    """Clase abstracta que contiene los métodos comunes a las operaciones matemáticas."""

    def __init__(self, inicio, fin):
        self.inicio = inicio
        self.fin = fin

    @abstractmethod
    def formatear_pregunta(self, operacion):
        """Formatea la pregunta para la operación dada."""
        pass

    @abstractmethod
    def formatear_celda(self, operacion):
        """Devuelve la representación de la operación, a mostrar en la celda."""
        pass

    @abstractmethod
    def calcular_respuesta(self, operacion):
        """Calcula y retorna la respuesta correcta para la operación."""
        pass

    @abstractmethod
    def generar_operaciones(self):
        """Genera todas las operaciones posibles en el rango dado."""
        pass
