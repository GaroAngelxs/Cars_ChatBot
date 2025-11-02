from experta import Fact


class Vehiculo(Fact):
    """Hecho estatico del vehículo"""
    pass

class Sintoma(Fact):
    """Síntoma del checkbox que el usuario selecciono"""
    pass

class Estado(Fact):
    """Respuesta del usuario a una pregunta"""
    pass

class Pregunta(Fact):
    """Hecho especial que el motor genera para el chatbot """
    pass

class Diagnostico(Fact):
    """La conclusion final del sistema"""
    pass

class Accion(Fact):
    """Hecho de control para el motor."""
    pass