from experta import *
from hechos import *

class SistemaBase(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.diagnosticos_encontrados = []
        self.pregunta_actual = None

    def obtener_diagnosticos(self):
        """Retorna una copia de los diagnósticos encontrados"""
        return self.diagnosticos_encontrados.copy()

    def obtener_pregunta_actual(self):
        """Retorna la pregunta actual"""
        return self.pregunta_actual

    def limpiar_pregunta_actual(self):
        """Limpia la pregunta actual"""
        self.pregunta_actual = None

    # Regla común para todas las clases hijas
    @Rule(Pregunta(clave=MATCH.c, texto=MATCH.t, opciones=MATCH.o))
    def guardar_pregunta(self, c, t, o):
        self.pregunta_actual = {'clave': c, 'texto': t, 'opciones': o}