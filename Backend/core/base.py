# Librerias clave
from experta import *
from hechos import *

# Clase SistemaBase
class SistemaBase(KnowledgeEngine):
    
    def __init__(self):
        super().__init__()
        
        self.diagnosticos_encontrados = []

        self.pregunta_actual = None

    # Función para darle una copia de los resultados encontrados.
    def obtener_diagnosticos(self):
        """Retorna una copia de los diagnósticos encontrados"""
        return self.diagnosticos_encontrados.copy()

    # Funcion para saber la pregunta actual
    def obtener_pregunta_actual(self):
        """Retorna la pregunta actual"""
        return self.pregunta_actual

    # Función para borrar la pregunta anterior
    def limpiar_pregunta_actual(self):
        """Limpia la pregunta actual"""
        self.pregunta_actual = None

    # Regla: Se activa cuando el sistema 've' una nueva pregunta.
    @Rule(Pregunta(clave=MATCH.c, texto=MATCH.t, opciones=MATCH.o))
    def guardar_pregunta(self, c, t, o):
        self.pregunta_actual = {'clave': c, 'texto': t, 'opciones': o}