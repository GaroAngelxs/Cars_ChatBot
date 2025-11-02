from experta import *
from hechos import *


class AsistenteAutomotriz(KnowledgeEngine):

    def __init__(self):
        super().__init__()
        self.diagnosticos_encontrados = []
        self.pregunta_actual = None

    @DefFacts()
    def _initial_action(self):
        """Hecho inicial para activar el motor."""
        yield Accion(tipo='iniciar_diagnostico')

    # Reglas simples

    @Rule(Sintoma(descripcion='humo_azul'))
    def regla_humo_azul(self):
        self.declare(Diagnostico(
            causa="Quema de aceite.",
            solucion="Posible falla de sellos o anillos de pistón desgastados.",
            severidad="Alta"
        ))

    @Rule(Sintoma(descripcion='chirrido_al_frenar'))
    def regla_chirrido_frenos(self):
        self.declare(Diagnostico(
            causa="Pastillas de freno desgastadas.",
            solucion="Reemplazar pastillas de freno inmediatamente.",
            severidad="Critica"
        ))

    # Regla de mantenimiento

    @Rule(AND(
        Estado(clave='kilometraje', valor=MATCH.km),
        Estado(clave='ultimo_servicio_km', valor=MATCH.serv_km),
        TEST(lambda km, serv_km: (km - serv_km) > 5000)
    ))
    def regla_mantenimiento_servicio(self):
        self.declare(Diagnostico(
            causa="Mantenimiento preventivo requerido por kilometraje.",
            solucion="Realizar cambio de aceite y revisión general.",
            severidad="Baja"
        ))

    # Arbol de dicison - sobrecalentamiento

    @Rule(Accion(tipo='iniciar_diagnostico'),
          Sintoma(descripcion='se_sobrecalienta'),
          NOT(Estado(clave='nivel_refrigerante')))
    def regla_arbol_calent_1_pregunta_nivel(self):
        self.declare(Pregunta(
            clave='nivel_refrigerante',
            texto='¿El nivel de refrigerante está bajo?',
            opciones=['si', 'no']
        ))

    @Rule(Sintoma(descripcion='se_sobrecalienta'),
          Estado(clave='nivel_refrigerante', valor='si'))
    def regla_arbol_calent_2_diagn_fuga(self):
        self.declare(Diagnostico(
            causa="Nivel de refrigerante bajo.",
            solucion="Posible fuga en radiador o mangueras. Rellenar y revisar.",
            severidad="Critica"
        ))

    @Rule(Sintoma(descripcion='se_sobrecalienta'),
          Estado(clave='nivel_refrigerante', valor='no'),
          NOT(Estado(clave='ventilador_funciona')))
    def regla_arbol_calent_3_pregunta_ventilador(self):
        self.declare(Pregunta(
            clave='ventilador_funciona',
            texto='Con el motor caliente, ¿el ventilador del radiador se enciende?',
            opciones=['si', 'no']
        ))

    @Rule(Sintoma(descripcion='se_sobrecalienta'),
          Estado(clave='nivel_refrigerante', valor='no'),
          Estado(clave='ventilador_funciona', valor='no'))
    def regla_arbol_calent_4_diagn_ventilador(self):
        self.declare(Diagnostico(
            causa="Falla electrica del ventilador.",
            solucion="Revisar fusible, relé o motor del ventilador.",
            severidad="Alta"
        ))

    @Rule(Sintoma(descripcion='se_sobrecalienta'),
          Estado(clave='nivel_refrigerante', valor='no'),
          Estado(clave='ventilador_funciona', valor='si'))
    def regla_arbol_calent_5_diagn_flujo(self):
        self.declare(Diagnostico(
            causa="Falla de flujo en el sistema.",
            solucion="Causa probable: Termostato atascado cerrado o radiador obstruido.",
            severidad="Alta"
        ))
        
    # arbol de decision - no arranca
    
    @Rule(Accion(tipo='iniciar_diagnostico'),
          Sintoma(descripcion='no_arranca'),
          NOT(Estado(clave='motor_gira')))
    def regla_arbol_noarranca_1_pregunta_giro(self):
        self.declare(Pregunta(
            clave='motor_gira',
            texto="Al girar la llave, ¿el motor GIRA (hace 'run-run') o NO GIRA (solo 'clic' o nada)?",
            opciones=['si_gira', 'no_gira_clic', 'no_gira_nada']
        ))

    @Rule(Sintoma(descripcion='no_arranca'),
          Estado(clave='motor_gira', valor='si_gira'))
    def regla_arbol_noarranca_2_diagn_combustible(self):
        self.declare(Diagnostico(
            causa="Falla en sistema de encendido o suministro de combustible.",
            solucion="Batería y arranque OK. Revisar bomba de combustible, filtro o bujias.",
            severidad="Media"
        ))
        
    @Rule(Sintoma(descripcion='no_arranca'),
          OR(Estado(clave='motor_gira', valor='no_gira_clic'),
             Estado(clave='motor_gira', valor='no_gira_nada')),
          NOT(Estado(clave='luces_encienden')))
    def regla_arbol_noarranca_3_pregunta_luces(self):
        self.declare(Pregunta(
            clave='luces_encienden',
            texto="¿Las luces del tablero y faros encienden con fuerza?",
            opciones=['si', 'no_tenues']
        ))

    @Rule(Sintoma(descripcion='no_arranca'),
          Estado(clave='luces_encienden', valor='no_tenues'))
    def regla_arbol_noarranca_4_diagn_bateria(self):
        self.declare(Diagnostico(
            causa="Batería descargada.",
            solucion="Batería muerta o terminales sulfatados. Requiere carga o reemplazo.",
            severidad="Alta"
        ))

    @Rule(Sintoma(descripcion='no_arranca'),
          Estado(clave='luces_encienden', valor='si'))
    def regla_arbol_noarranca_5_diagn_arranque(self):
        self.declare(Diagnostico(
            causa="Falla del motor de arranque (marcha).",
            solucion="La batería esta bien, pero el motor de arranque no funciona.",
            severidad="Alta"
        ))

    # Reglas de control

    @Rule(salience=-1)
    def limpiar_hechos_de_inicio(self):
        facts = [f for f in self.facts if isinstance(f, Accion) and f.get('tipo') == 'iniciar_diagnostico']
        if facts:
            self.retract(facts[0])
            
    @Rule(Pregunta(clave=MATCH.c, texto=MATCH.t, opciones=MATCH.o))
    def guardar_pregunta(self, c, t, o):
        self.pregunta_actual = {'clave': c, 'texto': t, 'opciones': o}

    @Rule(Diagnostico(causa=MATCH.c, solucion=MATCH.s, severidad=MATCH.sev))
    def guardar_diagnostico(self, c, s, sev):
        self.diagnosticos_encontrados.append({'causa': c, 'solucion': s, 'severidad': sev})