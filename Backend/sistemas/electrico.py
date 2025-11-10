from experta import *
from core.base import SistemaBase
from hechos import *

### Para el síntoma "no_enciende"
class SistemaElectrico1(SistemaBase):
    def __init__(self):
        super().__init__()

    # Activación del diagnóstico de electrico
    @Rule(Sistema(area='electrico_1'))
    def iniciar_diagnostico_motor(self):
        print("Iniciando diagnóstico: Sistema Electrico 1")

    # Paso 1: Preguntar sobre el clic de arranque
    @Rule(Sistema(area='electrico_1'),
        NOT(Estado(clave='clic_aranque')))
    def preguntar_clic_aranque(self):
        self.declare(Pregunta(
            clave='clic_aranque',
            texto="¿Escuchas el clic de arranque al girar la llave?",
            opciones=['si', 'no']
        ))

    # Paso 2: Preguntar por el comportamiento del tablero
    @Rule(Sistema(area='electrico_1'),
        Estado(clave='clic_aranque', valor='si'),
        NOT(Estado(clave='comportamiento_tablero')))
    def preguntar_comportamiento_tablero(self):
        self.declare(Pregunta(
            clave='comportamiento_tablero', 
            texto="¿Cómo se comportan las luces del tablero al intentar arrancar?",
            opciones=[
                'se_apagan_o_vuelven_tenues',
                'se_mantienen_encendidas_con_normalidad',
                'otro_comportamiento'
            ]
        ))

    # Diagnóstico 1: Batería desconectada o descargada
    @Rule(Sistema(area='electrico_1'),
        Estado(clave='clic_aranque', valor='no'))
    def diagnostico_bateria_desconectada(self):
        self.diagnosticos_encontrados.append({
            'causa': "Batería descargada o conexiones sueltas",
            'solucion': "Cargar o reemplazar la batería, revisar terminales y conexiones",
            'severidad': "Media"
        })

    # Diagnóstico 2: Batería descargada
    @Rule(Sistema(area='electrico_1'),
        Estado(clave='clic_aranque', valor='si'),
        Estado(clave='comportamiento_tablero', valor='se_apagan_o_vuelven_tenues'))
    def diagnostico_bateria_descargada(self):
        self.diagnosticos_encontrados.append({
            'causa': "Batería descargada",
            'solucion': "Cargar o reemplazar la batería",
            'severidad': "Media"
        })

    # Diagnóstico 3: Falla del motor de arranque
    @Rule(Sistema(area='electrico_1'),
        Estado(clave='clic_aranque', valor='si'),
        Estado(clave='comportamiento_tablero', valor='se_mantienen_encendidas_con_normalidad'))
    def diagnostico_falla_arranque(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falla en el sistema de arranque",
            'solucion': "Revisar motor de arranque, solenoide o interruptor de encendido",
            'severidad': "Alta"
        })

    # Diagnóstico 4: Otras causas
    @Rule(Sistema(area='electrico_1'),
        Estado(clave='clic_aranque', valor='si'),
        Estado(clave='comportamiento_tablero', valor='otro_comportamiento'))
    def diagnostico_otras_causas_no_enciende(self):
        self.diagnosticos_encontrados.append({
            'causa': "Otras causas posibles",
            'solucion': "Revisar otras posibles causas por las que sucede la falla",
            'severidad': "Media"
        })

### Para el síntoma "luces_parpadean"
class SistemaElectrico2(SistemaBase):
    def __init__(self):
        super().__init__()

    # Activación del diagnóstico de electrico
    @Rule(Sistema(area='electrico_2'))
    def iniciar_diagnostico_motor(self):
        print("Iniciando diagnóstico: Sistema Electrico 2")

    # Paso 1: Preguntar sobre parpadeo en las luces del tablero
    @Rule(Sistema(area='electrico_2'),
        NOT(Estado(clave='luces_tablero')))
    def preguntar_luces_tablero(self):
        self.declare(Pregunta(
            clave='luces_tablero',
            texto="¿El parpadeo de luces del tablero es constante con al auto encendido?",
            opciones=['si', 'no']
        ))

    # Diagnóstico 1: Falla en el alternador
    @Rule(Sistema(area='electrico_2'),
        Estado(clave='luces_tablero', valor='si'))
    def diagnostico_falla_alternador(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falla en alternador",
            'solucion': "Reemplazar el alternador",
            'severidad': "Alta"
        })

    # Diagnóstico 2: Otras causas
    @Rule(Sistema(area='electrico_2'),
        Estado(clave='luces_tablero', valor='no'))
    def diagnostico_otras_causas_luces_parpadean(self):
        self.diagnosticos_encontrados.append({
            'causa': "Otras causas posibles",
            'solucion': "Revisar otras posibles causas por las que sucede la falla",
            'severidad': "Media"
        })

### Para el síntoma "luces_de_faros_tenues"
class SistemaElectrico3(SistemaBase):
    def __init__(self):
        super().__init__()

    # Activación del diagnóstico de electrico
    @Rule(Sistema(area='electrico_3'))
    def iniciar_diagnostico_motor(self):
        print("Iniciando diagnóstico: Sistema Electrico 3")

    # Paso 1: Preguntar por el comportamiento al acelerar
    @Rule(Sistema(area='electrico_3'),
        NOT(Estado(clave='faros_acelerar')))
    def preguntar_faros_acelerar(self):
        self.declare(Pregunta(
            clave='faros_acelerar',
            texto="¿Los faros recuperan intensidad al acelerar?",
            opciones=['si', 'no']
        ))

    # Paso 2: Preguntar por los bornes de la batería
    @Rule(Sistema(area='electrico_3'),
        Estado(clave='faros_acelerar', valor='no'),
        NOT(Estado(clave='bornes_bateria')))
    def preguntar_bornes_bateria(self):
        self.declare(Pregunta(
            clave='bornes_bateria', 
            texto="¿Los bornes de la batería están cubiertos con sustancia blanca o azul?",
            opciones=[
                'si',
                'no'
            ]
        ))

    # Diagnóstico 1: Batería baja
    @Rule(Sistema(area='electrico_3'),
        Estado(clave='faros_acelerar', valor='si'))
    def diagnostico_bateria_baja(self):
        self.diagnosticos_encontrados.append({
            'causa': "Batería baja",
            'solucion': "Cargar o reemplazar la batería, revisar terminales y conexiones",
            'severidad': "Media"
        })

    # Diagnóstico 2: Bornes sulfatados
    @Rule(Sistema(area='electrico_3'),
        Estado(clave='faros_acelerar', valor='no'),
        Estado(clave='bornes_bateria', valor='si'))
    def diagnostico_bornes_sulfatados(self):
        self.diagnosticos_encontrados.append({
            'causa': "Bornes sulfatados",
            'solucion': "Limpiar los bornes con un cepillo de alambre",
            'severidad': "Baja"
        })

    # Diagnóstico 3: Otras causas
    @Rule(Sistema(area='electrico_3'),
        Estado(clave='faros_acelerar', valor='no'),
        Estado(clave='bornes_bateria', valor='no'))
    def diagnostico_otras_causas_luces_de_faros_tenues(self):
        self.diagnosticos_encontrados.append({
            'causa': "Otras causas posibles",
            'solucion': "Revisar otras posibles causas por las que sucede la falla",
            'severidad': "Media"
        })

### Para el síntoma "claxon_o_limpiaparabrisas_disfuncionales"
class SistemaElectrico4(SistemaBase):
    def __init__(self):
        super().__init__()

    # Activación del diagnóstico de electrico
    @Rule(Sistema(area='electrico_4'))
    def iniciar_diagnostico_motor(self):
        print("Iniciando diagnóstico: Sistema Electrico 4")

    # Paso 1: Preguntar por otros componentes
    @Rule(Sistema(area='electrico_4'),
        NOT(Estado(clave='otros_componentes')))
    def preguntar_otros_componentes(self):
        self.declare(Pregunta(
            clave='otros_componentes',
            texto="¿Otros componentes conectados al mismo fusible funcionan?",
            opciones=['si', 'no']
        ))

    # Diagnóstico 1: Fusible fundido
    @Rule(Sistema(area='electrico_4'),
        Estado(clave='otros_componentes', valor='no'))
    def diagnostico_fusible_fundido(self):
        self.diagnosticos_encontrados.append({
            'causa': "Fusible fundido",
            'solucion': "Reemplazar el fusible fundido",
            'severidad': "Baja"
        })

    # Diagnóstico 2: Falla en el circuito eléctrico
    @Rule(Sistema(area='electrico_4'),
        Estado(clave='otros_componentes', valor='si'))
    def diagnostico_falla_circuito(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falla en el circuito eléctrico",
            'solucion': "Revisar interruptor, cableado, relés y tierra del circuito",
            'severidad': "Media"
        })