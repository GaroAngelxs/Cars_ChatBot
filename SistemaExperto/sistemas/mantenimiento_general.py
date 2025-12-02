"""
Sistema especialista para mantenimiento general preventivo del vehículo.

Este módulo define la clase Mantenimiento_General, que se encarga de hacer
preguntas básicas sobre kilometraje y tiempo de uso de algunos componentes
(aceite, filtro de aire, bujías y batería) para generar un reporte general
de mantenimiento sugerido.
"""

from experta import *
from core.base import SistemaBase
from hechos import *

class Mantenimiento_General(SistemaBase):
    """
    Sistema especialista de mantenimiento general.

    Este sistema se activa con el área 'mantenimiento_general' y, mediante
    una serie de preguntas encadenadas, determina si se recomienda o no:
    - Servicio por kilometraje (aceite y revisión general).
    - Reemplazo del filtro de aire.
    - Cambio de bujías.
    - Revisión de la batería.

    Al final compila un reporte único de mantenimiento preventivo y lo
    agrega a la lista `diagnosticos_encontrados`.
    """
    def __init__(self):
        """Inicializa el sistema de mantenimiento general."""
        super().__init__()

    @Rule(Sistema(area='mantenimiento_general'))
    def iniciar_diagnostico_Mantenimiento(self):
        print("Iniciando diagnóstico: Mantenimiento general")
    
    @Rule(Sistema(area='mantenimiento_general'),
          NOT(Estado(clave='km_ultimo_servicio')))
    def preguntar_km_servicio(self):
        """
        Pregunta si el vehículo supera los kilómetros recomendados desde
        el último servicio.

        Clave generada:
        - km_ultimo_servicio: 'si' o 'no'
        """
        self.declare(Pregunta(
            clave='km_ultimo_servicio',
            texto="¿El vehículo supera los 5,000 km desde el último servicio?",
            opciones=['si', 'no']
        ))
    
    #  1. KM DESDE EL ULTIMO MANTENIMIENTOS
    @Rule(Sistema(area='mantenimiento_general'),
          Estado(clave='km_ultimo_servicio', valor='si'))
    def recomendar_servicio(self):
        """
        Si el vehículo supera los 5,000 km desde el último servicio,
        recomienda realizar cambio de aceite y revisión general.
        """
        self.declare(Estado(
            clave='resultado_km_servicio',
            valor="Se debe realizar cambio de aceite y revisión general"
        ))

    @Rule(Sistema(area='mantenimiento_general'),
          Estado(clave='km_ultimo_servicio', valor='no'))
    def no_requiere_servicio(self):
        """
        Si el vehículo no supera el kilometraje indicado, no recomienda
        este mantenimiento por kilómetros.
        """
        self.declare(Estado(
            clave='resultado_km_servicio',
            valor="No necesita este mantenimiento"
        ))


    #  2. FILTRO DE AIRE
    @Rule(Sistema(area='mantenimiento_general'),
          Estado(clave='resultado_km_servicio'), 
          NOT(Estado(clave='filtro_aire_km')))
    def preguntar_filtro_aire(self):
        """
        Una vez resuelto el servicio por km, pregunta por el filtro de aire:
        si tiene más de 10,000 km de uso.

        Clave generada:
        - filtro_aire_km: 'si' o 'no'
        """
        self.declare(Pregunta(
            clave='filtro_aire_km',
            texto="¿El filtro de aire tiene más de 10,000 km?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='mantenimiento_general'),
          Estado(clave='filtro_aire_km', valor='si'))
    def reemplazar_filtro_aire(self):
        """Recomienda reemplazar el filtro de aire si supera los 10,000 km."""
        self.declare(Estado(
            clave='resultado_filtro_aire',
            valor="Debe reemplazarse"
        ))

    @Rule(Sistema(area='mantenimiento_general'),
          Estado(clave='filtro_aire_km', valor='no'))
    def no_reemplazar_filtro_aire(self):
        """Indica que el filtro de aire no requiere mantenimiento por km."""
        self.declare(Estado(
            clave='resultado_filtro_aire',
            valor="No necesita este mantenimiento"
        ))


    #  3. BUJÍAS
    @Rule(Sistema(area='mantenimiento_general'),
          Estado(clave='resultado_filtro_aire'),
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
        """
        Una vez evaluado el filtro de aire, pregunta por el kilometraje de las bujías.

        Clave generada:
        - bujias_km: 'si' (más de 20,000 km) o 'no'
        """
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
          Estado(clave='resultado_bujias'),
          NOT(Estado(clave='bateria_anios')))
    def preguntar_bateria(self):
        """
        Una vez evaluadas las bujías, pregunta por la antigüedad de la batería.

        Clave generada:
        - bateria_anios: 'si' (más de 3 años) o 'no'
        """
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


    # REGLA FINAL PARA COMPILAR EL DIAGNÓSTICO 
    @Rule(Sistema(area='mantenimiento_general'),
          Estado(clave='resultado_km_servicio', valor=MATCH.res1),
          Estado(clave='resultado_filtro_aire', valor=MATCH.res2),
          Estado(clave='resultado_bujias', valor=MATCH.res3),
          Estado(clave='resultado_bateria', valor=MATCH.res4))
    def compilar_diagnostico_mantenimiento(self, res1, res2, res3, res4):
        """
        Regla final que compila todos los resultados parciales
        del mantenimiento general.

        Usa los valores almacenados en:
        - resultado_km_servicio
        - resultado_filtro_aire
        - resultado_bujias
        - resultado_bateria

        Y genera un único diagnóstico descriptivo de mantenimiento preventivo.
        """
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