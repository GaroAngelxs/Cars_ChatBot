from experta import *
from hechos import *
from core.base import SistemaBase

class RouterDiagnosticos(SistemaBase):
    def __init__(self):
        super().__init__()
        self.sistemas_activados = set()
        self.sintomas_ingresados = set()

    @DefFacts()
    def _initial_action(self):
        """Hecho inicial para activar el motor"""
        yield Accion(tipo='iniciar_diagnostico')

    @Rule(Accion(tipo='iniciar_diagnostico'),
          NOT(Sintoma()))
    def preguntar_sintomas_generales(self):
        self.declare(Pregunta(
            clave='sintoma_general',
            texto="¿Qué síntomas presenta su vehículo? (puede elegir varios separados por coma)",
            opciones=[
                'El_motor_no_arranca',
                'El_motor_se_calienta', 
                'hace_ruidos_raros', 
                'Al_acelerar_pierde_potencia', 
                'humo_excesivo',
                'Los_cambios_entran_con_dificultad',
                'Se_escuchan_ruidos_metalicos_en_cambio',
                'El_auto_no_avanza_al_acelerar',
                'Aceite_de_transmision_esta_bajo',
                'frenos_defectuosos',
                'fallas_electricas',
                'vibracion_excesiva',
                'Una_llanta_se_ve_baja',
                'Desgaste_irregular_llantas',
                'Vibracion_alta_velocidad'
            ]
        ))

    # Procesar MÚLTIPLES síntomas
    @Rule(Estado(clave='sintoma_general', valor=MATCH.valores))
    def procesar_sintomas_multiples(self, valores):
        """Procesa múltiples síntomas ingresados por el usuario"""
        if isinstance(valores, str):
            sintomas = [s.strip() for s in valores.split(',')]
            self.sintomas_ingresados.update(sintomas)
            
            print(f"Síntomas identificados: {', '.join(sintomas)}")
            
            for sintoma in sintomas:
                if sintoma in ['El_motor_no_arranca', 'Al_acelerar_pierde_potencia', 'humo_excesivo']:
                    self.declare(Sistema(area='motor'))
                    self.sistemas_activados.add('motor')
                    print(f"Sistema activado: Motor")
                    
                elif sintoma in ['El_motor_se_calienta']:
                    self.declare(Sistema(area='enfriamiento'))
                    self.sistemas_activados.add('enfriamiento')
                    print(f"Sistema activado: Enfriamiento")
                    
                elif sintoma in ['Los_cambios_entran_con_dificultad', 'vibracion_excesiva']:
                    self.declare(Sistema(area='transmision_1'))
                    self.sistemas_activados.add('transmision_1')
                    print(f"Sistema activado: Transmisión")

                elif sintoma in ['Se_escuchan_ruidos_metalicos_en_cambio']:
                    self.declare(Sistema(area='transmision_2'))
                    self.sistemas_activados.add('transmision_2')
                    print(f"Sistema activado: Transmisión")
                
                elif sintoma in ['El_auto_no_avanza_al_acelerar']:
                    self.declare(Sistema(area='transmision_3'))
                    self.sistemas_activados.add('transmision_3')
                    print(f"Sistema activado: Transmisión")

                elif sintoma in ['Aceite_de_transmision_esta_bajo']:
                    self.declare(Sistema(area='transmision_4'))
                    self.sistemas_activados.add('transmision_4')
                    print(f"Sistema activado: Transmisión")
                    
                elif sintoma in ['frenos_defectuosos']:
                    self.declare(Sistema(area='frenos'))
                    self.sistemas_activados.add('frenos')
                    print(f"Sistema activado: Frenos")
                    
                elif sintoma in ['fallas_electricas', 'hace_ruidos_raros']:
                    self.declare(Sistema(area='electrico'))
                    self.sistemas_activados.add('electrico')
                    print(f"Sistema activado: Eléctrico")
                
                elif sintoma in ['Una_llanta_se_ve_baja']:
                    self.declare(Sistema(area='llantas_1'))
                    self.sistemas_activados.add('llantas_1')
                    print(f"Sistema activado: Llantas (Presión)")

                elif sintoma in ['Desgaste_irregular_llantas']:
                    self.declare(Sistema(area='llantas_2'))
                    self.sistemas_activados.add('llantas_2')
                    print(f"Sistema activado: Llantas (Desgaste)")

                elif sintoma in ['Vibracion_alta_velocidad']:
                    self.declare(Sistema(area='llantas_3'))
                    self.sistemas_activados.add('llantas_3')
                    print(f"Sistema activado: Llantas (Vibración)")

    def obtener_sistemas_activados(self):
        """Retorna los sistemas que necesitan diagnóstico"""
        return self.sistemas_activados.copy()
    
    def obtener_sintomas_ingresados(self):
        """Retorna los síntomas ingresados por el usuario"""
        return self.sintomas_ingresados.copy()
    
    def limpiar_hechos_temporales(self):
        """Limpia hechos temporales entre ejecuciones"""
        self.sistemas_activados.clear()
        self.sintomas_ingresados.clear()