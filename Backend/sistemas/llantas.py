from experta import *
from core.base import SistemaBase
from hechos import *

# Especialista 1: Para Llanta baja

class SistemaLlantas1(SistemaBase):
    @Rule(Sistema(area='llantas_1'),
          NOT(Estado(clave='presion_medida')))
    def preguntar_presion(self):
        self.declare(Pregunta(
            clave='presion_medida',
            texto="¿Midió la presión con un manómetro y esta es inferior a la especificada?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='llantas_1'),
          Estado(clave='presion_medida', valor='si'))
    def diagnostico_falta_aire(self):
        self.diagnosticos_encontrados.append({
            'causa': "Llanta baja por falta de aire.",
            'solucion': "Inflar la llanta a la presión correcta indicada por el fabricante.",
            'severidad': "Baja"
        })

    @Rule(Sistema(area='llantas_1'),
          Estado(clave='presion_medida', valor='no'),
          NOT(Estado(clave='pierde_presion')))
    def preguntar_fuga(self):
        self.declare(Pregunta(
            clave='pierde_presion',
            texto="¿La llanta pierde presión consistentemente después de inflarla?",
            opciones=['si', 'no']
        ))
    
    @Rule(Sistema(area='llantas_1'),
          Estado(clave='pierde_presion', valor='si'))
    def diagnostico_fuga(self):
        self.diagnosticos_encontrados.append({
            'causa': "Posible fuga en la llanta.",
            'solucion': "Revisar la llanta en busca de perforaciones, un obús de válvula defectuoso o una fuga en el rin. Llevar a vulcanizadora.",
            'severidad': "Media"
        })

    @Rule(Sistema(area='llantas_1'),
          Estado(clave='pierde_presion', valor='no'))
    def diagnostico_sin_falla_presion(self):
        self.diagnosticos_encontrados.append({
            'causa': "La llanta está a la presión debida.",
            'solucion': "Monitorear la presión. No se detecta falla por ahora.",
            'severidad': "Baja"
        })

#Especialista 2: Para Desgaste irregular 

class SistemaLlantas2(SistemaBase):
    @Rule(Sistema(area='llantas_2'),
          NOT(Estado(clave='tipo_desgaste')))
    def preguntar_tipo_desgaste(self):
        self.declare(Pregunta(
            clave='tipo_desgaste',
            texto="¿Qué tipo de desgaste irregular presenta?",
            opciones=['desgaste_en_bordes', 'desgaste_en_parches', 'otro']
        ))

    @Rule(Sistema(area='llantas_2'),
          Estado(clave='tipo_desgaste', valor='desgaste_en_bordes'))
    def diagnostico_desalineacion(self):
        self.diagnosticos_encontrados.append({
            'causa': "Desgaste irregular en los bordes de la banda de rodadura.",
            'solucion': "El vehículo probablemente necesita una alineación.",
            'severidad': "Media"
        })

    @Rule(Sistema(area='llantas_2'),
          Estado(clave='tipo_desgaste', valor='desgaste_en_parches'))
    def diagnostico_desbalanceo(self):
        self.diagnosticos_encontrados.append({
            'causa': "Desgaste en parches o manchas irregulares.",
            'solucion': "Las ruedas probablemente necesitan un balanceo.",
            'severidad': "Media"
        })

# Especialista 3: Vibracion a alta velocidad 

class SistemaLlantas3(SistemaBase):
    @Rule(Sistema(area='llantas_3'),
          NOT(Estado(clave='lugar_vibracion')))
    def preguntar_lugar_vibracion(self):
        self.declare(Pregunta(
            clave='lugar_vibracion',
            texto="¿La vibración se siente principalmente en el volante o en el asiento/piso?",
            opciones=['volante', 'asiento_piso', 'ambos']
        ))

    @Rule(Sistema(area='llantas_3'),
          Estado(clave='lugar_vibracion', valor='volante'))
    def diagnostico_desbalanceo_delantero(self):
        self.diagnosticos_encontrados.append({
            'causa': "Vibración en el volante a alta velocidad.",
            'solucion': "Desbalanceo en las ruedas delanteras. Realizar balanceo.",
            'severidad': "Media"
        })

    @Rule(Sistema(area='llantas_3'),
          Estado(clave='lugar_Vibracion', valor='asiento_piso'))
    def diagnostico_desbalanceo_trasero(self):
        self.diagnosticos_encontrados.append({
            'causa': "Vibración en el asiento o piso a alta velocidad.",
            'solucion': "Desbalanceo en las ruedas traseras. Realizar balanceo.",
            'severidad': "Media"
        })