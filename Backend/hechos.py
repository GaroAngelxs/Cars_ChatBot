from experta import Fact
"""
Definición de los hechos (Facts) utilizados por el sistema experto Cars_ChatBot.

Este módulo contiene las clases base que representan:
- Sistema: identifica el área o subsistema del vehículo que se va a diagnosticar
  (motor, frenos, combustible, eléctrico, etc.).
- Estado: almacena información sobre síntomas u observaciones que se han ido
  confirmando durante la sesión de diagnóstico.
- Pregunta: representa una pregunta pendiente que el motor de reglas debe hacer
  al usuario para poder continuar con la inferencia.
"""

class Vehiculo(Fact):
    """Información del vehículo"""
    pass

class Sintoma(Fact):
    """Síntoma del vehículo"""
    pass

class Sistema(Fact):
    """Sistema del vehículo con problema"""
    """Hecho que indica el área del vehículo que se está diagnosticando.

    El campo 'area' se utiliza para activar el conjunto de reglas correspondiente
    a un sistema especialista (por ejemplo: 'motor_1', 'frenos_3', 'combustible_2').
    """
    pass

class Estado(Fact):
    """Estado de un componente"""
    """Hecho que almacena un dato concreto sobre el estado del vehículo.

    Se utiliza para guardar síntomas, condiciones o resultados de preguntas.
    Atributos típicos:
    - clave: nombre simbólico del dato (ej. 'pedal_esponjoso', 'tarda_en_arrancar').
    - valor: respuesta u observación asociada (ej. 'si', 'no', 'alto', 'bajo').
    """
    pass

class Pregunta(Fact):
    """Pregunta al usuario"""
    """Hecho que representa una pregunta que el sistema debe hacer al usuario.

    Este hecho se declara cuando una regla necesita información adicional.
    Atributos típicos:
    - clave: identificador interno de la pregunta.
    - texto: texto que verá el usuario en la interfaz.
    - opciones: lista de respuestas válidas esperadas (ej. ['si', 'no']).
    """
    pass

class Diagnostico(Fact):
    """Diagnóstico final"""
    pass

class Accion(Fact):
    """Acción del sistema"""
    pass