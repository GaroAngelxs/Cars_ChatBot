from experta import *
from core.base import SistemaBase
from hechos import *

### Para el síntoma "ruido_fuerte_escape"
class SistemaEscape1(SistemaBase):
    def __init__(self):
        super().__init__()

    # Activación del diagnóstico de escape
    @Rule(Sistema(area='escape_1'))
    def iniciar_diagnostico_motor(self):
        print("Iniciando diagnóstico: Sistema Escape 1")

    # Paso 1: Preguntar sobre comportamiento del sonido
    @Rule(Sistema(area='escape_1'),
        NOT(Estado(clave='comportamiento_sonido')))
    def preguntar_comportamiento_sonido(self):
        self.declare(Pregunta(
            clave='comportamiento_sonido',
            texto="¿Cómo se comporta el sonido del escape?",
            opciones=['traqueteo_metalico_en_el_frente', 'sonido_grave_en_parte_trasera', 'otro_comportamiento']
        ))

    # Diagnóstico 1: Fuga múltiple
    @Rule(Sistema(area='escape_1'),
        Estado(clave='comportamiento_sonido', valor='traqueteo_metalico_en_el_frente'))
    def diagnostico_fuga_múltiple(self):
        self.diagnosticos_encontrados.append({
            'causa': "Fuga múltiple de escape o tubo frontal",
            'solucion': "Reemplazar el tramo afectado o soldar la zona afectada",
            'severidad': "Alta"
        })

    # Diagnóstico 2: Ruptura en el silenciador
    @Rule(Sistema(area='escape_1'),
        Estado(clave='comportamiento_sonido', valor='sonido_grave_en_parte_trasera'))
    def diagnostico_ruptura_silenciador(self):
        self.diagnosticos_encontrados.append({
            'causa': "Ruptura en el silenciador",
            'solucion': "Reemplazar el silenciador dañado o repararlo mediante soldadura",
            'severidad': "Media"
        })

    # Diagnóstico 3: Otras causas
    @Rule(Sistema(area='escape_1'),
        Estado(clave='comportamiento_sonido', valor='otro_comportamiento'))
    def diagnostico_otras_causas_ruido_fuerte_escape(self):
        self.diagnosticos_encontrados.append({
            'causa': "Otras causas posibles",
            'solucion': "Revisar otras posibles causas por las que sucede la falla",
            'severidad': "Media"
        })

### Para el síntoma "olor_a_gases"
class SistemaEscape2(SistemaBase):
    def __init__(self):
        super().__init__()

    # Activación del diagnóstico de escape
    @Rule(Sistema(area='escape_2'))
    def iniciar_diagnostico_motor(self):
        print("Iniciando diagnóstico: Sistema Escape 2")

    # Paso 1: Preguntar sobre la intensidad del olor al detenerse
    @Rule(Sistema(area='escape_2'),
        NOT(Estado(clave='intensidad_olor')))
    def preguntar_intensidad_olor(self):
        self.declare(Pregunta(
            clave='intensidad_olor',
            texto="¿El olor es más intenso al detenerse o con las ventanas cerradas?",
            opciones=['si', 'no']
        ))

    # Paso 2: Preguntar sobre la fuente del olor en el aire acondicionado
    @Rule(Sistema(area='escape_2'),
        Estado(clave='intensidad_olor', valor='no'),
        NOT(Estado(clave='aire_acondicionado')))
    def preguntar_aire_acondicionado(self):
        self.declare(Pregunta(
            clave='aire_acondicionado',
            texto="¿El olor se detecta principalmente con el aire acondicionado encendido?",
            opciones=['si', 'no']
        ))

    # Diagnóstico 1: Fuga en el sistema de escape bajo el chasis
    @Rule(Sistema(area='escape_2'),
        Estado(clave='intensidad_olor', valor='si'))
    def diagnostico_fuga_escape_chasis(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falla en el sistema de escape bajo el chasis",
            'solucion': "Reemplazar el tramo afectado o soldar la zona afectada",
            'severidad': "Alta"
        })

    # Diagnóstico 2: Fuga múltiple cerca del motor
    @Rule(Sistema(area='escape_2'),
        Estado(clave='intensidad_olor', valor='no'),
        Estado(clave='aire_acondicionado', valor='si'))
    def diagnostico_fuga_escape_motor(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falla múltiple del escape cerca del motor",
            'solucion': "Reemplazar el tramo afectado o soldar la zona afectada",
            'severidad': "Alta"
        })

    # Diagnóstico 3: Otras causas
    @Rule(Sistema(area='escape_2'),
        Estado(clave='intensidad_olor', valor='no'),
        Estado(clave='aire_acondicionado', valor='no'))
    def diagnostico_otras_causas_olor_a_gases(self):
        self.diagnosticos_encontrados.append({
            'causa': "Otras causas posibles",
            'solucion': "Revisar otras posibles causas por las que sucede la falla",
            'severidad': "Media"
        })

### Para el síntoma "humo_escape_oscuro"
class SistemaEscape3(SistemaBase):
    def __init__(self):
        super().__init__()

    # Activación del diagnóstico de escape
    @Rule(Sistema(area='escape_3'))
    def iniciar_diagnostico_motor(self):
        print("Iniciando diagnóstico: Sistema Escape 3")

    # Paso 1: Preguntar por el color y textura del humo
    @Rule(Sistema(area='escape_3'),
        NOT(Estado(clave='color_textura_humo')))
    def preguntar_color_textura_humo(self):
        self.declare(Pregunta(
            clave='color_textura_humo',
            texto="¿El humo tiene color negro y textura densa?",
            opciones=['si', 'no']
        ))

    # Paso 2: Preguntar por la pérdida de potencia y alto consumo de combustible
    @Rule(Sistema(area='escape_3'),
        Estado(clave='color_textura_humo', valor='no'),
        NOT(Estado(clave='potencia_consumo')))
    def preguntar_potencia_consumo(self):
        self.declare(Pregunta(
            clave='potencia_consumo', 
            texto="¿La potencia del auto disminuye mientras el consumo de gasolina aumenta?",
            opciones=[
                'si',
                'no'
            ]
        ))

    # Diagnóstico 1: Exceso de gasolina
    @Rule(Sistema(area='escape_3'),
        Estado(clave='color_textura_humo', valor='si'))
    def diagnostico_exceso_gasolina(self):
        self.diagnosticos_encontrados.append({
            'causa': "Exceso de combustible",
            'solucion': "Limpiar o reemplazar inyectores, revisar sensor de oxígeno, verificar presión del combustible.",
            'severidad': "Media"
        })

    # Diagnóstico 2: Combustión incompleta
    @Rule(Sistema(area='escape_3'),
        Estado(clave='color_textura_humo', valor='no'),
        Estado(clave='potencia_consumo', valor='si'))
    def diagnostico_combustion_incompleta(self):
        self.diagnosticos_encontrados.append({
            'causa': "Combustión incompleta",
            'solucion': "Revisar y limpiar inyectores, cambiar bujías y cables, verificar sensor de oxígeno.",
            'severidad': "Media"
        })

    # Diagnóstico 3: Otras causas
    @Rule(Sistema(area='escape_3'),
        Estado(clave='color_textura_humo', valor='no'),
        Estado(clave='potencia_consumo', valor='no'))
    def diagnostico_otras_causas_humo_escape_oscuro(self):
        self.diagnosticos_encontrados.append({
            'causa': "Otras causas posibles",
            'solucion': "Revisar otras posibles causas por las que sucede la falla",
            'severidad': "Media"
        })