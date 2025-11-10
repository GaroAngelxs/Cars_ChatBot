from experta import *
from core.base import SistemaBase
from hechos import *

### Sistema de combustible
# Basado en reglas del PDF (Sistema de combustible 1–8).

# Grupo 1: Arranque tardío (Reglas 1–2)
class SistemaCombustible1(SistemaBase):
    def __init__(self):
        super().__init__()

    @Rule(Sistema(area='combustible_1'))
    def iniciar(self):
        print("Iniciando diagnóstico: Sistema Combustible 1 (arranque tardío)")

    # P1: ¿El motor tarda en arrancar?
    @Rule(Sistema(area='combustible_1'),
          NOT(Estado(clave='tarda_en_arrancar')))
    def preguntar_tarda_en_arrancar(self):
        self.declare(Pregunta(
            clave='tarda_en_arrancar',
            texto='¿El motor tarda en arrancar?',
            opciones=['si','no']
        ))

    # P2: Si tarda en arrancar, ¿se escucha zumbido de la bomba al dar contacto?
    @Rule(Sistema(area='combustible_1'),
          Estado(clave='tarda_en_arrancar', valor='si'),
          NOT(Estado(clave='zumbido_bomba_contacto')))
    def preguntar_zumbido_bomba(self):
        self.declare(Pregunta(
            clave='zumbido_bomba_contacto',
            texto='Al encender el contacto (sin dar marcha), ¿se escucha el zumbido de la bomba de combustible?',
            opciones=['si','no']
        ))

    # Dx1: Bomba de combustible defectuosa
    @Rule(Sistema(area='combustible_1'),
          Estado(clave='tarda_en_arrancar', valor='si'),
          Estado(clave='zumbido_bomba_contacto', valor='no'))
    def dx_bomba_defectuosa(self):
        self.diagnosticos_encontrados.append({
            'causa': 'Bomba de combustible defectuosa',
            'solucion': 'Verificar alimentación eléctrica y reemplazar la bomba si no opera al dar contacto',
            'severidad': 'Alta'
        })

    # P3: Si tarda en arrancar, ¿la presión de combustible es inferior a la especificada?
    @Rule(Sistema(area='combustible_1'),
          Estado(clave='tarda_en_arrancar', valor='si'),
          NOT(Estado(clave='presion_combustible_baja')))
    def preguntar_presion_baja(self):
        self.declare(Pregunta(
            clave='presion_combustible_baja',
            texto='¿La presión de combustible medida es inferior a la especificada?',
            opciones=['si','no']
        ))

    # Dx2: Filtro de combustible sucio
    @Rule(Sistema(area='combustible_1'),
          Estado(clave='tarda_en_arrancar', valor='si'),
          Estado(clave='presion_combustible_baja', valor='si'))
    def dx_filtro_combustible_sucio(self):
        self.diagnosticos_encontrados.append({
            'causa': 'Filtro de combustible sucio',
            'solucion': 'Medir presión en riel; reemplazar filtro y verificar regulador/líneas',
            'severidad': 'Media'
        })


# Grupo 2: Consumo alto (Reglas 3–4)
class SistemaCombustible2(SistemaBase):
    def __init__(self):
        super().__init__()

    @Rule(Sistema(area='combustible_2'))
    def iniciar(self):
        print("Iniciando diagnóstico: Sistema Combustible 2 (consumo alto)")

    # P1: ¿Consumo de combustible alto?
    @Rule(Sistema(area='combustible_2'),
          NOT(Estado(clave='consumo_combustible_alto')))
    def preguntar_consumo_alto(self):
        self.declare(Pregunta(
            clave='consumo_combustible_alto',
            texto='¿El consumo de combustible es alto?',
            opciones=['si','no']
        ))

    # P2A: Falta de potencia / respuesta lenta
    @Rule(Sistema(area='combustible_2'),
          Estado(clave='consumo_combustible_alto', valor='si'),
          NOT(Estado(clave='falta_potencia_y_respuesta_lenta')))
    def preguntar_falta_potencia(self):
        self.declare(Pregunta(
            clave='falta_potencia_y_respuesta_lenta',
            texto='¿El motor presenta falta de potencia y respuesta lenta?',
            opciones=['si','no']
        ))

    # Dx3: Filtro de aire sucio
    @Rule(Sistema(area='combustible_2'),
          Estado(clave='consumo_combustible_alto', valor='si'),
          Estado(clave='falta_potencia_y_respuesta_lenta', valor='si'))
    def dx_filtro_aire_sucio(self):
        self.diagnosticos_encontrados.append({
            'causa': 'Filtro de aire sucio',
            'solucion': 'Inspeccionar y reemplazar filtro de aire; verificar MAF si aplica',
            'severidad': 'Media'
        })

    # P2B: Marcha mínima irregular / fallos de encendido
    @Rule(Sistema(area='combustible_2'),
          Estado(clave='consumo_combustible_alto', valor='si'),
          NOT(Estado(clave='marcha_minima_irregular_o_misfire')))
    def preguntar_marcha_irregular(self):
        self.declare(Pregunta(
            clave='marcha_minima_irregular_o_misfire',
            texto='¿El motor tiene marcha mínima irregular o fallos de encendido?',
            opciones=['si','no']
        ))

    # Dx4: Inyectores sucios
    @Rule(Sistema(area='combustible_2'),
          Estado(clave='consumo_combustible_alto', valor='si'),
          Estado(clave='marcha_minima_irregular_o_misfire', valor='si'))
    def dx_inyectores_sucios(self):
        self.diagnosticos_encontrados.append({
            'causa': 'Inyectores sucios',
            'solucion': 'Aplicar limpieza de inyectores (ultrasónica o aditivo) y revisar patrones de pulverizado',
            'severidad': 'Media'
        })


# Grupo 3: Olor a gasolina (Reglas 5–6)
class SistemaCombustible3(SistemaBase):
    def __init__(self):
        super().__init__()

    @Rule(Sistema(area='combustible_3'))
    def iniciar(self):
        print("Iniciando diagnóstico: Sistema Combustible 3 (olor a gasolina)")

    # P1: ¿Se percibe olor a gasolina?
    @Rule(Sistema(area='combustible_3'),
          NOT(Estado(clave='olor_a_gasolina')))
    def preguntar_olor_gasolina(self):
        self.declare(Pregunta(
            clave='olor_a_gasolina',
            texto='¿Se percibe olor a gasolina?',
            opciones=['si','no']
        ))

    # P2A: ¿Manchas húmedas o goteos bajo el vehículo?
    @Rule(Sistema(area='combustible_3'),
          Estado(clave='olor_a_gasolina', valor='si'),
          NOT(Estado(clave='manchas_o_goteos_bajo_vehiculo')))
    def preguntar_manchas_goteos(self):
        self.declare(Pregunta(
            clave='manchas_o_goteos_bajo_vehiculo',
            texto='¿Se observan manchas húmedas o goteos de gasolina bajo el vehículo?',
            opciones=['si','no']
        ))

    # Dx5: Fuga en el sistema de combustible
    @Rule(Sistema(area='combustible_3'),
          Estado(clave='olor_a_gasolina', valor='si'),
          Estado(clave='manchas_o_goteos_bajo_vehiculo', valor='si'))
    def dx_fuga_combustible(self):
        self.diagnosticos_encontrados.append({
            'causa': 'Fuga en el sistema de combustible',
            'solucion': 'Inspeccionar líneas, conexiones, regulador y tanque; reparar de inmediato por seguridad',
            'severidad': 'Crítica'
        })

    # P2B: ¿Humo negro con fuerte olor a gasolina?
    @Rule(Sistema(area='combustible_3'),
          Estado(clave='olor_a_gasolina', valor='si'),
          NOT(Estado(clave='humo_negro_fuerte_olor')))
    def preguntar_humo_negro(self):
        self.declare(Pregunta(
            clave='humo_negro_fuerte_olor',
            texto='¿El humo del escape es negro con fuerte olor a gasolina?',
            opciones=['si','no']
        ))

    # Dx6: Mezcla demasiado rica
    @Rule(Sistema(area='combustible_3'),
          Estado(clave='olor_a_gasolina', valor='si'),
          Estado(clave='humo_negro_fuerte_olor', valor='si'))
    def dx_mezcla_rica(self):
        self.diagnosticos_encontrados.append({
            'causa': 'Mezcla demasiado rica',
            'solucion': 'Revisar sensor O2/MAF/temperatura, regulador y fugas de inyectores; escanear códigos',
            'severidad': 'Alta'
        })


# Grupo 4: Pérdida de potencia en pendientes (Reglas 7–8)
class SistemaCombustible4(SistemaBase):
    def __init__(self):
        super().__init__()

    @Rule(Sistema(area='combustible_4'))
    def iniciar(self):
        print("Iniciando diagnóstico: Sistema Combustible 4 (pendientes)")

    # P1: ¿Pierde potencia en pendientes?
    @Rule(Sistema(area='combustible_4'),
          NOT(Estado(clave='pierde_potencia_en_pendientes')))
    def preguntar_potencia_pendientes(self):
        self.declare(Pregunta(
            clave='pierde_potencia_en_pendientes',
            texto='¿El motor pierde potencia en pendientes?',
            opciones=['si','no']
        ))

    # P2A: ¿Empeora con tanque bajo?
    @Rule(Sistema(area='combustible_4'),
          Estado(clave='pierde_potencia_en_pendientes', valor='si'),
          NOT(Estado(clave='empeora_con_tanque_bajo')))
    def preguntar_tanque_bajo(self):
        self.declare(Pregunta(
            clave='empeora_con_tanque_bajo',
            texto='¿El problema empeora cuando el tanque tiene poca gasolina?',
            opciones=['si','no']
        ))

    # Dx7: Obstrucción en el suministro de combustible
    @Rule(Sistema(area='combustible_4'),
          Estado(clave='pierde_potencia_en_pendientes', valor='si'),
          Estado(clave='empeora_con_tanque_bajo', valor='si'))
    def dx_obstruccion_suministro(self):
        self.diagnosticos_encontrados.append({
            'causa': 'Obstrucción en el suministro de combustible',
            'solucion': 'Inspeccionar colador del tanque, líneas y filtro; revisar bomba bajo carga',
            'severidad': 'Alta'
        })

    # P2B: ¿Detonación/cascabeleo al acelerar?
    @Rule(Sistema(area='combustible_4'),
          Estado(clave='pierde_potencia_en_pendientes', valor='si'),
          NOT(Estado(clave='detonacion_o_cascabeleo')))
    def preguntar_detonacion(self):
        self.declare(Pregunta(
            clave='detonacion_o_cascabeleo',
            texto='¿Se escucha detonación o cascabeleo al acelerar?',
            opciones=['si','no']
        ))

    # Dx8: Problemas de octanaje o encendido
    @Rule(Sistema(area='combustible_4'),
          Estado(clave='pierde_potencia_en_pendientes', valor='si'),
          Estado(clave='detonacion_o_cascabeleo', valor='si'))
    def dx_octanaje_encendido(self):
        self.diagnosticos_encontrados.append({
            'causa': 'Problemas de octanaje o encendido',
            'solucion': 'Usar gasolina con octanaje adecuado; revisar avance de encendido y sensores de detonación',
            'severidad': 'Media'
        })
