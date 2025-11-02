from experta import *
from core.base import SistemaBase
from hechos import *

class SistemaMotor(SistemaBase):
    def __init__(self):
        super().__init__()

    # Activación del diagnóstico de motor
    @Rule(Sistema(area='motor'))
    def iniciar_diagnostico_motor(self):
        print("Iniciando diagnóstico: Sistema Motor")

    # Paso 1: Preguntar sobre la batería
    @Rule(Sistema(area='motor'),
          NOT(Estado(clave='bateria_cargada')))
    def preguntar_estado_bateria(self):
        self.declare(Pregunta(
            clave='bateria_cargada',
            texto="¿La batería está cargada (luces del tablero encienden normal)?",
            opciones=['si', 'no']
        ))
    
    # Paso 2: Si batería cargada, preguntar cómo gira el motor
    @Rule(Sistema(area='motor'),
          Estado(clave='bateria_cargada', valor='si'),
          NOT(Estado(clave='motor_gira')))
    def preguntar_giro_motor(self):
        self.declare(Pregunta(
            clave='motor_gira', 
            texto="¿Cómo reacciona el motor al girar la llave?",
            opciones=['gira_lento', 'no_gira']
        ))

    # Diagnóstico 1: Sistema de encendido
    @Rule(Sistema(area='motor'),
          Estado(clave='bateria_cargada', valor='si'),
          Estado(clave='motor_gira', valor='gira_lento'))
    def diagnostico_sistema_encendido(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falla en el sistema de encendido",
            'solucion': "Revisar bujías, cables de bujía, bobina de encendido y distribuidor",
            'severidad': "Alta"
        })

    # Diagnóstico 2: Batería descargada
    @Rule(Sistema(area='motor'),
          Estado(clave='bateria_cargada', valor='no'))
    def diagnostico_bateria_descargada(self):
        self.diagnosticos_encontrados.append({
            'causa': "Batería descargada o conexiones sueltas",
            'solucion': "Cargar batería o revisar terminales y conexiones",
            'severidad': "Media"
        })