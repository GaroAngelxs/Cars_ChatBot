from experta import *
from core.base import SistemaBase
from hechos import *

class SistemaTransmision(SistemaBase):
    def __init__(self):
        super().__init__()

    @Rule(Sistema(area='transmision'))
    def iniciar_diagnostico_transmision(self):
        print("Iniciando diagnóstico: Sistema Transmision")

    # Paso 1: Preguntar sobre si los cambios entran con dificultad
    @Rule(Sistema(area='transmision'),
        NOT(Estado(clave='cambios_entran_dificultad')))
    def preguntar_si_cambios_entran(self):
        self.declare(Pregunta(  
            clave='cambios_entran_dificultad',
            texto="¿Los cambios entran con dificultad?",
            opciones=['si', 'no']
        ))
    
    # Paso 2: Preguntar si el pedal tiene un recorrido suave
    @Rule(Sistema(area='transmision'),
        Estado(clave='cambios_entran_dificultad', valor='si'),
        NOT(Estado(clave='pedal_recorrido_suave')))
    def preguntar_recorrido_del_pedal(self):
        self.declare(Pregunta(
            clave='pedal_recorrido_suave',
            texto="¿El pedal tiene un recorrido muy largo o suave?",
            opciones=['si', 'no']
        ))
 
    # Paso 3: Preguntar el color del aceite de la transmision
    @Rule(Sistema(area='transmision'),
        Estado(clave='cambios_entran_dificultad', valor='si'),
        Estado(clave='pedal_recorrido_suave', valor='no'),
        NOT(Estado(clave='color_olor_del_aceite')))
    def preguntar_color_olor_del_aceite(self):
        self.declare(Pregunta(
            clave='color_olor_del_aceite',
            texto="¿El aceite tiene un color oscuro y quemado?",
            opciones=['si', 'no']
        ))

    # Paso 4: 
    @Rule(Sistema(area='transmision'),
        Estado(clave='cambios_entran_dificultad',valor='no'),
        NOT(Estado(clave='ruidos_metalicos_en_marcha')))
    def preguntar_si_hay_ruidos_marcha(self):
        self.declare(Pregunta(
            clave='ruidos_metalicos_en_marcha',
            texto="¿Se escuchan ruidos metalicos al cambiar de marcha?",
            opciones=['si', 'no']
        ))

    # Paso 5: 
    @Rule(Sistema(area='transmision'),
        Estado(clave='ruidos_metalicos_en_marcha',valor='si'),
        NOT(Estado(clave='ruido_mas_fuerte_en_especifico')))
    def preguntar_si_hay_ruidos_marcha(self):
        self.declare(Pregunta(
            clave='ruido_mas_fuerte_en_especifico',
            texto="¿Se escucha un ruido mas fuerte en una marcha en especifico?",
            opciones=['si', 'no']
        ))

    # Diagnóstico 1: Sistema de transmision
    @Rule(Sistema(area='transmision'),
        Estado(clave='cambios_entran_dificultad', valor='si'),
        Estado(clave='pedal_recorrido_suave', valor='si'))
    def diagnostico_sistema_de_transmision_embrague(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falla en embrague",
            'solucion': "El embrague está desgastado",
            'severidad': "Alta"
        })
    
    # Diagnóstico 2: Sistema de transmision
    @Rule(Sistema(area='transmision'),
        Estado(clave='cambios_entran_dificultad', valor='si'),
        Estado(clave='color_olor_del_aceite', valor='si'))
    def diagnostico_sistema_de_transmision_aceite(self):
        self.diagnosticos_encontrados.append({
            'causa': "Aceite desgastado",
            'solucion': "El aceite de transmisión está desgastado",
            'severidad': "Alta"
        })