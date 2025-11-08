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

    # Pregunta inicial - permite MÚLTIPLES síntomas
    @Rule(Accion(tipo='iniciar_diagnostico'),
          NOT(Sintoma()))
    def preguntar_sintomas_generales(self):
        self.declare(Pregunta(
            clave='sintoma_general',
            texto="¿Qué síntomas presenta su vehículo? (puede elegir varios separados por coma)",
            opciones=[
                'no_arranca',
                'se_apaga',
                'se_calia', 
                'hace_ruidos_raros', 
                'pierde_potencia', 
                'humo_excesivo',
                'problemas_cambios',
                'frenos_defectuosos',
                'fallas_electricas',
                'vibracion_excesiva'
            ]
        ))

    # Procesar MÚLTIPLES síntomas
    @Rule(Estado(clave='sintoma_general', valor=MATCH.valores))
    def procesar_sintomas_multiples(self, valores):
        """Procesa múltiples síntomas ingresados por el usuario"""
        if isinstance(valores, str):
            # Convertir string a lista de síntomas
            sintomas = [s.strip() for s in valores.split(',')]
            self.sintomas_ingresados.update(sintomas)
            
            print(f"🔍 Síntomas identificados: {', '.join(sintomas)}")
            
            # Activar sistemas correspondientes a CADA síntoma
            for sintoma in sintomas:
                if sintoma == 'no_arranca':
                    self.declare(Sistema(area='motor'))
                    self.declare(Estado(clave='no_arranca', valor='si'))
                    self.sistemas_activados.add('motor')
                    print(f"   ✅ Sistema activado: Motor")

                elif sintoma == 'se_apaga':
                    self.declare(Sistema(area='motor'))
                    self.declare(Estado(clave='se_apaga', valor='si'))
                    self.sistemas_activados.add('motor')
                    print(f"   ✅ Sistema activado: Motor")
                    
                elif sintoma in ['se_calia']:
                    self.declare(Sistema(area='enfriamiento'))
                    self.sistemas_activados.add('enfriamiento')
                    print(f"   ✅ Sistema activado: Enfriamiento")
                    
                elif sintoma in ['problemas_cambios', 'vibracion_excesiva']:
                    self.declare(Sistema(area='transmision'))
                    self.sistemas_activados.add('transmision')
                    print(f"   ✅ Sistema activado: Transmisión")
                    
                elif sintoma in ['frenos_defectuosos']:
                    self.declare(Sistema(area='frenos'))
                    self.sistemas_activados.add('frenos')
                    print(f"   ✅ Sistema activado: Frenos")
                    
                elif sintoma in ['fallas_electricas', 'hace_ruidos_raros']:
                    self.declare(Sistema(area='electrico'))
                    self.sistemas_activados.add('electrico')
                    print(f"   ✅ Sistema activado: Eléctrico")

    # ⚠️ ELIMINADAS todas las reglas de preguntas específicas
    # El router SOLO activa sistemas, NO hace preguntas técnicas

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