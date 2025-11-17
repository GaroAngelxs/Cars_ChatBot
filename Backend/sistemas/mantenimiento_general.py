from experta import *
from core.base import SistemaBase
from hechos import *

class Mantenimiento_General(SistemaBase):
    def __init__(self):
        super().__init__()

    @Rule(Sistema(area='mantenimiento_general'))
    def iniciar_diagnostico_Mantenimiento(self):
        print("Iniciando diagnóstico: Mantenimiento general")
    
    @Rule(Sistema(area='mantenimiento_general'),
          NOT(Estado(clave='km_ultimo_servicio')))
    def preguntar_km_servicio(self):
        self.declare(Pregunta(
            clave='km_ultimo_servicio',
            texto="¿El vehículo supera los 5,000 km desde el último servicio?",
            opciones=['si', 'no']
        ))
    
    #  1. Kilometros desde ultimo mantenimiento 
    @Rule(Sistema(area='mantenimiento_general'),
          Estado(clave='km_ultimo_servicio', valor='si'))
    def recomendar_servicio(self):
        self.declare(Estado(
            clave='resultado_km_servicio',
            valor="Se debe realizar cambio de aceite y revisión general"
        ))

    @Rule(Sistema(area='mantenimiento_general'),
          Estado(clave='km_ultimo_servicio', valor='no'))
    def no_requiere_servicio(self):
        self.declare(Estado(
            clave='resultado_km_servicio',
            valor="No necesita este mantenimiento"
        ))


    #  2. FILTRO DE AIRE
    @Rule(Sistema(area='mantenimiento_general'),
          Estado(clave__exists=True), 
          NOT(Estado(clave='filtro_aire_km')))
    def preguntar_filtro_aire(self):
        self.declare(Pregunta(
            clave='filtro_aire_km',
            texto="¿El filtro de aire tiene más de 10,000 km?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='mantenimiento_general'),
          Estado(clave='filtro_aire_km', valor='si'))
    def reemplazar_filtro_aire(self):
        self.declare(Estado(
            clave='resultado_filtro_aire',
            valor="Debe reemplazarse"
        ))

    @Rule(Sistema(area='mantenimiento_general'),
          Estado(clave='filtro_aire_km', valor='no'))
    def no_reemplazar_filtro_aire(self):
        self.declare(Estado(
            clave='resultado_filtro_aire',
            valor="No necesita este mantenimiento"
        ))


    #  3. BUJÍAS
    @Rule(Sistema(area='mantenimiento_general'),
          Estado(clave__exists=True),
          NOT(Estado(clave='bujias_km')))
    def preguntar_bujias(self):
        self.declare(Pregunta(
            clave='bujias_km',
            texto="¿Las bujías tienen más de 20,000 km?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='mantenimiento_general'),
          Estado(clave='bujias_km', valor='si'))
    def cambiar_bujias(self):
        self.declare(Estado(
            clave='resultado_bujias',
            valor="Deben cambiarse"
        ))

    @Rule(Sistema(area='mantenimiento_general'),
          Estado(clave='bujias_km', valor='no'))
    def no_cambiar_bujias(self):
        self.declare(Estado(
            clave='resultado_bujias',
            valor="No necesita este mantenimiento"
        ))


    #  4. BATERÍA
    @Rule(Sistema(area='mantenimiento_general'),
          Estado(clave__exists=True), 
          NOT(Estado(clave='bateria_anios')))
    def preguntar_bateria(self):
        self.declare(Pregunta(
            clave='bateria_anios',
            texto="¿La batería tiene más de 3 años?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='mantenimiento_general'),
          Estado(clave='bateria_anios', valor='si'))
    def revisar_bateria(self):
        self.declare(Estado(
            clave='resultado_bateria',
            valor="Debe revisarse su capacidad de carga"
        ))

    @Rule(Sistema(area='mantenimiento_general'),
          Estado(clave='bateria_anios', valor='no'))
    def no_revisar_bateria(self):
        self.declare(Estado(
            clave='resultado_bateria',
            valor="No necesita este mantenimiento"
        ))

    # REGLA FINAL: COMPILAR RESULTADOS 
    
    @Rule(Sistema(area='mantenimiento_general'),
          Estado(clave='resultado_km_servicio', valor=MATCH.res1),
          Estado(clave='resultado_filtro_aire', valor=MATCH.res2),
          Estado(clave='resultado_bujias', valor=MATCH.res3),
          Estado(clave='resultado_bateria', valor=MATCH.res4))
    def compilar_diagnostico_mantenimiento(self, res1, res2, res3, res4):
        
        causa = "Reporte de Mantenimiento General Preventivo."
        solucion = (
            f"1. Servicio por KM: {res1}\n"
            f"2. Filtro de Aire: {res2}\n"
            f"3. Bujías: {res3}\n"
            f"4. Batería: {res4}"
        )

        self.diagnosticos_encontrados.append({
            'causa': causa,
            'solucion': solucion,
            'severidad': "Baja"
        })