import random

class Configuracion:
    """Clase para centralizar configuración y estilos de toda la aplicación"""
    
    # Colores
    COLOR_FONDO = "#FFF0F5"  # Rosa muy claro
    COLOR_CABECERA = "#FFD1DC"  # Rosa pálido
    COLOR_TEXTO = "#8B0000"  # Rojo oscuro
    COLOR_TITULO = "#C71585"  # Rosa intenso
    COLOR_ROSA = "#FF69B4"  # Rosa fuerte
    COLOR_LILA = "#DDA0DD"  # Lila
    
    # Colores para celdas
    COLOR_CORRECTO = "#98FB98"  # Verde pálido
    COLOR_INCORRECTO = "#FFC0CB"  # Rosa claro
    COLOR_NEUTRO = "#FFFFFF"  # Blanco
    
    # Fuentes
    FUENTE_NORMAL = ("Comic Sans MS", 12)
    FUENTE_TITULO = ("Comic Sans MS", 18, "bold")
    FUENTE_GRANDE = ("Comic Sans MS", 24, "bold")
    FUENTE_SUBTITULO = ("Comic Sans MS", 16)
    FUENTE_BOTONES = ("Comic Sans MS", 14, "bold")
    FUENTE_CELDA = ("Comic Sans MS", 10)
    
    # Decoraciones
    DECORACIONES = ["👑", "⭐", "🌟", "💫", "✨", "🦄", "🧚‍♀️", "🎀"]
    
    # Mensajes
    MENSAJES_CORRECTO = [
        "¡Respuesta mágica! Eres toda una princesa matemática.",
        "¡Fantástico! Tu varita mágica matemática funciona de maravilla.",
        "¡Genial! Las matemáticas son tu superpoder."
    ]
    
    MENSAJES_INCORRECTO = [
        "¡Ups! Inténtalo de nuevo. ¡La magia está en ti!",
        "Casi lo tienes. ¡Sigue practicando tu magia matemática!",
        "¡Prueba otra vez! Cada error te acerca a ser una princesa matemática."
    ]
    
    # Títulos por operación
    TITULOS_OPERACIONES = {
        "suma": "Aventura de Sumas Mágicas",
        "resta": "Desafío de Restas Encantadas",
        "multiplicacion": "Multiplicaciones Mágicas",
        "division": "Pócimas de División"
    }
    
    # Probabilidad de repetir operaciones fallidas (30% es un buen equilibrio)
    PROB_REPETIR_FALLIDAS = 0.3

    
class Utilidades:
    """Clase para funciones de utilidad compartidas"""
    
    @staticmethod
    def formatear_tiempo(segundos):
        """Convierte segundos en formato horas:minutos:segundos"""
        horas = int(segundos // 3600)
        minutos = int((segundos % 3600) // 60)
        segundos = int(segundos % 60)
        return f"{horas:02d}:{minutos:02d}:{segundos:02d}"
    
    @staticmethod
    def mensaje_aleatorio(lista_mensajes):
        """Selecciona un mensaje aleatorio de una lista"""
        return random.choice(lista_mensajes)