from experta import *
from hechos import *

# Clase base para el sistema de reglas
# Aqui se manejan las preguntas que se muestran al usuario
# y los diagnosticos que se van encontrando
"""
Componentes base del motor de reglas de Cars_ChatBot.

Este módulo define la clase SistemaBase, que extiende el motor KnowledgeEngine
de experta y proporciona utilidades comunes para todos los sistemas especialistas,
como el almacenamiento de diagnósticos generados y la gestión de preguntas.
"""

class SistemaBase(KnowledgeEngine):
    """Clase base para todos los sistemas especialistas de diagnóstico.

    Responsabilidades principales:
    - Ejecutar las reglas asociadas a un subsistema del vehículo.
    - Ir acumulando en `diagnosticos_encontrados` las posibles causas
      y soluciones detectadas durante la inferencia.
    - Proveer métodos auxiliares comunes (reinicio de estado, formateo
      de resultados, etc.) que reutilizan los distintos módulos.
    """
    def __init__(self):
        super().__init__()

        self.diagnosticos_encontrados = []
        self.pregunta_actual = None

    def obtener_diagnosticos(self):
        """
        Regresa una copia de los diagnósticos encontrados.
        Se devuelve copia para evitar que la lista original
        se modifique accidentalmente desde fuera.
        """
        return self.diagnosticos_encontrados.copy()

    def obtener_pregunta_actual(self):
        """
        Devuelve la pregunta actual que el sistema generó.
        Esto sirve para mostrarla al usuario cuando se necesite.
        """
        return self.pregunta_actual

    def limpiar_pregunta_actual(self):
        """
        Limpia la pregunta actual cuando ya fue respondida
        o cuando se quiere avanzar a otra parte del proceso.
        """
        self.pregunta_actual = None

    # Regla comun para todas las clases que hereden de esta
    # Cada vez que aparezca un hecho del tipo Pregunta
    # esta regla guarda sus datos como la pregunta actual
    @Rule(Pregunta(clave=MATCH.c, texto=MATCH.t, opciones=MATCH.o))
    def guardar_pregunta(self, c, t, o):
        # Guardamos la pregunta en un diccionario 
        self.pregunta_actual = {'clave': c, 'texto': t, 'opciones': o}
