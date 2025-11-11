from experta import *
from core.base import SistemaBase
from hechos import *

### Para el síntoma "no_enfria"
class SistemaAcondicionado1(SistemaBase):
    def __init__(self):
        super().__init__()

    # Activación del diagnóstico de aire acondicionado
    @Rule(Sistema(area='acondicionado_1'))
    def iniciar_diagnostico_motor(self):
        print("Iniciando diagnóstico: Sistema Aire Acondicionado 1")

    # Paso 1: Preguntar temperatura de las lineas
    @Rule(Sistema(area='acondicionado_1'),
        NOT(Estado(clave='temperatura_lineas')))
    def preguntar_temperatura_lineas(self):
        self.declare(Pregunta(
            clave='temperatura_lineas',
            texto="¿Las lineas del aire acondicionado están frías al tocarlas?",
            opciones=['si', 'no']
        ))

    # Paso 2: Preguntar por manchas de aceite
    @Rule(Sistema(area='acondicionado_1'),
        Estado(clave='temperatura_lineas', valor='si'),
        NOT(Estado(clave='manchas_conexiones')))
    def preguntar_manchas_conexiones(self):
        self.declare(Pregunta(
            clave='manchas_conexiones',
            texto="¿Se observan manchas de aceite en las conexiones del sistema?",
            opciones=['si', 'no']
        ))

    # Diagnóstico 1: Relleno de gas refrigerante
    @Rule(Sistema(area='acondicionado_1'),
        Estado(clave='temperatura_lineas', valor='no'))
    def diagnostico_relleno_gas_refrigerante(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falta de gas refrigerante",
            'solucion': "Rellenar el depósito de gas refrigerante",
            'severidad': "Baja"
        })

    # Diagnóstico 2: Fuga de sistema de refrigeracion
    @Rule(Sistema(area='acondicionado_1'),
        Estado(clave='temperatura_lineas', valor='si'),
        Estado(clave='manchas_conexiones', valor='si'))
    def diagnostico_refrigeracion(self):
        self.diagnosticos_encontrados.append({
            'causa': "Fuga en el sistema de refrigeración",
            'solucion': "Localizar la fuga con detector de UV o nitrógeno, reparar o reemplazar el componente dañado.",
            'severidad': "Media"
        })
    
    # Diagnóstico 3: Otras causas
    @Rule(Sistema(area='acondicionado_1'),
        Estado(clave='temperatura_lineas', valor='si'),
        Estado(clave='manchas_conexiones', valor='no'))
    def diagnostico_otras_causas_no_enfria(self):
        self.diagnosticos_encontrados.append({
            'causa': "Otras causas posibles",
            'solucion': "Revisar otras posibles causas por las que sucede la falla",
            'severidad': "Media"
        })


### Para el síntoma "aire_huele_mal"
class SistemaAcondicionado2(SistemaBase):
    def __init__(self):
        super().__init__()

    # Activación del diagnóstico de aire acondicionado
    @Rule(Sistema(area='acondicionado_2'))
    def iniciar_diagnostico_motor(self):
        print("Iniciando diagnóstico: Sistema Aire Acondicionado 2")

    # Paso 1: Preguntar por el olor a humedad
    @Rule(Sistema(area='acondicionado_2'),
        NOT(Estado(clave='olor_humedad')))
    def preguntar_olor_humedad(self):
        self.declare(Pregunta(
            clave='olor_humedad',
            texto="¿Puede percibir olor a humedad al encender el sistema?",
            opciones=['si', 'no']
        ))

    # Paso 2: Preguntar por persistencia del olor
    @Rule(Sistema(area='acondicionado_2'),
        Estado(clave='olor_humedad', valor='no'),
        NOT(Estado(clave='persistencia_olor')))
    def preguntar_persistencia_olor(self):
        self.declare(Pregunta(
            clave='persistencia_olor',
            texto="¿Se percibe olor incluso después de reemplazar el filtro?",
            opciones=['si', 'no']
        ))

    # Diagnóstico 1: Filtro de aire sucio
    @Rule(Sistema(area='acondicionado_2'),
        Estado(clave='olor_humedad', valor='si'))
    def diagnostico_filtro_aire_sucio(self):
        self.diagnosticos_encontrados.append({
            'causa': "Filtro de aire sucio",
            'solucion': "Limpiar o reemplazar el filtro de aire",
            'severidad': "Baja"
        })

    # Diagnóstico 2: Evaporador sucio
    @Rule(Sistema(area='acondicionado_2'),
        Estado(clave='olor_humedad', valor='no'),
        Estado(clave='persistencia_olor', valor='si'))
    def diagnostico_evaporador_sucio(self):
        self.diagnosticos_encontrados.append({
            'causa': "Evaporador sucio",
            'solucion': "Limpiar o reemplazar el filtro de aire",
            'severidad': "Baja"
        })
    
    # Diagnóstico 3: Otras causas
    @Rule(Sistema(area='acondicionado_2'),
        Estado(clave='olor_humedad', valor='no'),
        Estado(clave='persistencia_olor', valor='no'))
    def diagnostico_otras_causas_aire_huele_mal(self):
        self.diagnosticos_encontrados.append({
            'causa': "Otras causas posibles",
            'solucion': "Revisar otras posibles causas por las que sucede la falla",
            'severidad': "Media"
        })

### Para el síntoma "compresor_no_arranca"
class SistemaAcondicionado3(SistemaBase):
    def __init__(self):
        super().__init__()

    # Activación del diagnóstico de aire acondicionado
    @Rule(Sistema(area='acondicionado_3'))
    def iniciar_diagnostico_motor(self):
        print("Iniciando diagnóstico: Sistema Aire Acondicionado 3")

    # Paso 1: Preguntar por embrague del compresor
    @Rule(Sistema(area='acondicionado_3'),
        NOT(Estado(clave='embrague_compresor')))
    def preguntar_embrague_compresor(self):
        self.declare(Pregunta(
            clave='embrague_compresor',
            texto="¿El embrague del compresor recibe señal eléctrica?",
            opciones=['si', 'no']
        ))

    # Paso 2: Preguntar por presión del sistema
    @Rule(Sistema(area='acondicionado_3'),
        Estado(clave='embrague_compresor', valor='si'),
        NOT(Estado(clave='presion_sistema')))
    def preguntar_presion_sistema(self):
        self.declare(Pregunta(
            clave='presion_sistema',
            texto="¿La presión del sistema está por debajo del mínimo requerido?",
            opciones=['si', 'no']
        ))

    # Diagnóstico 1: Problema eléctrico
    @Rule(Sistema(area='acondicionado_3'),
        Estado(clave='embrague_compresor', valor='no'))
    def diagnostico_problema_electrico_aire(self):
        self.diagnosticos_encontrados.append({
            'causa': "Problema eléctrico",
            'solucion': "Revisar fusibles, relés y cableado del circuito del compresor.",
            'severidad': "Media"
        })

    # Diagnóstico 2: Falta de presión
    @Rule(Sistema(area='acondicionado_3'),
        Estado(clave='embrague_compresor', valor='si'),
        Estado(clave='presion_sistema', valor='si'))
    def diagnostico_falta_de_presion_aire(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falta de presión de gas",
            'solucion': "Recarga de refrigerante después de localizar y reparar la fuga. Verificar presión del sistema con manómetros.",
            'severidad': "Media"
        })
    
    # Diagnóstico 3: Otras causas
    @Rule(Sistema(area='acondicionado_3'),
        Estado(clave='embrague_compresor', valor='si'),
        Estado(clave='presion_sistema', valor='no'))
    def diagnostico_otras_causas_compresor_no_arranca(self):
        self.diagnosticos_encontrados.append({
            'causa': "Otras causas posibles",
            'solucion': "Revisar otras posibles causas por las que sucede la falla",
            'severidad': "Media"
        })

### Para el síntoma "compresor_ruidos_anormales"
class SistemaAcondicionado4(SistemaBase):
    def __init__(self):
        super().__init__()

    # Activación del diagnóstico de aire acondicionado
    @Rule(Sistema(area='acondicionado_4'))
    def iniciar_diagnostico_motor(self):
        print("Iniciando diagnóstico: Sistema Aire Acondicionado 4")

    # Paso 1: Preguntar por el ruido metálico
    @Rule(Sistema(area='acondicionado_4'),
        NOT(Estado(clave='ruido_metalico_aire')))
    def preguntar_ruido_metalico_aire(self):
        self.declare(Pregunta(
            clave='ruido_metalico_aire',
            texto="¿Se escucha un ruido metálico en el compresor?",
            opciones=['si', 'no']
        ))

    # Paso 2: Preguntar por el ruido al encender
    @Rule(Sistema(area='acondicionado_4'),
        Estado(clave='ruido_metalico_aire', valor='no'),
        NOT(Estado(clave='ruido_encender_sistema')))
    def preguntar_ruido_encender_sistema(self):
        self.declare(Pregunta(
            clave='ruido_encender_sistema',
            texto="¿El ruido es solo al encender el sistema de aire acondicionado?",
            opciones=['si', 'no']
        ))

    # Diagnóstico 1: Cojinetes internos desgastados
    @Rule(Sistema(area='acondicionado_4'),
        Estado(clave='ruido_metalico_aire', valor='si'))
    def diagnostico_cojinetes_desgastados(self):
        self.diagnosticos_encontrados.append({
            'causa': "Cojinetes internos desgastados",
            'solucion': "Reemplazo completo del compresor y limpieza del sistema de refrigeración.",
            'severidad': "Alta"
        })

    # Diagnóstico 2: Falla en embrague de compresor
    @Rule(Sistema(area='acondicionado_4'),
        Estado(clave='ruido_metalico_aire', valor='no'),
        Estado(clave='ruido_encender_sistema', valor='si'))
    def diagnostico_falla_embrague_de_compresor(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falla en embrague de compresor",
            'solucion': "Reemplazo del embrague del compresor o del compresor completo si el embrague no se vende por separado.",
            'severidad': "Media"
        })
    
    # Diagnóstico 3: Otras causas
    @Rule(Sistema(area='acondicionado_4'),
        Estado(clave='ruido_metalico_aire', valor='no'),
        Estado(clave='ruido_encender_sistema', valor='no'))
    def diagnostico_otras_causas_compresor_ruidos_anormales(self):
        self.diagnosticos_encontrados.append({
            'causa': "Otras causas posibles",
            'solucion': "Revisar otras posibles causas por las que sucede la falla",
            'severidad': "Media"
        })