from experta import *
from hechos import *
from core.base import SistemaBase

class RouterDiagnosticos(SistemaBase):
    def __init__(self):
        super().__init__()
        self.sistemas_activados = set()
        self.sintomas_ingresados = set()

        self.mapeo_sintomas = {
            'El_motor_no_arranca': 'El motor del auto no arranca',
            'El_auto_se_apaga': 'El auto se apaga repentinamente',
            'El_auto_emite_humo_negro': 'El auto emite humo negro',
            'El_auto_emite_humo_azul': 'El auto emite humo azul',
            'El_auto_emite_humo_blanco': 'El auto emite humo blanco',
            'El_motor_vibra_excesivamente': 'El motor vibra excesivamente',
            'El_motor_se_calienta': 'El motor se calienta mucho',
            'Liquido_verde_o_rojo_debajo_del_motor': 'Hay líquido verde o rojo debajo del motor',
            'El_ventilador_del_auto_no_hace_ruido': 'El ventilador no hace ruido',
            'Los_cambios_entran_con_dificultad': 'Los cambios entran con mucha dificultad',
            'Se_escuchan_ruidos_metalicos_en_cambio': 'Se escuchan ruidos metálicos al cambiar de marcha',
            'El_auto_no_avanza_al_acelerar': 'El auto no avanza al acelerar',
            'Aceite_de_transmision_esta_bajo': 'El aceite de la transmisión está bajo',
            'Una_llanta_se_ve_baja': 'Una llanta del auto está baja',
            'Desgaste_irregular_llantas': 'Hay desgaste irregular en las llantas',
            'Vibracion_alta_velocidad': 'El auto produce vibración a alta velocidad',
            'El_auto_no_enciende': 'El auto no enciende',
            'Las_luces_del_tablero_parpadean': 'Las luces del tablero parpadean',
            'Luces_de_faros_tenues': 'Las luces de los faros son tenues',
            'Claxon_o_limpiaparabrisas_disfuncionales': 'El claxon o limpiaparabrisas son disfuncionales',
            'Pedal_de_freno_esponjoso': 'El pedal del freno se siente esponjoso',
            'Chirrido_al_frenar': 'Se escucha un chirrido al frenar',
            'Desvio_al_frenar': 'El vehículo se desvía al frenar',
            'Vibracion_al_frenar': 'Vibración al frenar',
            'Arranque_tardio': 'El motor tarda en arrancar',
            'Consumo_combustible_alto': 'El consumo de combustible es alto',
            'Olor_a_gasolina': 'Se percibe olor a gasolina',
            'Perdida_potencia_en_pendientes': 'El motor pierde potencia en pendientes'
        }

    @DefFacts()
    def _initial_action(self):
        """Hecho inicial para activar el motor"""
        yield Accion(tipo='iniciar_diagnostico')

    @Rule(Accion(tipo='iniciar_diagnostico'),
          NOT(Sintoma()))
    def preguntar_sintomas_generales(self):

        opciones_naturales = list(self.mapeo_sintomas.values())

        self.declare(Pregunta(
            clave='sintoma_general',
            texto="¿Qué síntomas presenta su vehículo?",
            opciones=opciones_naturales
        ))

    # Procesar MÚLTIPLES síntomas
    @Rule(Estado(clave='sintoma_general', valor=MATCH.valores))
    def procesar_sintomas_multiples(self, valores):
        """Procesa múltiples síntomas ingresados por el usuario"""
        if isinstance(valores, str):

            sintomas_naturales = [s.strip() for s in valores.split(',')]

            mapeo_inverso = {v: k for k, v in self.mapeo_sintomas.items()}

            sintomas_codigos = []

            for sintoma_natural in sintomas_naturales:
                if sintoma_natural in mapeo_inverso:
                    codigo = mapeo_inverso[sintoma_natural]
                    sintomas_codigos.append(codigo)
                else:
                    codigo_encontrado = None
                    for texto_natural, codigo in mapeo_inverso.items():
                        if sintoma_natural.lower() in texto_natural.lower():
                            codigo_encontrado = codigo
                            break
                    
                    if codigo_encontrado:
                        sintomas_codigos.append(codigo_encontrado)
                    else:
                        print(f"Síntoma no reconocido: {sintoma_natural}")
            
            self.sintomas_ingresados.update(sintomas_codigos)

            for codigo in sintomas_codigos:
                self.procesar_sintoma_individual(codigo)

    def procesar_sintoma_individual(self, sintoma):
        """Procesa un síntoma individual por su código"""

        if sintoma == 'El_motor_no_arranca':
            self.declare(Sistema(area='motor_1'))
            self.sistemas_activados.add('motor_1')
                
        elif sintoma == 'El_auto_se_apaga':
            self.declare(Sistema(area='motor_2'))
            self.sistemas_activados.add('motor_2')
                
        elif sintoma == 'El_auto_emite_humo_negro':
            self.declare(Sistema(area='motor_3'))
            self.sistemas_activados.add('motor_3')

        elif sintoma == 'El_auto_emite_humo_azul':
            self.declare(Sistema(area='motor_4'))
            self.sistemas_activados.add('motor_4')
                
        elif sintoma == 'El_auto_emite_humo_blanco':
            self.declare(Sistema(area='motor_5'))
            self.sistemas_activados.add('motor_5')
                
        elif sintoma == 'El_motor_vibra_excesivamente':
            self.declare(Sistema(area='motor_6'))
            self.sistemas_activados.add('motor_6')
                    
        elif sintoma == 'El_motor_se_calienta':
            self.declare(Sistema(area='enfriamiento_1'))
            self.sistemas_activados.add('enfriamiento_1')

        elif sintoma == 'Liquido_verde_o_rojo_debajo_del_motor':
            self.declare(Sistema(area='enfriamiento_2'))
            self.sistemas_activados.add('enfriamiento_2')
 
        elif sintoma == 'El_ventilador_del_auto_no_hace_ruido':
            self.declare(Sistema(area='enfriamiento_3'))
            self.sistemas_activados.add('enfriamiento_3')
                    
        elif sintoma == 'Los_cambios_entran_con_dificultad':
            self.declare(Sistema(area='transmision_1'))
            self.sistemas_activados.add('transmision_1')

        elif sintoma == 'Se_escuchan_ruidos_metalicos_en_cambio':
            self.declare(Sistema(area='transmision_2'))
            self.sistemas_activados.add('transmision_2')
                
        elif sintoma == 'El_auto_no_avanza_al_acelerar':
            self.declare(Sistema(area='transmision_3'))
            self.sistemas_activados.add('transmision_3')

        elif sintoma == 'Aceite_de_transmision_esta_bajo':
            self.declare(Sistema(area='transmision_4'))
            self.sistemas_activados.add('transmision_4')
                
        elif sintoma in ['Una_llanta_se_ve_baja']:
            self.declare(Sistema(area='llantas_1'))
            self.sistemas_activados.add('llantas_1')

        elif sintoma == 'Desgaste_irregular_llantas':
            self.declare(Sistema(area='llantas_2'))
            self.sistemas_activados.add('llantas_2')

        elif sintoma == 'Vibracion_alta_velocidad':
            self.declare(Sistema(area='llantas_3'))
            self.sistemas_activados.add('llantas_3')

        elif sintoma == 'El_auto_no_enciende':
            self.declare(Sistema(area='electrico_1'))
            self.sistemas_activados.add('electrico_1')
                
        elif sintoma == 'Las_luces_del_tablero_parpadean':
            self.declare(Sistema(area='electrico_2'))
            self.sistemas_activados.add('electrico_2')
                
        elif sintoma == 'Luces_de_faros_tenues':
            self.declare(Sistema(area='electrico_3'))
            self.sistemas_activados.add('electrico_3')
                
        elif sintoma == 'Claxon_o_limpiaparabrisas_disfuncionales':
            self.declare(Sistema(area='electrico_4'))
            self.sistemas_activados.add('electrico_4')
        
        elif sintoma == 'Pedal_de_freno_esponjoso':
            self.declare(Sistema(area='frenos_1'))
            self.sistemas_activados.add('frenos_1')

        elif sintoma == 'Chirrido_al_frenar':
            self.declare(Sistema(area='frenos_2'))
            self.sistemas_activados.add('frenos_2')

        elif sintoma == 'Desvio_al_frenar':
            self.declare(Sistema(area='frenos_3'))
            self.sistemas_activados.add('frenos_3')

        elif sintoma == 'Vibracion_al_frenar':
            self.declare(Sistema(area='frenos_4'))
            self.sistemas_activados.add('frenos_4')
        elif sintoma == 'Arranque_tardio':
            self.declare(Sistema(area='combustible_1'))
            self.sistemas_activados.add('combustible_1')
        elif sintoma == 'Consumo_combustible_alto':
            self.declare(Sistema(area='combustible_2'))
            self.sistemas_activados.add('combustible_2')
        elif sintoma == 'Olor_a_gasolina':
            self.declare(Sistema(area='combustible_3'))
            self.sistemas_activados.add('combustible_3')
        elif sintoma == 'Perdida_potencia_en_pendientes':
            self.declare(Sistema(area='combustible_4'))
            self.sistemas_activados.add('combustible_4')


    def obtener_sistemas_activados(self):
        """Retorna los sistemas que necesitan diagnóstico"""
        return self.sistemas_activados.copy()
    
    def obtener_sintomas_ingresados(self):
        """Retorna los síntomas ingresados por el usuario"""
        sintomas_naturales = []
        for codigo in self.sintomas_ingresados:
            if codigo in self.mapeo_sintomas:
                sintomas_naturales.append(self.mapeo_sintomas[codigo])
        return sintomas_naturales

    def obtener_sintomas_codigos(self):
        """Retorna los síntomas en formato código (para uso interno)"""
        return self.sintomas_ingresados.copy()
    
    def limpiar_hechos_temporales(self):
        """Limpia hechos temporales entre ejecuciones"""
        self.sistemas_activados.clear()
        self.sintomas_ingresados.clear()
