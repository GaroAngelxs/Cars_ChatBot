from experta import *
from core.base import SistemaBase
from hechos import *

class SistemaSuspension1(SistemaBase):
    def __init__(self):
        super().__init__()

    @Rule(Sistema(area='suspension_1'))
    def iniciar_diagnostico_transmision(self):
        print("Iniciando diagnóstico: Sistema Suspension")

    @Rule(Sistema(area='suspension_1'),
        NOT(Estado(clave='volante_vibra_alta_velocidad')))
    def preguntar_si_cambios_entran(self):
        self.declare(Pregunta(  
            clave='volante_vibra_alta_velocidad',
            texto="¿El volante vibra a alta velocidad?",
            opciones=['si', 'no']
        ))
    
    @Rule(Sistema(area='suspension_1'),
        Estado(clave='volante_vibra_alta_velocidad', valor='si'),
        NOT(Estado(clave='vibracion_progresiva')))
    def preguntar_recorrido_del_pedal(self):
        self.declare(Pregunta(
            clave='vibracion_progresiva',
            texto="¿La vibracion es progresiva? Es decir, entre mas velocidad mas vibra",
            opciones=['si', 'no']
        ))
 
    @Rule(Sistema(area='suspension_1'),
        Estado(clave='volante_vibra_alta_velocidad', valor='si'),
        Estado(clave='vibracion_progresiva', valor='no'),
        NOT(Estado(clave='volante_juego')))
    def preguntar_color_olor_del_aceite(self):
        self.declare(Pregunta(
            clave='volante_juego',
            texto="¿Al sacudir el volante se siente como si estuviera suelto?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='suspension_1'),
        Estado(clave='volante_vibra_alta_velocidad', valor='si'),
        Estado(clave='vibracion_progresiva', valor='si'))
    def diagnostico_sistema_de_transmision_embrague(self):
        self.diagnosticos_encontrados.append({
            'causa': "Desbalance en las ruedas",
            'solucion': "Balancear las ruedas",
            'severidad': "Alta"
        })
    
    @Rule(Sistema(area='suspension_1'),
        Estado(clave='volante_vibra_alta_velocidad', valor='si'),
        Estado(clave='volante_juego', valor='si'))
    def diagnostico_sistema_de_transmision_aceite(self):
        self.diagnosticos_encontrados.append({
            'causa': "Desgaste en las terminales de la direccion",
            'solucion': "Cambiar las terminales de la direccion",
            'severidad': "Alta"
        })

