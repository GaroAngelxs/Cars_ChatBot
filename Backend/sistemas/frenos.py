from experta import *
from core.base import SistemaBase
from hechos import *

### Sistema de frenos

# Grupo 1: Pedal esponjoso (Reglas 1-2)
class SistemaFrenos1(SistemaBase):
    def __init__(self):
        super().__init__()

    @Rule(Sistema(area='frenos_1'))
    def iniciar(self):
        print("Iniciando diagnóstico: Sistema Frenos 1 (pedal esponjoso)")

    # P1: ¿Pedal esponjoso?
    @Rule(Sistema(area='frenos_1'),
          NOT(Estado(clave='pedal_esponjoso')))
    def preguntar_pedal_esponjoso(self):
        self.declare(Pregunta(
            clave='pedal_esponjoso',
            texto='¿El pedal del freno se siente esponjoso?',
            opciones=['si','no']
        ))

    # P2: Si es esponjoso, preguntar recorrido
    @Rule(Sistema(area='frenos_1'),
          Estado(clave='pedal_esponjoso', valor='si'),
          NOT(Estado(clave='recorrido_pedal_largo')))
    def preguntar_recorrido(self):
        self.declare(Pregunta(
            clave='recorrido_pedal_largo',
            texto='¿El recorrido/altura del pedal al frenar es mayor de lo normal?',
            opciones=['si','no']
        ))

    # Dx1: Aire en el sistema
    @Rule(Sistema(area='frenos_1'),
          Estado(clave='pedal_esponjoso', valor='si'),
          Estado(clave='recorrido_pedal_largo', valor='si'))
    def dx_aire(self):
        self.diagnosticos_encontrados.append({
            'causa': 'Aire en el sistema de frenos',
            'solucion': 'Purgar el sistema y renovar/limpiar líquido si es necesario',
            'severidad': 'Alta'
        })

    # P3: Si es esponjoso, preguntar nivel de líquido
    @Rule(Sistema(area='frenos_1'),
          Estado(clave='pedal_esponjoso', valor='si'),
          NOT(Estado(clave='nivel_liquido_frenos_bajo')))
    def preguntar_nivel_liquido(self):
        self.declare(Pregunta(
            clave='nivel_liquido_frenos_bajo',
            texto='¿El nivel de líquido de frenos ha bajado notablemente?',
            opciones=['si','no']
        ))

    # Dx2: Fuga hidráulica
    @Rule(Sistema(area='frenos_1'),
          Estado(clave='pedal_esponjoso', valor='si'),
          Estado(clave='nivel_liquido_frenos_bajo', valor='si'))
    def dx_fuga_hidraulica(self):
        self.diagnosticos_encontrados.append({
            'causa': 'Fuga en el sistema hidráulico de frenos',
            'solucion': 'Inspeccionar líneas, cilindro maestro, mangueras, pinzas/cilindros; reparar y purgar',
            'severidad': 'Crítica'
        })


# Grupo 2: Chirridos al frenar (Reglas 3-4)
class SistemaFrenos2(SistemaBase):
    def __init__(self):
        super().__init__()

    @Rule(Sistema(area='frenos_2'))
    def iniciar(self):
        print("Iniciando diagnóstico: Sistema Frenos 2 (chirridos)")

    # P1: ¿Se escucha chirrido al frenar?
    @Rule(Sistema(area='frenos_2'),
          NOT(Estado(clave='chirrido_al_frenar')))
    def preguntar_chirrido(self):
        self.declare(Pregunta(
            clave='chirrido_al_frenar',
            texto='¿Se escucha un chirrido al frenar?',
            opciones=['si','no']
        ))

    # P2: Si hay chirrido, caracterizar el sonido
    @Rule(Sistema(area='frenos_2'),
          Estado(clave='chirrido_al_frenar', valor='si'),
          NOT(Estado(clave='tipo_sonido_chirrido')))
    def preguntar_tipo_chirrido(self):
        self.declare(Pregunta(
            clave='tipo_sonido_chirrido',
            texto='¿Cómo es el sonido?',
            opciones=['metalico_agudo', 'desaparece_tras_varias_frenadas']
        ))

    # Dx3: Pastillas desgastadas
    @Rule(Sistema(area='frenos_2'),
          Estado(clave='chirrido_al_frenar', valor='si'),
          Estado(clave='tipo_sonido_chirrido', valor='metalico_agudo'))
    def dx_pastillas_desgastadas(self):
        self.diagnosticos_encontrados.append({
            'causa': 'Pastillas de freno desgastadas',
            'solucion': 'Inspeccionar espesor y cambiar pastillas (y revisar discos)',
            'severidad': 'Media'
        })

    # Dx4: Polvo acumulado
    @Rule(Sistema(area='frenos_2'),
          Estado(clave='chirrido_al_frenar', valor='si'),
          Estado(clave='tipo_sonido_chirrido', valor='desaparece_tras_varias_frenadas'))
    def dx_polvo(self):
        self.diagnosticos_encontrados.append({
            'causa': 'Acumulación de polvo en pastillas',
            'solucion': 'Limpieza del conjunto de freno; revisar clips/antirruido',
            'severidad': 'Baja'
        })


# Grupo 3: Desvío al frenar (Reglas 5-6)
class SistemaFrenos3(SistemaBase):
    def __init__(self):
        super().__init__()

    @Rule(Sistema(area='frenos_3'))
    def iniciar(self):
        print("Iniciando diagnóstico: Sistema Frenos 3 (desvío)")

    # P1: ¿Se desvía al frenar?
    @Rule(Sistema(area='frenos_3'),
          NOT(Estado(clave='desvio_al_frenar')))
    def preguntar_desvio(self):
        self.declare(Pregunta(
            clave='desvio_al_frenar',
            texto='¿El vehículo se desvía hacia un lado al frenar?',
            opciones=['si','no']
        ))

    # P2: Si se desvía, ¿es al mismo lado siempre?
    @Rule(Sistema(area='frenos_3'),
          Estado(clave='desvio_al_frenar', valor='si'),
          NOT(Estado(clave='desvio_constante_mismo_lado')))
    def preguntar_constancia_desvio(self):
        self.declare(Pregunta(
            clave='desvio_constante_mismo_lado',
            texto='¿Ese desvío es consistente siempre hacia el mismo lado?',
            opciones=['si','no']
        ))

    # Dx5: Desgaste desigual
    @Rule(Sistema(area='frenos_3'),
          Estado(clave='desvio_al_frenar', valor='si'),
          Estado(clave='desvio_constante_mismo_lado', valor='si'))
    def dx_desgaste_desigual(self):
        self.diagnosticos_encontrados.append({
            'causa': 'Desgaste desigual de pastillas o discos',
            'solucion': 'Comparar espesores izq/der; revisar calipers/guías y corregir',
            'severidad': 'Media'
        })

    # P3: ¿Se observa líquido en llanta o pinza?
    @Rule(Sistema(area='frenos_3'),
          Estado(clave='desvio_al_frenar', valor='si'),
          NOT(Estado(clave='liquido_en_llanta_o_pinza')))
    def preguntar_liquido(self):
        self.declare(Pregunta(
            clave='liquido_en_llanta_o_pinza',
            texto='¿Hay líquido de frenos visible en la llanta o pinza?',
            opciones=['si','no']
        ))

    # Dx6: Fuga en una rueda
    @Rule(Sistema(area='frenos_3'),
          Estado(clave='desvio_al_frenar', valor='si'),
          Estado(clave='liquido_en_llanta_o_pinza', valor='si'))
    def dx_fuga_rueda(self):
        self.diagnosticos_encontrados.append({
            'causa': 'Fuga de líquido de frenos en una rueda',
            'solucion': 'Revisar sello del pistón de caliper/cilindro, mangueras y purga; reparar',
            'severidad': 'Crítica'
        })


# Grupo 4: Vibración al frenar (Reglas 7-8)
class SistemaFrenos4(SistemaBase):
    def __init__(self):
        super().__init__()

    @Rule(Sistema(area='frenos_4'))
    def iniciar(self):
        print("Iniciando diagnóstico: Sistema Frenos 4 (vibración)")

    # P1: ¿Vibración al frenar?
    @Rule(Sistema(area='frenos_4'),
          NOT(Estado(clave='vibracion_al_frenar')))
    def preguntar_vibracion(self):
        self.declare(Pregunta(
            clave='vibracion_al_frenar',
            texto='¿Sientes vibración al frenar?',
            opciones=['si','no']
        ))

    # P2: ¿Dónde se siente más?
    @Rule(Sistema(area='frenos_4'),
          Estado(clave='vibracion_al_frenar', valor='si'),
          NOT(Estado(clave='lugar_vibracion_freno')))
    def preguntar_lugar_vibracion(self):
        self.declare(Pregunta(
            clave='lugar_vibracion_freno',
            texto='¿Dónde se siente principalmente la vibración al frenar?',
            opciones=['pedal','volante']
        ))

    # Dx7: Discos deformados (pedal)
    @Rule(Sistema(area='frenos_4'),
          Estado(clave='vibracion_al_frenar', valor='si'),
          Estado(clave='lugar_vibracion_freno', valor='pedal'))
    def dx_discos_deformados(self):
        self.diagnosticos_encontrados.append({
            'causa': 'Discos de freno deformados (alabeo)',
            'solucion': 'Medir alabeo; rectificar o reemplazar; asegurar par de apriete correcto',
            'severidad': 'Media'
        })

    # Dx8: Discos delanteros deformados (volante)
    @Rule(Sistema(area='frenos_4'),
          Estado(clave='vibracion_al_frenar', valor='si'),
          Estado(clave='lugar_vibracion_freno', valor='volante'))
    def dx_discos_delanteros_deformados(self):
        self.diagnosticos_encontrados.append({
            'causa': 'Discos delanteros deformados',
            'solucion': 'Inspeccionar eje delantero; rectificar/cambiar discos; revisar bujes/rodamientos',
            'severidad': 'Media'
        })
