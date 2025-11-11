from experta import *
from core.base import SistemaBase
from hechos import *

# "TESTIGO CHECK ENGINE" 

class SistemaSensores1(SistemaBase):
    @Rule(Sistema(area='sensores_1'),
          NOT(Estado(clave='motor_funciona_normal')))
    def preguntar_rendimiento_motor(self):
        self.declare(Pregunta(
            clave='motor_funciona_normal',
            texto="Con la luz 'CHECK ENGINE' encendida, ¿siente que el motor funcionar normalmente o presenta fallos de rendimiento/consumo?",
            opciones=['funciona_normal', 'presenta_fallos']
        ))

    @Rule(Sistema(area='sensores_1'),
          Estado(clave='motor_funciona_normal', valor='funciona_normal'))
    def diagnostico_falla_obd(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falla detectada por el sistema OBD.",
            'solucion': "El motor funciona, pero hay un codigo de error almacenado. Se recomienda escanear el vehiculo",
            'severidad': "Baja"
        })

    @Rule(Sistema(area='sensores_1'),
          Estado(clave='motor_funciona_normal', valor='presenta_fallos'))
    def diagnostico_falla_sensores_motor(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falla de sensores críticos del motor.",
            'solucion': "El fallo de rendimiento (consumo excesivo, jaloneos) indica un problema con un sensor (ej. MAF, oxígeno, cigüeñal). Requiere escaneo inmediato.",
            'severidad': "Alta"
        })

# "TESTIGO DE ACEITE"

class SistemaSensores2(SistemaBase):
    @Rule(Sistema(area='sensores_2'),
          NOT(Estado(clave='golpeteo_metalico')))
    def preguntar_golpeteo(self):
        self.declare(Pregunta(
            clave='golpeteo_metalico',
            texto="Con el testigo de 'LUZ DE ACEITE' encendido, ¿se escucha un golpeteo metalico en el motor?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='sensores_2'),
          Estado(clave='golpeteo_metalico', valor='si'))
    def diagnostico_baja_presion(self):
        self.diagnosticos_encontrados.append({
            'causa': "Baja presión de aceite.",
            'solucion': "Detenga el motor inmediatamente. Causa probable: bomba de aceite defectuosa, aceite incorrecto, o falla grave del motor. Requiere grua o jalon.",
            'severidad': "Critica"
        })

    @Rule(Sistema(area='sensores_2'),
          Estado(clave='golpeteo_metalico', valor='no'),
          NOT(Estado(clave='nivel_aceite_bajo')))
    def preguntar_nivel_aceite(self):
        self.declare(Pregunta(
            clave='nivel_aceite_bajo',
            texto="¿Reviso la varilla de nivel de aceite y marca por debajo del mínimo?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='sensores_2'),
          Estado(clave='nivel_aceite_bajo', valor='si'))
    def diagnostico_nivel_bajo(self):
        self.diagnosticos_encontrados.append({
            'causa': "Niveles bajos de aceite.",
            'solucion': "Rellenar con el aceite especificado por el fabricante hasta el nivel correcto y revisar posibles fugas.",
            'severidad': "Media"
        })

    @Rule(Sistema(area='sensores_2'),
          Estado(clave='nivel_aceite_bajo', valor='no'))
    def diagnostico_falla_sensor_aceite(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falla del sensor de presión de aceite (bulbo de aceite).",
            'solucion': "Si el nivel de aceite es normal y no hay ruidos, es probable que el sensor esté fallando y enviando una señal falsa. Reemplazar el sensor.",
            'severidad': "Baja"
        })

# "TESTIGO DE BATERIA" 

class SistemaSensores3(SistemaBase):
    @Rule(Sistema(area='sensores_3'),
          NOT(Estado(clave='voltaje_bajo')))
    def preguntar_voltaje(self):
        self.declare(Pregunta(
            clave='voltaje_bajo',
            texto="Con la 'LUZ DE BATERÍA' encendida y el motor en marcha, ¿el voltímetro (si tiene) marca menos de 13 voltios? (O las luces se ven tenues)",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='sensores_3'),
          Estado(clave='voltaje_bajo', valor='si'))
    def diagnostico_alternador(self):
        self.diagnosticos_encontrados.append({
            'causa': "El alternador no está cargando.",
            'solucion': "El vehículo está funcionando solo con la batería y se apagará pronto. Revisar banda del alternador, conexiones o reemplazar el alternador.",
            'severidad': "Critica"
        })

    @Rule(Sistema(area='sensores_3'),
          Estado(clave='voltaje_bajo', valor='no'))
    def diagnostico_falla_sensor_bateria(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falla de sensores o cableado.",
            'solucion': "Si el sistema de carga funciona (voltaje > 13.5V), la luz puede estar encendida por un falso contacto o un sensor defectuoso.",
            'severidad': "Baja"
        })

# "TESTIGO LUZ DE FRENOS"

class SistemaSensores4(SistemaBase):
    @Rule(Sistema(area='sensores_4'),
          NOT(Estado(clave='nivel_frenos_bajo')))
    def preguntar_nivel_frenos(self):
        self.declare(Pregunta(
            clave='nivel_frenos_bajo',
            texto="Con el testigo de frenos encendido, ¿el nivel del líquido de frenos esta bajo?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='sensores_4'),
          Estado(clave='nivel_frenos_bajo', valor='si'))
    def diagnostico_liquido_frenos_bajo(self):
        self.diagnosticos_encontrados.append({
            'causa': "Nivel bajo de líquido de frenos.",
            'solucion': "Puede deberse a desgaste de balatas (normal) o una fuga (peligroso). Rellenar con líquido de frenos (DOT 3/4) y revisar por fugas.",
            'severidad': "Alta"
        })

    @Rule(Sistema(area='sensores_4'),
          Estado(clave='nivel_frenos_bajo', valor='no'),
          NOT(Estado(clave='luz_abs_encendida')))
    def preguntar_luz_abs(self):
        self.declare(Pregunta(
            clave='luz_abs_encendida',
            texto="¿El testigo de 'ABS' también está encendida?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='sensores_4'),
          Estado(clave='luz_abs_encendida', valor='si'))
    def diagnostico_falla_abs(self):
        self.diagnosticos_encontrados.append({
            'causa': "Problema en el sistema de frenos ABS.",
            'solucion': "Hay una falla en el sistema ABS (sensor de rueda, módulo, etc.). El frenado normal puede funcionar, pero el ABS no. Requiere escaneo.",
            'severidad': "Media"
        })

    @Rule(Sistema(area='sensores_4'),
          Estado(clave='luz_abs_encendida', valor='no'))
    def diagnostico_falla_sensor_frenos(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falla de sensor (Nivel de líquido o freno de mano).",
            'solucion': "Si el nivel es normal y el ABS está bien, revise si el freno de mano está totalmente liberado o si el sensor del nivel de líquido está atascado.",
            'severidad': "Baja"
        })

# "TESTIGO DE TEMPERATURA"

class SistemaSensores5(SistemaBase):
    @Rule(Sistema(area='sensores_5'),
          NOT(Estado(clave='indicador_zona_roja')))
    def preguntar_indicador_temp(self):
        self.declare(Pregunta(
            clave='indicador_zona_roja',
            texto="Con el testigo de temperatura encendido, ¿el indicador de temperatura (aguja) marca en la zona roja?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='sensores_5'),
          Estado(clave='indicador_zona_roja', valor='si'))
    def diagnostico_sobrecalentamiento(self):
        self.diagnosticos_encontrados.append({
            'causa': "Motor sobrecalentado.",
            'solucion': "Detenga el vehículo en un lugar seguro y apague el motor. Causa probable: fuga de refrigerante, termostato pegado, ventilador no funciona, revisar bomba de agua.",
            'severidad': "Critica"
        })

    @Rule(Sistema(area='sensores_5'),
          Estado(clave='indicador_zona_roja', valor='no'))
    def diagnostico_falla_sensor_temp(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falla del sensor de temperatura (ECT).",
            'solucion': "Si el motor no está realmente caliente, el sensor que mide la temperatura está fallando y enviando una señal falsa a la computadora.",
            'severidad': "Baja"
        })