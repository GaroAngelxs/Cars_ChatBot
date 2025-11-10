from experta import *
from core.base import SistemaBase
from hechos import *

### Para el síntoma "no_arranca"
class SistemaMotor1(SistemaBase):
    def __init__(self):
        super().__init__()

    # Activación del diagnóstico de motor
    @Rule(Sistema(area='motor_1'))
    def iniciar_diagnostico_motor(self):
        print("Iniciando diagnóstico: Sistema Motor 1")

    # Paso 1: Preguntar sobre la batería
    @Rule(Sistema(area='motor_1'),
        NOT(Estado(clave='bateria_cargada')))
    def preguntar_estado_bateria(self):
        self.declare(Pregunta(
            clave='bateria_cargada',
            texto="¿La batería está cargada (luces del tablero encienden normal)?",
            opciones=['si', 'no']
        ))

    # Paso 2: Si batería cargada, preguntar comportamiento del arranque
    @Rule(Sistema(area='motor_1'),
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
    @Rule(Sistema(area='motor_1'),
        Estado(clave='bateria_cargada', valor='no'))
    def diagnostico_bateria_descargada(self):
        self.diagnosticos_encontrados.append({
            'causa': "Batería descargada o conexiones sueltas",
            'solucion': "Cargar o reemplazar la batería, revisar terminales y conexiones",
            'severidad': "Media"
        })

    # Diagnóstico 2: Sistema de encendido
    @Rule(Sistema(area='motor_1'),
        Estado(clave='bateria_cargada', valor='si'),
        Estado(clave='comportamiento_arranque', valor='gira_muy_lentamente'))
    def diagnostico_sistema_encendido(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falla en el sistema de encendido",
            'solucion': "Revisar bujías, cables de bujía, bobina de encendido y distribuidor",
            'severidad': "Alta"
        })

    # Diagnóstico 3: Suministro de combustible
    @Rule(Sistema(area='motor_1'),
        Estado(clave='bateria_cargada', valor='si'),
        Estado(clave='comportamiento_arranque', valor='gira_normal_pero_no_explosiona'))
    def diagnostico_suministro_combustible(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falla en el suministro de combustible",
            'solucion': "Revisar bomba de combustible, filtro de combustible, inyectores y presión de combustible",
            'severidad': "Alta"
        })

    # Diagnóstico 4: Motor no gira
    @Rule(Sistema(area='motor_1'),
        Estado(clave='bateria_cargada', valor='si'),
        Estado(clave='comportamiento_arranque', valor='no_gira'))
    def diagnostico_motor_no_gira(self):
        self.diagnosticos_encontrados.append({
            'causa': "Problema mecánico o eléctrico severo - motor no gira",
            'solucion': "Revisar motor de arranque, solenoide, cableado y compresión del motor",
            'severidad': "Alta"
        })

    # Diagnóstico 5: Otras causas
    @Rule(Sistema(area='motor_1'),
        Estado(clave='bateria_cargada', valor='si'),
        Estado(clave='comportamiento_arranque', valor='otro_comportamiento'))
    def diagnostico_otras_causas_no_arranca(self):
        self.diagnosticos_encontrados.append({
            'causa': "Otras causas posibles",
            'solucion': "Revisar otras posibles causas por las que sucede la falla",
            'severidad': "Media"
        })

### Para el síntoma "se_apaga"
class SistemaMotor2(SistemaBase):
    def __init__(self):
        super().__init__()

    # Activación del diagnóstico de motor
    @Rule(Sistema(area='motor_2'))
    def iniciar_diagnostico_motor(self):
        print("Iniciando diagnóstico: Sistema Motor 2")

    # Paso 1: Preguntar por el tanque de combustible
    @Rule(Sistema(area='motor_2'),
          NOT(Estado(clave='tiene_combustible')))
    def preguntar_tanque_combustible(self):
        self.declare(Pregunta(
            clave='tiene_combustible',
            texto='¿El tanque de combustible cuenta con combustible?',
            opciones=['si', 'no']
        ))

    # Paso 2: Preguntar como se comporta el motor
    @Rule(Sistema(area='motor_2'),
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
    @Rule(Sistema(area='motor_2'),
          Estado(clave='tiene_combustible', valor='no'))
    def diagnostico_sin_combustible(self):
        self.diagnosticos_encontrados.append({
            'causa':'Falta de combustible',
            'solucion':'Suministrar combustible al auto',
            'severidad':'Baja'
        })

    # Diagnóstico 2: Falla en la bomba de combustible
    @Rule(Sistema(area='motor_2'),
          Estado(clave='tiene_combustible', valor='si'),
          Estado(clave='comportamiento_motor', valor='se_escucha_zumbido'))
    def diagnostico_bomba_combustible(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falla en la bomba de combustible",
            'solucion': "Reemplaza la bomba de combustible",
            'severidad': "Alta"
        })

    # Diagnóstico 3: Falla en sensor del cigüeñal
    @Rule(Sistema(area='motor_2'),
        Estado(clave='tiene_combustible', valor='si'),
        Estado(clave='comportamiento_motor', valor='el_motor_no_responde_al_acelerador'))
    def diagnostico_sensor_ciguenal(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falla en el sensor del cigüeñal",
            'solucion': "Reemplazar el sensor del cigüeñal",
            'severidad': "Moderada"
        })
    
    #Diagnóstico 4: Otras causas
    @Rule(Sistema(area='motor_2'),
          Estado(clave='tiene_combustible', valor='si'),
          Estado(clave='comportamiento_motor', valor='otro_comportamiento'))
    def diagnostico_otras_causas_se_apaga(self):
        self.diagnosticos_encontrados.append({
            'causa': "Otras causas posibles",
            'solucion': "Revisar otras posibles causas por las que sucede la falla",
            'severidad': "Media"
        })

### Para el síntoma "emite_humo_negro"
class SistemaMotor3(SistemaBase):
    def __init__(self):
        super().__init__()

    # Activación del diagnóstico de motor
    @Rule(Sistema(area='motor_3'))
    def iniciar_diagnostico_motor(self):
        print("Iniciando diagnóstico: Sistema Motor 3")

    # Paso 1: Preguntar por el consumo de combustible
    @Rule(Sistema(area='motor_3'),
          NOT(Estado(clave='consumo_combustible')))
    def preguntar_consumo_combustible(self):
        self.declare(Pregunta(
            clave='consumo_combustible',
            texto='¿Ha notado un aumento en el consumo de combustible?',
            opciones=['si', 'no']
        ))

    # Paso 2: Preguntar por la potencia del motor
    @Rule(Sistema(area='motor_3'),
          Estado(clave='consumo_combustible', valor='no'),
          NOT(Estado(clave='potencia_motor')))
    def preguntar_potencia_motor(self):
        self.declare(Pregunta(
            clave='potencia_motor',
            texto='¿Ha notado pérdida de potencia en el motor?',
            opciones=[
                'si',
                'no'
                ]
        ))

    # Diagnóstico 1: Exceso de combustible
    @Rule(Sistema(area='motor_3'),
          Estado(clave='consumo_combustible', valor='si'))
    def diagnostico_exceso_combustible(self):
        self.diagnosticos_encontrados.append({
            'causa':'Exceso de combustible',
            'solucion':'Revisar sensor de oxígeno y el sistema de inyección',
            'severidad':'Media'
        })

    # Diagnóstico 2: Filtro de aire sucio
    @Rule(Sistema(area='motor_3'),
          Estado(clave='consumo_combustible', valor='no'),
          Estado(clave='potencia_motor', valor='si'))
    def diagnostico_filtro_aire(self):
        self.diagnosticos_encontrados.append({
            'causa': "Filtro de aire sucio",
            'solucion': "Reemplaza o limpia el filtro de aire",
            'severidad': "Media"
        })
    
    #Diagnóstico 3: Otras causas
    @Rule(Sistema(area='motor_3'),
          Estado(clave='consumo_combustible', valor='no'),
          Estado(clave='potencia_motor', valor='no'))
    def diagnostico_otras_causas_humo_negro(self):
        self.diagnosticos_encontrados.append({
            'causa': "Otras causas posibles",
            'solucion': "Revisar otras posibles causas por las que sucede la falla",
            'severidad': "Media"
        })

### Para el síntoma "emite_humo_azul"
class SistemaMotor4(SistemaBase):
    def __init__(self):
        super().__init__()

    # Activación del diagnóstico de motor
    @Rule(Sistema(area='motor_4'))
    def iniciar_diagnostico_motor(self):
        print("Iniciando diagnóstico: Sistema Motor 4")

    # Paso 1: Preguntar por el nivel de aceite
    @Rule(Sistema(area='motor_4'),
          NOT(Estado(clave='nivel_aceite')))
    def preguntar_nivel_aceite(self):
        self.declare(Pregunta(
            clave='nivel_aceite',
            texto='¿Ha notado una disminución en el nivel de aceite?',
            opciones=['si', 'no']
        ))

    # Paso 2: Preguntar por la compresión en los cilindros
    @Rule(Sistema(area='motor_4'),
          Estado(clave='nivel_aceite', valor='no'),
          NOT(Estado(clave='compresion_cilindros')))
    def preguntar_compresion_cilindros(self):
        self.declare(Pregunta(
            clave='compresion_cilindros',
            texto='¿Ha notado baja compresión en los cilindros?',
            opciones=[
                'si',
                'no'
                ]
        ))

    # Diagnóstico 1: Quema de aceite
    @Rule(Sistema(area='motor_4'),
          Estado(clave='nivel_aceite', valor='si'))
    def diagnostico_quema_aceite(self):
        self.diagnosticos_encontrados.append({
            'causa':'Quema de aceite',
            'solucion':'Revisar sellos o desgaste en válvulas',
            'severidad':'Alta'
        })

    # Diagnóstico 2: Anillos desgastados
    @Rule(Sistema(area='motor_4'),
          Estado(clave='nivel_aceite', valor='no'),
          Estado(clave='compresion_cilindros', valor='si'))
    def diagnostico_anillos_desgastados(self):
        self.diagnosticos_encontrados.append({
            'causa': "Anillos desgastados",
            'solucion': "Reemplaza los anillos de los pistones",
            'severidad': "Alta"
        })
    
    #Diagnóstico 3: Otras causas
    @Rule(Sistema(area='motor_4'),
          Estado(clave='nivel_aceite', valor='no'),
          Estado(clave='compresion_cilindros', valor='no'))
    def diagnostico_otras_causas_humo_azul(self):
        self.diagnosticos_encontrados.append({
            'causa': "Otras causas posibles",
            'solucion': "Revisar otras posibles causas por las que sucede la falla",
            'severidad': "Media"
        })

### Para el síntoma "emite_humo_blanco"
class SistemaMotor5(SistemaBase):
    def __init__(self):
        super().__init__()

    # Activación del diagnóstico de motor
    @Rule(Sistema(area='motor_5'))
    def iniciar_diagnostico_motor(self):
        print("Iniciando diagnóstico: Sistema Motor 5")

    # Paso 1: Preguntar por el nivel de refrigerante
    @Rule(Sistema(area='motor_5'),
          NOT(Estado(clave='nivel_refrigerante')))
    def preguntar_nivel_refrigerante(self):
        self.declare(Pregunta(
            clave='nivel_refrigerante',
            texto='¿Ha notado una disminución en el nivel de refrigerante?',
            opciones=['si', 'no']
        ))

    # Diagnóstico 1: Fuga de refrigerante
    @Rule(Sistema(area='motor_5'),
          Estado(clave='nivel_refrigerante', valor='si'))
    def diagnostico_fuga_refrigerante(self):
        self.diagnosticos_encontrados.append({
            'causa':'Fuga de refrigerante',
            'solucion':'Reemplazar la junta de culata quemada o reparar la culata agrietada. ',
            'severidad':'Alta'
        })
    
    #Diagnóstico 2: Otras causas
    @Rule(Sistema(area='motor_5'),
          Estado(clave='nivel_refrigerante', valor='no'))
    def diagnostico_otras_causas_humo_blanco(self):
        self.diagnosticos_encontrados.append({
            'causa': "Otras causas posibles",
            'solucion': "Revisar otras posibles causas por las que sucede la falla",
            'severidad': "Media"
        })

### Para el síntoma "vibra_excesivamente"
class SistemaMotor6(SistemaBase):
    def __init__(self):
        super().__init__()

    # Activación del diagnóstico de motor
    @Rule(Sistema(area='motor_6'))
    def iniciar_diagnostico_motor(self):
        print("Iniciando diagnóstico: Sistema Motor 6")

    # Paso 1: Preguntar por la desaparición de la falla a altas revoluciones
    @Rule(Sistema(area='motor_6'),
          NOT(Estado(clave='altas_revoluciones')))
    def preguntar_altas_revoluciones(self):
        self.declare(Pregunta(
            clave='altas_revoluciones',
            texto='¿La falla desaparece al aumentar las revoluciones?',
            opciones=['si', 'no']
        ))

    # Paso 2: Preguntar por golpes metálicos a altas revoluciones
    @Rule(Sistema(area='motor_6'),
          Estado(clave='altas_revoluciones', valor='no'),
          NOT(Estado(clave='golpes_metalicos')))
    def preguntar_golpes_metalicos(self):
        self.declare(Pregunta(
            clave='golpes_metalicos',
            texto='¿Se escuchan golpes metálicos al aumentar las revoluciones?',
            opciones=[
                'si',
                'no'
                ]
        ))

    # Diagnóstico 1: Bujías sucias
    @Rule(Sistema(area='motor_6'),
          Estado(clave='altas_revoluciones', valor='si'))
    def diagnostico_bujias_sucias(self):
        self.diagnosticos_encontrados.append({
            'causa':'Bujías sucias',
            'solucion':'Limpia las bujías del motor',
            'severidad':'Baja'
        })

    # Diagnóstico 2: Falla de cilindro
    @Rule(Sistema(area='motor_6'),
          Estado(clave='altas_revoluciones', valor='no'),
          Estado(clave='golpes_metalicos', valor='si'))
    def diagnostico_falla_cilindro(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falla en el cilindro",
            'solucion': "Reemplaza las bujías y revisa los inyectores de combustible",
            'severidad': "Alta"
        })
    
    #Diagnóstico 2: Otras causas
    @Rule(Sistema(area='motor_6'),
          Estado(clave='altas_revoluciones', valor='no'),
          Estado(clave='golpes_metalicos', valor='no'))
    def diagnostico_otras_causas_vibra_excesivamente(self):
        self.diagnosticos_encontrados.append({
            'causa': "Otras causas posibles",
            'solucion': "Revisar otras posibles causas por las que sucede la falla",
            'severidad': "Media"
        })