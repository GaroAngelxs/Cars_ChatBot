from experta import *
from core.base import SistemaBase
from hechos import *

#  SISTEMA DE DIRECCIÓN 1
#  Diagnostica un volante duro y problemas de dirección asistida
class SistemaDireccion1(SistemaBase):
    def __init__(self):
        super().__init__()

    # Regla inicial: se activa cuando el sistema seleccionado es "direccion_1"
    @Rule(Sistema(area='direccion_1'))
    def iniciar_diagnostico_transmision(self):
        print("Iniciando diagnóstico: Sistema Dirección")

    # Pregunta principal: si el volante se siente duro al girar
    @Rule(Sistema(area='direccion_1'),
        NOT(Estado(clave='volante_duro')))
    def preguntar_si_cambios_entran(self):
        self.declare(Pregunta(
            clave='volante_duro',
            texto="¿El volante se siente duro al girar?",
            opciones=['si', 'no']
        ))
    
    # Si el volante está duro, preguntar por el nivel del líquido de dirección
    @Rule(Sistema(area='direccion_1'),
        Estado(clave='volante_duro', valor='si'),
        NOT(Estado(clave='nivel_liquido')))
    def preguntar_recorrido_del_pedal(self):
        self.declare(Pregunta(
            clave='nivel_liquido',
            texto="¿El nivel de líquido de dirección está debajo del mínimo?",
            opciones=['si', 'no']
        ))
 
    # Si el nivel está bien, preguntar si hay ruido en la bomba al girar
    @Rule(Sistema(area='direccion_1'),
        Estado(clave='volante_duro', valor='si'),
        Estado(clave='nivel_liquido', valor='no'),
        NOT(Estado(clave='ruido_bomba')))
    def preguntar_color_olor_del_aceite(self):
        self.declare(Pregunta(
            clave='ruido_bomba',
            texto="¿Cuando giras se escucha un rechinido o un ruido fuerte?",
            opciones=['si', 'no']
        ))

    # Diagnóstico: Falta de líquido de dirección
    @Rule(Sistema(area='direccion_1'),
        Estado(clave='volante_duro', valor='si'),
        Estado(clave='nivel_liquido', valor='si'))
    def diagnostico_sistema_de_transmision_embrague(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falta líquido de dirección en el depósito",
            'solucion': "Rellenar el líquido faltante",
            'severidad': "Alta"
        })
    
    # Diagnóstico: Bomba de dirección asistida fallando
    @Rule(Sistema(area='direccion_1'),
        Estado(clave='volante_duro', valor='si'),
        Estado(clave='ruido_bomba', valor='si'))
    def diagnostico_sistema_de_transmision_aceite(self):
        self.diagnosticos_encontrados.append({
            'causa': "La bomba de dirección asistida está fallando",
            'solucion': "Cambiar la bomba de dirección",
            'severidad': "Alta"
        })
