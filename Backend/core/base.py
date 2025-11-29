from experta import *
from hechos import *

# Clase base para el sistema de reglas
# Aqui se manejan las preguntas que se muestran al usuario
# y los diagnosticos que se van encontrando
class SistemaBase(KnowledgeEngine):
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
