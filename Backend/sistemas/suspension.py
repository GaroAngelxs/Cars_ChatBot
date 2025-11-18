from experta import *
from core.base import SistemaBase
from hechos import *

class SistemaSuspension1(SistemaBase):
    def __init__(self):
        super().__init__()

    @Rule(Sistema(area='suspension_1'))
    def iniciar_diagnostico_transmision(self):
        print("Iniciando diagnóstico: Sistema Suspension")

    @Rule(Sistema(area='suspension_1'),
        NOT(Estado(clave='volante_vibra_alta_velocidad')))
    def preguntar_si_cambios_entran(self):
        self.declare(Pregunta(  
            clave='volante_vibra_alta_velocidad',
            texto="¿El volante vibra a alta velocidad?",
            opciones=['si', 'no']
        ))
    
    @Rule(Sistema(area='suspension_1'),
        Estado(clave='volante_vibra_alta_velocidad', valor='si'),
        NOT(Estado(clave='vibracion_progresiva')))
    def preguntar_recorrido_del_pedal(self):
        self.declare(Pregunta(
            clave='vibracion_progresiva',
            texto="¿La vibracion es progresiva? Es decir, entre mas velocidad mas vibra",
            opciones=['si', 'no']
        ))
 
    @Rule(Sistema(area='suspension_1'),
        Estado(clave='volante_vibra_alta_velocidad', valor='si'),
        Estado(clave='vibracion_progresiva', valor='no'),
        NOT(Estado(clave='volante_juego')))
    def preguntar_color_olor_del_aceite(self):
        self.declare(Pregunta(
            clave='volante_juego',
            texto="¿Al sacudir el volante se siente como si estuviera suelto?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='suspension_1'),
        Estado(clave='volante_vibra_alta_velocidad', valor='si'),
        Estado(clave='vibracion_progresiva', valor='si'))
    def diagnostico_sistema_de_transmision_embrague(self):
        self.diagnosticos_encontrados.append({
            'causa': "Desbalance en las ruedas",
            'solucion': "Balancear las ruedas",
            'severidad': "Alta"
        })
    
    @Rule(Sistema(area='suspension_1'),
        Estado(clave='volante_vibra_alta_velocidad', valor='si'),
        Estado(clave='volante_juego', valor='si'))
    def diagnostico_sistema_de_transmision_aceite(self):
        self.diagnosticos_encontrados.append({
            'causa': "Desgaste en las terminales de la direccion",
            'solucion': "Cambiar las terminales de la direccion",
            'severidad': "Alta"
        })

    # 5 – INCLINACIÓN AL GIRAR (balanceo)

    @Rule(Sistema(area='suspension_1'),
          NOT(Estado(clave='vehiculo_inclina_girar')))
    def preguntar_vehiculo_inclina_girar(self):
        self.declare(Pregunta(
            clave='vehiculo_inclina_girar',
            texto="¿El vehículo se inclina al girar?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='suspension_1'),
          Estado(clave='vehiculo_inclina_girar', valor='si'),
          NOT(Estado(clave='balanceo_excesivo')))
    def preguntar_balanceo_excesivo(self):
        self.declare(Pregunta(
            clave='balanceo_excesivo',
            texto="¿El balanceo es excesivo y continuo después del giro?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='suspension_1'),
          Estado(clave='vehiculo_inclina_girar', valor='si'),
          Estado(clave='balanceo_excesivo', valor='si'))
    def diagnostico_amortiguadores_desgastados(self):
        self.diagnosticos_encontrados.append({
            'causa': "Amortiguadores desgastados",
            'solucion': "Reemplazar los amortiguadores",
            'severidad': "Alta"
        })

    @Rule(Sistema(area='suspension_1'),
          Estado(clave='vehiculo_inclina_girar', valor='si'),
          Estado(clave='balanceo_excesivo', valor='no'))
    def diagnostico_buscar_otras_causas_5(self):
        self.diagnosticos_encontrados.append({
            'causa': "El balanceo no es excesivo",
            'solucion': "Buscar otras causas",
            'severidad': "Media"
        })

    @Rule(Sistema(area='suspension_1'),
          Estado(clave='vehiculo_inclina_girar', valor='no'))
    def no_hay_falla_5(self):
        self.diagnosticos_encontrados.append({
            'causa': "No se detecta inclinación al girar",
            'solucion': "Sin falla",
            'severidad': "Baja"
        })


    # 6 – INCLINACIÓN + RUIDO SECO

    @Rule(Sistema(area='suspension_1'),
          NOT(Estado(clave='vehiculo_inclina_girar_baches')))
    def preguntar_inclinacion_baches(self):
        self.declare(Pregunta(
            clave='vehiculo_inclina_girar_baches',
            texto="¿El vehículo se inclina al girar?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='suspension_1'),
          Estado(clave='vehiculo_inclina_girar_baches', valor='si'),
          NOT(Estado(clave='ruido_seco_baches')))
    def preguntar_ruido_seco(self):
        self.declare(Pregunta(
            clave='ruido_seco_baches',
            texto="¿Se escucha un ruido seco al pasar sobre baches?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='suspension_1'),
          Estado(clave='vehiculo_inclina_girar_baches', valor='si'),
          Estado(clave='ruido_seco_baches', valor='si'))
    def diagnostico_resortes_bujes_barra(self):
        self.diagnosticos_encontrados.append({
            'causa': "Resortes o bujes de la barra estabilizadora dañados",
            'solucion': "Reemplazar componentes dañados",
            'severidad': "Alta"
        })

    @Rule(Sistema(area='suspension_1'),
          Estado(clave='vehiculo_inclina_girar_baches', valor='si'),
          Estado(clave='ruido_seco_baches', valor='no'))
    def diagnostico_buscar_otras_causas_6(self):
        self.diagnosticos_encontrados.append({
            'causa': "No hay ruido seco",
            'solucion': "Buscar otras causas",
            'severidad': "Media"
        })

    @Rule(Sistema(area='suspension_1'),
          Estado(clave='vehiculo_inclina_girar_baches', valor='no'))
    def no_hay_falla_6(self):
        self.diagnosticos_encontrados.append({
            'causa': "No se detecta inclinación",
            'solucion': "Sin falla",
            'severidad': "Baja"
        })
 
    # 7 – GOLPETEO + RUIDO FRONTAL

    @Rule(Sistema(area='suspension_1'),
          NOT(Estado(clave='golpeteo_baches')))
    def preguntar_golpeteo_baches(self):
        self.declare(Pregunta(
            clave='golpeteo_baches',
            texto="¿Se escucha un golpeteo en baches?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='suspension_1'),
          Estado(clave='golpeteo_baches', valor='si'),
          NOT(Estado(clave='ruido_frontal')))
    def preguntar_ruido_frontal(self):
        self.declare(Pregunta(
            clave='ruido_frontal',
            texto="¿El ruido se percibe más en la parte frontal del vehículo?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='suspension_1'),
          Estado(clave='golpeteo_baches', valor='si'),
          Estado(clave='ruido_frontal', valor='si'))
    def diagnostico_bujes_suspension(self):
        self.diagnosticos_encontrados.append({
            'causa': "Bujes de suspensión dañados",
            'solucion': "Reemplazar bujes",
            'severidad': "Alta"
        })

    @Rule(Sistema(area='suspension_1'),
          Estado(clave='golpeteo_baches', valor='si'),
          Estado(clave='ruido_frontal', valor='no'))
    def diagnostico_otras_causas_7(self):
        self.diagnosticos_encontrados.append({
            'causa': "El ruido no es frontal",
            'solucion': "Buscar otras causas",
            'severidad': "Media"
        })

    @Rule(Sistema(area='suspension_1'),
          Estado(clave='golpeteo_baches', valor='no'))
    def no_hay_falla_7(self):
        self.diagnosticos_encontrados.append({
            'causa': "Sin golpeteo",
            'solucion': "Sin falla",
            'severidad': "Baja"
        })

    # 8 – GOLPETEO + JUEGO VERTICAL

    @Rule(Sistema(area='suspension_1'),
          NOT(Estado(clave='golpeteo_baches_jv')))
    def preguntar_golpeteo_baches_jv(self):
        self.declare(Pregunta(
            clave='golpeteo_baches_jv',
            texto="¿Se escucha un golpeteo en baches?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='suspension_1'),
          Estado(clave='golpeteo_baches_jv', valor='si'),
          NOT(Estado(clave='juego_vertical_ruedas')))
    def preguntar_juego_vertical(self):
        self.declare(Pregunta(
            clave='juego_vertical_ruedas',
            texto="¿Hay juego vertical en las ruedas al levantarlas con el gato?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='suspension_1'),
          Estado(clave='golpeteo_baches_jv', valor='si'),
          Estado(clave='juego_vertical_ruedas', valor='si'))
    def diagnostico_rotulas_danadas(self):
        self.diagnosticos_encontrados.append({
            'causa': "Rótulas de suspensión dañadas",
            'solucion': "Reemplazar rótulas",
            'severidad': "Alta"
        })

    @Rule(Sistema(area='suspension_1'),
          Estado(clave='golpeteo_baches_jv', valor='si'),
          Estado(clave='juego_vertical_ruedas', valor='no'))
    def diagnostico_otras_causas_8(self):
        self.diagnosticos_encontrados.append({
            'causa': "No hay juego vertical",
            'solucion': "Buscar otras causas",
            'severidad': "Media"
        })

    @Rule(Sistema(area='suspension_1'),
          Estado(clave='golpeteo_baches_jv', valor='no'))
    def no_hay_falla_8(self):
        self.diagnosticos_encontrados.append({
            'causa': "Sin golpeteo",
            'solucion': "Sin falla",
            'severidad': "Baja"
        })

    #  9 – DESVÍO + DESGASTE IRREGULAR

    @Rule(Sistema(area='suspension_1'),
          NOT(Estado(clave='vehiculo_desvia')))
    def preguntar_vehiculo_desvia(self):
        self.declare(Pregunta(
            clave='vehiculo_desvia',
            texto="¿El vehículo se desvía hacia un lado?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='suspension_1'),
          Estado(clave='vehiculo_desvia', valor='si'),
          NOT(Estado(clave='desgaste_irregular_llantas')))
    def preguntar_desgaste_llantas(self):
        self.declare(Pregunta(
            clave='desgaste_irregular_llantas',
            texto="¿Los neumáticos muestran desgaste irregular en los hombros?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='suspension_1'),
          Estado(clave='vehiculo_desvia', valor='si'),
          Estado(clave='desgaste_irregular_llantas', valor='si'))
    def diagnostico_componentes_suspension(self):
        self.diagnosticos_encontrados.append({
            'causa': "Desgaste en componentes de la suspensión",
            'solucion': "Revisar y cambiar piezas desgastadas",
            'severidad': "Alta"
        })

    @Rule(Sistema(area='suspension_1'),
          Estado(clave='vehiculo_desvia', valor='si'),
          Estado(clave='desgaste_irregular_llantas', valor='no'))
    def diagnostico_otras_causas_9(self):
        self.diagnosticos_encontrados.append({
            'causa': "No hay desgaste irregular",
            'solucion': "Buscar otras causas",
            'severidad': "Media"
        })

    @Rule(Sistema(area='suspension_1'),
          Estado(clave='vehiculo_desvia', valor='no'))
    def no_hay_falla_9(self):
        self.diagnosticos_encontrados.append({
            'causa': "El vehículo no se desvía",
            'solucion': "Sin falla",
            'severidad': "Baja"
        })


