from experta import *
from core.base import SistemaBase
from hechos import *

### Para el síntoma "nivel_aceite_bajo"
class SistemaFluidos1(SistemaBase):
    def __init__(self):
        super().__init__()

    # Activación del diagnóstico de escape
    @Rule(Sistema(area='fluidos_1'))
    def iniciar_diagnostico_motor(self):
        print("Iniciando diagnóstico: Sistema Fluidos 1")

    # Paso 1: Preguntar por manchas de aceite
    @Rule(Sistema(area='fluidos_1'),
        NOT(Estado(clave='manchas_aceite')))
    def preguntar_manchas_aceite(self):
        self.declare(Pregunta(
            clave='manchas_aceite',
            texto="¿Puede ver manchas de aceite bajo el vehículo?",
            opciones=['si', 'no']
        ))

    # Diagnóstico 1: Relleno de aceite
    @Rule(Sistema(area='fluidos_1'),
        Estado(clave='manchas_aceite', valor='no'))
    def diagnostico_relleno_aceite(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falta de aceite",
            'solucion': "Rellenar el depósito de aceite",
            'severidad': "Media"
        })

    # Diagnóstico 2: Fuga de aceite
    @Rule(Sistema(area='fluidos_1'),
        Estado(clave='manchas_aceite', valor='si'))
    def diagnostico_fuga_aceite(self):
        self.diagnosticos_encontrados.append({
            'causa': "Fuga de aceite",
            'solucion': "Identificar fuente de la fuga y reemplazar empaques defectuosos.",
            'severidad': "Alta"
        })

### Para el síntoma "liquido_de_frenos_bajo"
class SistemaFluidos2(SistemaBase):
    def __init__(self):
        super().__init__()

    # Activación del diagnóstico de fluidos
    @Rule(Sistema(area='fluidos_2'))
    def iniciar_diagnostico_motor(self):
        print("Iniciando diagnóstico: Sistema Fluidos 2")

    # Paso 1: Preguntar sobre la disminución temporal del líquido
    @Rule(Sistema(area='fluidos_2'),
        NOT(Estado(clave='disminución_liquido')))
    def preguntar_disminución_liquido(self):
        self.declare(Pregunta(
            clave='disminución_liquido',
            texto="¿El nivel del líquido baja consistentemente con el tiempo?",
            opciones=['si', 'no']
        ))

    # Paso 2: Preguntar sobre el pedal
    @Rule(Sistema(area='fluidos_2'),
        Estado(clave='disminución_liquido', valor='no'),
        NOT(Estado(clave='pedal_esponjoso_freno')))
    def preguntar_pedal_esponjoso_freno(self):
        self.declare(Pregunta(
            clave='pedal_esponjoso_freno',
            texto="¿El pedal de freno se siente esponjoso al pisarlo?",
            opciones=['si', 'no']
        ))

    # Diagnóstico 1: Fuga en el sistema de frenos
    @Rule(Sistema(area='fluidos_2'),
        Estado(clave='disminución_liquido', valor='si'))
    def diagnostico_fuga_sistema_frenos(self):
        self.diagnosticos_encontrados.append({
            'causa': "Fuga en el sistema de frenos",
            'solucion': "Detener inmediatamente el vehículo. Reemplazar líneas de freno, cilindros o mordazas defectuosas.",
            'severidad': "Alta"
        })

    # Diagnóstico 2: Contaminación en el sistema hidráulico
    @Rule(Sistema(area='fluidos_2'),
        Estado(clave='disminución_liquido', valor='no'),
        Estado(clave='pedal_esponjoso_freno', valor='si'))
    def diagnostico_contaminacion_hidraulica(self):
        self.diagnosticos_encontrados.append({
            'causa': "Contaminación en el sistema hidráulico",
            'solucion': "Vaciado y relleno coompleto del sistema. Purgar todas las líneas hasta que salga líquido limpio.",
            'severidad': "Alta"
        })

    # Diagnóstico 3: Otras causas
    @Rule(Sistema(area='fluidos_2'),
        Estado(clave='disminución_liquido', valor='no'),
        Estado(clave='pedal_esponjoso_freno', valor='no'))
    def diagnostico_otras_causas_liquido_de_frenos_bajo(self):
        self.diagnosticos_encontrados.append({
            'causa': "Otras causas posibles",
            'solucion': "Revisar otras posibles causas por las que sucede la falla",
            'severidad': "Media"
        })

### Para el síntoma "refrigerante_marron"
class SistemaFluidos3(SistemaBase):
    def __init__(self):
        super().__init__()

    # Activación del diagnóstico de fluidos
    @Rule(Sistema(area='fluidos_3'))
    def iniciar_diagnostico_motor(self):
        print("Iniciando diagnóstico: Sistema Fluidos 3")

    # Paso 1: Preguntar depósitos de óxido en el radiador
    @Rule(Sistema(area='fluidos_3'),
        NOT(Estado(clave='oxido_radiador')))
    def preguntar_oxido_radiador(self):
        self.declare(Pregunta(
            clave='oxido_radiador',
            texto="¿Puede observar depósitos de óxido en el radiador?",
            opciones=['si', 'no']
        ))

    # Paso 2: Preguntar por sobrecalentamiento
    @Rule(Sistema(area='fluidos_3'),
        Estado(clave='oxido_radiador', valor='no'),
        NOT(Estado(clave='sobrecalentamiento_motor')))
    def preguntar_sobrecalentamiento_motor(self):
        self.declare(Pregunta(
            clave='sobrecalentamiento_motor', 
            texto="¿El motor muestra señales de sobrecalentamiento?",
            opciones=['si','no']
        ))

    # Diagnóstico 1: Limpieza en sistemas de enfriamiento
    @Rule(Sistema(area='fluidos_3'),
        Estado(clave='oxido_radiador', valor='si'))
    def diagnostico_limpieza_enfriamiento(self):
        self.diagnosticos_encontrados.append({
            'causa': "Suciedad en el sistema de enfriamiento",
            'solucion': "Limpiar el sistema de enfriamiento (radiador, etc.).",
            'severidad': "Media"
        })

    # Diagnóstico 2: Contaminación por óxido
    @Rule(Sistema(area='fluidos_3'),
        Estado(clave='oxido_radiador', valor='no'),
        Estado(clave='sobrecalentamiento_motor', valor='si'))
    def diagnostico_contaminacion_oxido(self):
        self.diagnosticos_encontrados.append({
            'causa': "Contaminación por óxido",
            'solucion': "Lavado completo del sistema con productos desincrustantes, reemplazo del líquido refrigerante.",
            'severidad': "Alta"
        })

    # Diagnóstico 3: Otras causas
    @Rule(Sistema(area='fluidos_3'),
        Estado(clave='oxido_radiador', valor='no'),
        Estado(clave='sobrecalentamiento_motor', valor='no'))
    def diagnostico_otras_causas_refrigerante_marron(self):
        self.diagnosticos_encontrados.append({
            'causa': "Otras causas posibles",
            'solucion': "Revisar otras posibles causas por las que sucede la falla",
            'severidad': "Media"
        })

### Para el síntoma "liquido_direccion_oscuro"
class SistemaFluidos4(SistemaBase):
    def __init__(self):
        super().__init__()

    # Activación del diagnóstico de fluidos
    @Rule(Sistema(area='fluidos_4'))
    def iniciar_diagnostico_motor(self):
        print("Iniciando diagnóstico: Sistema Fluidos 4")

    # Paso 1: Preguntar por olor a quemado
    @Rule(Sistema(area='fluidos_4'),
        NOT(Estado(clave='olor_quemado')))
    def preguntar_olor_quemado(self):
        self.declare(Pregunta(
            clave='olor_quemado',
            texto="¿Puede percibir un olor a quemado?",
            opciones=['si', 'no']
        ))

    # Paso 2: Preguntar por ruido de direccion
    @Rule(Sistema(area='fluidos_4'),
        Estado(clave='olor_quemado', valor='no'),
        NOT(Estado(clave='ruido_direccion')))
    def preguntar_ruido_direccion(self):
        self.declare(Pregunta(
            clave='ruido_direccion', 
            texto="¿Puede escuchar ruidos provenientes de la dirección?",
            opciones=['si','no']
        ))

    # Diagnóstico 1: Fallo en bomba de dirección
    @Rule(Sistema(area='fluidos_4'),
        Estado(clave='olor_quemado', valor='si'))
    def diagnostico_fallo_bomba_direccion(self):
        self.diagnosticos_encontrados.append({
            'causa': "Fallo en bomba de dirección",
            'solucion': "Cambio inmediato del líquido de dirección hidráulica. Limpieza del sistema y revisión de la bomba de dirección por posibles daños internos.",
            'severidad': "Alta"
        })

    # Diagnóstico 2: Pérdida de propiedades lubricantes
    @Rule(Sistema(area='fluidos_4'),
        Estado(clave='olor_quemado', valor='no'),
        Estado(clave='ruido_direccion', valor='si'))
    def diagnostico_propiedades_lubricantes(self):
        self.diagnosticos_encontrados.append({
            'causa': "Pérdida de propiedades lubricantes",
            'solucion': "Reemplazo del líquido de dirección hidráulica.",
            'severidad': "Baja"
        })

    # Diagnóstico 3: Otras causas
    @Rule(Sistema(area='fluidos_4'),
        Estado(clave='olor_quemado', valor='no'),
        Estado(clave='ruido_direccion', valor='no'))
    def diagnostico_otras_causas_liquido_direccion_oscuro(self):
        self.diagnosticos_encontrados.append({
            'causa': "Otras causas posibles",
            'solucion': "Revisar otras posibles causas por las que sucede la falla",
            'severidad': "Media"
        })