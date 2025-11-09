from experta import *
from core.base import SistemaBase
from hechos import *

class SistemaTransmision1(SistemaBase):
    def __init__(self):
        super().__init__()

    @Rule(Sistema(area='transmision_1'))
    def iniciar_diagnostico_transmision(self):
        print("Iniciando diagnóstico: Sistema Transmision")

    # Paso 1: Preguntar sobre si los cambios entran con dificultad
    @Rule(Sistema(area='transmision_1'),
        NOT(Estado(clave='cambios_entran_dificultad')))
    def preguntar_si_cambios_entran(self):
        self.declare(Pregunta(  
            clave='cambios_entran_dificultad',
            texto="¿Los cambios entran con dificultad?",
            opciones=['si', 'no']
        ))
    
    # Paso 2: Preguntar si el pedal tiene un recorrido suave
    @Rule(Sistema(area='transmision_1'),
        Estado(clave='cambios_entran_dificultad', valor='si'),
        NOT(Estado(clave='pedal_recorrido_suave')))
    def preguntar_recorrido_del_pedal(self):
        self.declare(Pregunta(
            clave='pedal_recorrido_suave',
            texto="¿El pedal tiene un recorrido muy largo o suave?",
            opciones=['si', 'no']
        ))
 
    # Paso 3: Preguntar el color del aceite de la transmision
    @Rule(Sistema(area='transmision_1'),
        Estado(clave='cambios_entran_dificultad', valor='si'),
        Estado(clave='pedal_recorrido_suave', valor='no'),
        NOT(Estado(clave='color_olor_del_aceite')))
    def preguntar_color_olor_del_aceite(self):
        self.declare(Pregunta(
            clave='color_olor_del_aceite',
            texto="¿El aceite tiene un color oscuro y quemado?",
            opciones=['si', 'no']
        ))

    # Diagnóstico 1: Sistema de transmision
    @Rule(Sistema(area='transmision_1'),
        Estado(clave='cambios_entran_dificultad', valor='si'),
        Estado(clave='pedal_recorrido_suave', valor='si'))
    def diagnostico_sistema_de_transmision_embrague(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falla en embrague",
            'solucion': "El embrague está desgastado",
            'severidad': "Alta"
        })
    
    # Diagnóstico 2: Sistema de transmision
    @Rule(Sistema(area='transmision_1'),
        Estado(clave='cambios_entran_dificultad', valor='si'),
        Estado(clave='color_olor_del_aceite', valor='si'))
    def diagnostico_sistema_de_transmision_aceite(self):
        self.diagnosticos_encontrados.append({
            'causa': "Aceite desgastado",
            'solucion': "El aceite de transmisión está desgastado",
            'severidad': "Alta"
        })

class SistemaTransmision2(SistemaBase):
    def __init__(self):
        super().__init__()

    @Rule(Sistema(area='transmision_2'))
    def iniciar_diagnostico_transmision(self):
        print("Iniciando diagnóstico: Sistema Transmision")

    # Paso 1: Preguntar sobre si los cambios entran con dificultad
    @Rule(Sistema(area='transmision_2'),
        NOT(Estado(clave='ruidos_metalicos_marcha')))
    def preguntar_si_hay_ruidos_metalicos_marcha(self):
        self.declare(Pregunta(  
            clave='ruidos_metalicos_marcha',
            texto="¿Hay ruidos metalicos al cambiar de marcha?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='transmision_2'),
        Estado(clave='ruidos_metalicos_marcha', valor = 'si'),
        NOT(Estado(clave='ruidos_fuerte_especifico')))
    def preguntar_si_el_ruido_es_fuerte_especifico(self):
        self.declare(Pregunta(  
            clave='ruidos_fuerte_especifico',
            texto="¿El ruido es mas fuerte en una marcha en especifico?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='transmision_2'),
        Estado(clave='ruidos_metalicos_marcha', valor = 'si'),
        Estado(clave='ruidos_fuerte_especifico', valor = 'no'),
        NOT(Estado(clave='ruidos_fuerte_todas')))
    def preguntar_si_el_ruido_es_fuerte_todas(self):
        self.declare(Pregunta(  
            clave='ruidos_fuerte_todas',
            texto="¿El ruido es parecido en todas las marchas?",
            opciones=['si', 'no']
        ))

        # Diagnóstico 1: Sistema de transmision
    @Rule(Sistema(area='transmision_2'),
        Estado(clave='ruidos_metalicos_marcha', valor='si'),
        Estado(clave='ruidos_fuerte_especifico', valor='si'))
    def diagnostico_sistema_de_transmision_desgaste_engranajes(self):
        self.diagnosticos_encontrados.append({
            'causa': "Desgaste de engranajes en la transmision",
            'solucion': "Reparar caja de cambios",
            'severidad': "Alta"
        })
    
    # Diagnóstico 2: Sistema de transmision
    @Rule(Sistema(area='transmision_2'),
        Estado(clave='ruidos_metalicos_marcha', valor='si'),
        Estado(clave='ruidos_fuerte_todas', valor='si'))
    def diagnostico_sistema_de_transmision_falta_aceite(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falta lubricante en la transmision",
            'solucion': "Rellenar el lubricante faltante en la transmsiion",
            'severidad': "Alta"
        })

class SistemaTransmision3(SistemaBase):
    def __init__(self):
        super().__init__()

    @Rule(Sistema(area='transmision_3'))
    def iniciar_diagnostico_transmision(self):
        print("Iniciando diagnóstico: Sistema Transmision")

    @Rule(Sistema(area='transmision_3'),
        NOT(Estado(clave='auto_avanza_al_acelerar')))
    def preguntar_si_el_auto_avanza_al_acelerar(self):
        self.declare(Pregunta(  
            clave='auto_avanza_al_acelerar',
            texto="¿El auto avanza al acelerar?",
            opciones=['si', 'no']
        ))
    
    @Rule(Sistema(area='transmision_3'),
        Estado(clave='auto_avanza_al_acelerar',valor = 'no'),
        NOT(Estado(clave='revoluciones_suben_sin_acelerar')))
    def preguntar_sobre_revoluciones(self):
        self.declare(Pregunta(  
            clave='revoluciones_suben_sin_acelerar',
            texto="¿Las revoluciones del auto suben sin acelerar?",
            opciones=['si', 'no']
        ))
    
    @Rule(Sistema(area='transmision_3'),
        Estado(clave='auto_avanza_al_acelerar',valor = 'no'),
        Estado(clave='revoluciones_suben_sin_acelerar', valor = 'no'),
        NOT(Estado(clave='ruido_fuerte_o_traqueteo')))
    def preguntar_si_hay_ruidos_metalicos(self):
        self.declare(Pregunta(  
            clave='ruido_fuerte_o_traqueteo',
            texto="¿Se escucha un ruido fuerte o un traqueteo al intentar moverse?",
            opciones=['si', 'no']
        ))

         # Diagnóstico 1: Sistema de transmision
    @Rule(Sistema(area='transmision_3'),
        Estado(clave='auto_avanza_al_acelerar', valor='no'),
        Estado(clave='revoluciones_suben_sin_acelerar', valor='si'))
    def diagnostico_sistema_de_transmision_embrague_patinado(self):
        self.diagnosticos_encontrados.append({
            'causa': "Embrague en mal estado patinando",
            'solucion': "Cambiar el embrague",
            'severidad': "Alta"
        })
    
    # Diagnóstico 2: Sistema de transmision
    @Rule(Sistema(area='transmision_3'),
        Estado(clave='auto_avanza_al_acelerar', valor='no'),
        Estado(clave='ruido_fuerte_o_traqueteo', valor='si'))
    def diagnostico_sistema_de_transmision_falla_transmision(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falla general en la caja de cambios",
            'solucion': "Repeararla o cambiarla",
            'severidad': "Alta"
        })

class SistemaTransmision4(SistemaBase):
    def __init__(self):
        super().__init__()

    @Rule(Sistema(area='transmision_4'))
    def iniciar_diagnostico_transmision(self):
        print("Iniciando diagnóstico: Sistema Transmision")

    @Rule(Sistema(area='transmision_4'),
        NOT(Estado(clave='aceite_transmision_bajo')))
    def preguntar_si_aceite_transmision_bajo(self):
        self.declare(Pregunta(  
            clave='aceite_transmision_bajo',
            texto="¿El aceite de transmision esta bajo?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='transmision_4'),
        Estado(clave='aceite_transmision_bajo',valor='si'),
        NOT(Estado(clave='hay_goteo_aceite')))
    def preguntar_si_hay_goteo_aceite(self):
        self.declare(Pregunta(  
            clave='hay_goteo_aceite',
            texto="¿Hay goteo de aceite bajo el auto?",
            opciones=['si', 'no']
        ))

    # Diagnóstico 1: Sistema de transmision
    @Rule(Sistema(area='transmision_4'),
        Estado(clave='aceite_transmision_bajo', valor='si'),
        Estado(clave='hay_goteo_aceite', valor='no'))
    def diagnostico_sistema_aceite_transmision_bajo(self):
        self.diagnosticos_encontrados.append({
            'causa': "Simplemente aceite bajo",
            'solucion': "Rellenar aceite faltante",
            'severidad': "Bajo"
        })
    
    # Diagnóstico 2: Sistema de transmision
    @Rule(Sistema(area='transmision_4'),
        Estado(clave='aceite_transmision_baj0', valor='si'),
        Estado(clave='hay_goteo_aceite', valor='si'))
    def diagnostico_sistema_de_transmision_posible_fuga(self):
        self.diagnosticos_encontrados.append({
            'causa': "Posibiles fugas de aceite",
            'solucion': "Buscar las fugas de aceite y repararlas",
            'severidad': "Alta"
        })
    
 