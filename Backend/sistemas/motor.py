from experta import *
from core.base import SistemaBase
from hechos import *

### Lista de síntomas principales del motor:
# el motor no arranca
# el motor se apaga
# el motor emite humo negro
# el motor emite humo azul
# el motor emite humo blanco
# el motor vibra excesivamente


class SistemaMotor(SistemaBase):
    def __init__(self):
        super().__init__()

    # Activación del diagnóstico de motor
    @Rule(Sistema(area='motor'))
    def iniciar_diagnostico_motor(self):
        print("Iniciando diagnóstico: Sistema Motor")

    ### Para el síntoma no_arranca

    # Paso 1: Preguntar sobre la batería
    @Rule(Sistema(area='motor'),
        Estado(clave='no_arranca', valor='si'),
        NOT(Estado(clave='bateria_cargada')))
    def preguntar_estado_bateria(self):
        self.declare(Pregunta(
            clave='bateria_cargada',
            texto="¿La batería está cargada (luces del tablero encienden normal)?",
            opciones=['si', 'no']
        ))

    # Paso 2: Si batería cargada, preguntar comportamiento del arranque
    @Rule(Sistema(area='motor'),
        Estado(clave='no_arranca', valor='si'),
        Estado(clave='bateria_cargada', valor='si'),
        NOT(Estado(clave='comportamiento_arranque')))
    def preguntar_comportamiento_arranque(self):
        self.declare(Pregunta(
            clave='comportamiento_arranque', 
            texto="¿Cómo se comporta el motor al intentar arrancar?",
            opciones=[
                'gira_muy_lentamente',
                'gira_normal_pero_no_explosiona', 
                'no_gira',
                'otro_comportamiento'
            ]
        ))

    # Diagnóstico 1: Batería descargada
    @Rule(Sistema(area='motor'),
        Estado(clave='no_arranca', valor='si'),
        Estado(clave='bateria_cargada', valor='no'))
    def diagnostico_bateria_descargada(self):
        self.diagnosticos_encontrados.append({
            'causa': "Batería descargada o conexiones sueltas",
            'solucion': "Cargar o reemplazar la batería, revisar terminales y conexiones",
            'severidad': "Media"
        })

    # Diagnóstico 2: Sistema de encendido
    @Rule(Sistema(area='motor'),
        Estado(clave='no_arranca', valor='si'),
        Estado(clave='bateria_cargada', valor='si'),
        Estado(clave='comportamiento_arranque', valor='gira_muy_lentamente'))
    def diagnostico_sistema_encendido(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falla en el sistema de encendido",
            'solucion': "Revisar bujías, cables de bujía, bobina de encendido y distribuidor",
            'severidad': "Alta"
        })

    # Diagnóstico 3: Suministro de combustible
    @Rule(Sistema(area='motor'),
        Estado(clave='no_arranca', valor='si'),
        Estado(clave='bateria_cargada', valor='si'),
        Estado(clave='comportamiento_arranque', valor='gira_normal_pero_no_explosiona'))
    def diagnostico_suministro_combustible(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falla en el suministro de combustible",
            'solucion': "Revisar bomba de combustible, filtro de combustible, inyectores y presión de combustible",
            'severidad': "Alta"
        })

    # Diagnóstico 4: Motor no gira
    @Rule(Sistema(area='motor'),
        Estado(clave='no_arranca', valor='si'),
        Estado(clave='bateria_cargada', valor='si'),
        Estado(clave='comportamiento_arranque', valor='no_gira'))
    def diagnostico_motor_no_gira(self):
        self.diagnosticos_encontrados.append({
            'causa': "Problema mecánico o eléctrico severo - motor no gira",
            'solucion': "Revisar motor de arranque, solenoide, cableado y compresión del motor",
            'severidad': "Alta"
        })

    # Diagnóstico 5: Otras causas
    @Rule(Sistema(area='motor'),
        Estado(clave='no_arranca', valor='si'),
        Estado(clave='bateria_cargada', valor='si'),
        Estado(clave='comportamiento_arranque', valor='otro_comportamiento'))
    def diagnostico_otras_causas_no_arranca(self):
        self.diagnosticos_encontrados.append({
            'causa': "Otras causas posibles",
            'solucion': "Revisar otras posibles causas por las que sucede la falla",
            'severidad': "Media"
        })

    ### Para el síntoma se_apaga

    # Paso 1: Preguntar por el tanque de combustible
    @Rule(Sistema(area='motor'),
          Estado(clave='se_apaga', valor='si'),
          NOT(Estado(clave='tiene_combustible')))
    def preguntar_tanque_combustible(self):
        self.declare(Pregunta(
            clave='tiene_combustible',
            texto='¿El tanque de combustible cuenta con combustible?',
            opciones=['si', 'no']
        ))

    # Paso 2: Preguntar como se comporta el motor
    @Rule(Sistema(area='motor'),
          Estado(clave='tiene_combustible', valor='si'),
          NOT(Estado(clave='comportamiento_motor')))
    def preguntar_comportamiento_motor(self):
        self.declare(Pregunta(
            clave='comportamiento_motor',
            texto='¿Como se comporta el motor?',
            opciones=[
                'se_escucha_zumbido',
                'el_motor_no_responde_al_acelerador',
                'otro_comportamiento'
                ]
        ))

    # Diagnóstico 1: Falta de combustible
    @Rule(Sistema(area='motor'),
          Estado(clave='tiene_combustible', valor='no'))
    def diagnostico_sin_combustible(self):
        self.diagnosticos_encontrados.append({
            'causa':'Falta de combustible',
            'solucion':'Suministrar combustible al auto',
            'severidad':'Baja'
        })

    # Diagnóstico 2: Falla en la bomba de combustible
    @Rule(Sistema(area='motor'),
          Estado(clave='tiene_combustible', valor='si'),
          Estado(clave='comportamiento_motor', valor='se_escucha_zumbido'))
    def diagnostico_bomba_combustible(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falla en la bomba de combustible",
            'solucion': "Reemplaza la bomba de combustible",
            'severidad': "Alta"
        })

    # Diagnóstico 3: Falla en sensor del cigüeñal
    @Rule(Sistema(area='motor'),
        Estado(clave='tiene_combustible', valor='si'),
        Estado(clave='comportamiento_motor', valor='el_motor_no_responde_al_acelerador'))
    def diagnostico_sensor_ciguenal(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falla en el sensor del cigüeñal",
            'solucion': "Reemplazar el sensor del cigüeñal",
            'severidad': "Moderada"
        })
    
    #Diagnóstico 4: Otras causas
    @Rule(Sistema(area='motor'),
          Estado(clave='tiene_combustible', valor='si'),
          Estado(clave='comportamiento_motor', valor='otro_comportamiento'))
    def diagnostico_otras_causas_se_apaga(self):
        self.diagnosticos_encontrados.append({
            'causa': "Otras causas posibles",
            'solucion': "Revisar otras posibles causas por las que sucede la falla",
            'severidad': "Media"
        })