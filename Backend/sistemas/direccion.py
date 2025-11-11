from experta import *
from core.base import SistemaBase
from hechos import *

class SistemaDireccion1(SistemaBase):
    def __init__(self):
        super().__init__()

    @Rule(Sistema(area='direccion_1'))
    def iniciar_diagnostico_transmision(self):
        print("Iniciando diagnóstico: Sistema Suspension")

    @Rule(Sistema(area='direccion_1'),
        NOT(Estado(clave='volante_duro')))
    def preguntar_si_cambios_entran(self):
        self.declare(Pregunta(  
            clave='volante_duro',
            texto="¿El volante se siente duro al girar?",
            opciones=['si', 'no']
        ))
    
    @Rule(Sistema(area='direccion_1'),
        Estado(clave='volante_duro', valor='si'),
        NOT(Estado(clave='nivel_liquido')))
    def preguntar_recorrido_del_pedal(self):
        self.declare(Pregunta(
            clave='nivel_liquido',
            texto="¿El nivel de liquido de direccion esta debajo del minimo?",
            opciones=['si', 'no']
        ))
 
    @Rule(Sistema(area='direccion_1'),
        Estado(clave='volante_duro', valor='si'),
        Estado(clave='nivel_liquido', valor='no'),
        NOT(Estado(clave='ruido_bomba')))
    def preguntar_color_olor_del_aceite(self):
        self.declare(Pregunta(
            clave='ruido_bomba',
            texto="¿Cuando giras se escuchar un rechinido o un ruido fuerte?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='direccion_1'),
        Estado(clave='volante_duro', valor='si'),
        Estado(clave='nivel_liquido', valor='si'))
    def diagnostico_sistema_de_transmision_embrague(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falta liquido de direccion en el deposito",
            'solucion': "Rellenar el liquido faltante",
            'severidad': "Alta"
        })
    
    @Rule(Sistema(area='direccion_1'),
        Estado(clave='volante_duro', valor='si'),
        Estado(clave='ruido_bomba', valor='si'))
    def diagnostico_sistema_de_transmision_aceite(self):
        self.diagnosticos_encontrados.append({
            'causa': "La bomba de direccion asistida esta fallando",
            'solucion': "Cambiar la bomba de direccion",
            'severidad': "Alta"
        })