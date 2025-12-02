from experta import *
from core.base import SistemaBase
from hechos import *

"""
Sistema especialista para el diagnóstico del sistema de suspencion.

Este módulo define varios subconjuntos de reglas (suspencion1, suspencion2,
etc.), cada uno enfocado en un grupo de síntomas específicos como:

- vibracion en el volante.
- volante duro.
- Inclinacion al girar.
- golpeteo en baches.
- Desvio del vehiculo.

Cada clase hereda de SistemaBase y utiliza hechos Estado/Pregunta para
interactuar con el usuario y generar diagnósticos estructurados.
"""


# --- 1. VIBRACIÓN EN EL VOLANTE (SistemaSuspension1) ---
class SistemaSuspension1(SistemaBase):
    @Rule(Sistema(area='suspension_1'),
          NOT(Estado(clave='vibracion_progresiva')))
    def preguntar_vibracion_progresiva(self):
        self.declare(Pregunta(
            clave='vibracion_progresiva',
            texto="La vibración en el volante... ¿aumenta progresivamente conforme aumenta la velocidad?",
            opciones=['si', 'no']
        ))
    
    @Rule(Sistema(area='suspension_1'),
          Estado(clave='vibracion_progresiva', valor='si'))
    def diagnostico_desbalance(self):
        self.diagnosticos_encontrados.append({
            'causa': "Desbalance de ruedas.",
            'solucion': "Las llantas necesitan balanceo y rotación.",
            'severidad': "Media"
        })

    @Rule(Sistema(area='suspension_1'),
          Estado(clave='vibracion_progresiva', valor='no'),
          NOT(Estado(clave='juego_direccion')))
    def preguntar_juego_direccion(self):
        self.declare(Pregunta(
            clave='juego_direccion',
            texto="¿Siente 'juego' o holgura en la dirección al mover el volante (se mueve sin que las llantas giren)?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='suspension_1'),
          Estado(clave='vibracion_progresiva', valor='no'),
          Estado(clave='juego_direccion', valor='si'))
    def diagnostico_terminales(self):
        self.diagnosticos_encontrados.append({
            'causa': "Desgaste en los terminales de dirección.",
            'solucion': "Reemplazar las terminales de dirección y alinear.",
            'severidad': "Alta"
        })

# --- 2. VOLANTE DURO (SistemaDireccion1) ---
class SistemaDireccion1(SistemaBase):
    @Rule(Sistema(area='direccion_1'),
          NOT(Estado(clave='nivel_liquido_bajo')))
    def preguntar_nivel_liquido(self):
        self.declare(Pregunta(
            clave='nivel_liquido_bajo',
            texto="¿El nivel de líquido de dirección hidráulica está por debajo del mínimo?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='direccion_1'),
          Estado(clave='nivel_liquido_bajo', valor='si'))
    def diagnostico_falta_liquido(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falta líquido hidráulico.",
            'solucion': "Rellenar el depósito con líquido de dirección y buscar fugas.",
            'severidad': "Media"
        })

    @Rule(Sistema(area='direccion_1'),
          Estado(clave='nivel_liquido_bajo', valor='no'),
          NOT(Estado(clave='rechinido_al_girar')))
    def preguntar_rechinido(self):
        self.declare(Pregunta(
            clave='rechinido_al_girar',
            texto="¿Se escucha un rechinido al girar el volante con el motor encendido?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='direccion_1'),
          Estado(clave='nivel_liquido_bajo', valor='no'),
          Estado(clave='rechinido_al_girar', valor='si'))
    def diagnostico_bomba_direccion(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falla en la bomba de dirección asistida.",
            'solucion': "La bomba está fallando o la banda está patinando. Revisar banda y bomba.",
            'severidad': "Alta"
        })

# --- 3. INCLINACIÓN AL GIRAR  ---
class SistemaSuspension2(SistemaBase):
    @Rule(Sistema(area='suspension_2'),
          NOT(Estado(clave='balanceo_continuo')))
    def preguntar_balanceo(self):
        self.declare(Pregunta(
            clave='balanceo_continuo',
            texto="Después del giro, ¿el vehículo sigue balanceándose excesivamente?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='suspension_2'),
          Estado(clave='balanceo_continuo', valor='si'))
    def diagnostico_amortiguadores(self):
        self.diagnosticos_encontrados.append({
            'causa': "Amortiguadores desgastados.",
            'solucion': "Reemplazar los amortiguadores (en pares).",
            'severidad': "Alta"
        })

    @Rule(Sistema(area='suspension_2'),
          Estado(clave='balanceo_continuo', valor='no'),
          NOT(Estado(clave='ruido_seco_baches')))
    def preguntar_ruido_seco(self):
        self.declare(Pregunta(
            clave='ruido_seco_baches',
            texto="¿Se escucha un ruido seco (golpe) al pasar sobre baches?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='suspension_2'),
          Estado(clave='balanceo_continuo', valor='no'),
          Estado(clave='ruido_seco_baches', valor='si'))
    def diagnostico_barra_estabilizadora(self):
        self.diagnosticos_encontrados.append({
            'causa': "Resortes o bujes de la barra estabilizadora dañados.",
            'solucion': "Revisar gomas y tornillos de la barra estabilizadora.",
            'severidad': "Media"
        })

# --- 4. GOLPETEO EN BACHES ---
class SistemaSuspension3(SistemaBase):
    @Rule(Sistema(area='suspension_3'),
          NOT(Estado(clave='ruido_frontal')))
    def preguntar_ubicacion_ruido(self):
        self.declare(Pregunta(
            clave='ruido_frontal',
            texto="¿El ruido se percibe más en la parte frontal del vehículo?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='suspension_3'),
          Estado(clave='ruido_frontal', valor='si'))
    def diagnostico_bujes(self):
        self.diagnosticos_encontrados.append({
            'causa': "Bujes de suspensión dañados.",
            'solucion': "Reemplazar los bujes de las horquillas de suspensión.",
            'severidad': "Media"
        })

    @Rule(Sistema(area='suspension_3'),
          Estado(clave='ruido_frontal', valor='no'),
          NOT(Estado(clave='juego_vertical')))
    def preguntar_juego_vertical(self):
        self.declare(Pregunta(
            clave='juego_vertical',
            texto="Al levantar el auto, ¿hay juego vertical en las ruedas al moverlas?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='suspension_3'),
          Estado(clave='ruido_frontal', valor='no'),
          Estado(clave='juego_vertical', valor='si'))
    def diagnostico_rotulas(self):
        self.diagnosticos_encontrados.append({
            'causa': "Rótulas de suspensión dañadas.",
            'solucion': "Reemplazar las rótulas inmediatamente. Peligro de seguridad.",
            'severidad': "Critica"
        })

# --- 5. DESVÍO DEL VEHÍCULO  ---
class SistemaSuspension4(SistemaBase):
    @Rule(Sistema(area='suspension_4'),
          NOT(Estado(clave='desgaste_hombros')))
    def preguntar_desgaste_hombros(self):
        self.declare(Pregunta(
            clave='desgaste_hombros',
            texto="¿Los neumáticos muestran desgaste irregular en los hombros (bordes)?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='suspension_4'),
          Estado(clave='desgaste_hombros', valor='si'))
    def diagnostico_componentes(self):
        self.diagnosticos_encontrados.append({
            'causa': "Desgaste en componentes de suspensión.",
            'solucion': "Revisar horquillas y amortiguadores doblados, luego alinear.",
            'severidad': "Alta"
        })