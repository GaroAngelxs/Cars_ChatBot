from experta import *
from core.base import SistemaBase
from hechos import *

class SistemaEnfriamiento1(SistemaBase):
    def __init__(self):
        super().__init__()

    @Rule(Sistema(area='enfriamiento_1'))
    def iniciar_diagnostico_enfriamiento(self):
        print("Iniciando diagnóstico: Sistema Enfriamiento")

    @Rule(Sistema(area='enfriamiento_1'),
        NOT(Estado(clave='signos_de_sobrecalentamiento')))
    def preguntar_si_hay_sobrecalentamiento(self):
        self.declare(Pregunta(  
            clave='signos_de_sobrecalentamiento',
            texto="¿Hay una luz de temperatura en el tablero o la aguja de temperatura esta muy arriba?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='enfriamiento_1'),
        Estado(clave='signos_de_sobrecalentamiento', valor='si'),
        NOT(Estado(clave='nivel_anticongelante')))
    def preguntar_nivel_anticongelante(self):
        self.declare(Pregunta(  
            clave='nivel_anticongelante',
            texto="¿El nivel del anticongelante en el depositivo esta bajo?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='enfriamiento_1'),
        Estado(clave='signos_de_sobrecalentamiento', valor='si'),
        Estado(clave='nivel_anticongelante', valor='no'),
        NOT(Estado(clave='temperatura_mangueras')))
    def preguntar_temperatura_mangueras(self):
        self.declare(Pregunta(  
            clave='temperatura_mangueras',
            texto="¿Las mangueras que salen del radiador estan calientes?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='enfriamiento_1'),
        Estado(clave='signos_de_sobrecalentamiento', valor='si'),
        Estado(clave='nivel_anticongelante', valor='si'))
    def diagnostico_sistema_de_enfriamiento_anticongelante(self):
        self.diagnosticos_encontrados.append({
            'causa': "Falta refrigerante en el sistema",
            'solucion': "Llenar el refrigereante faltante",
            'severidad': "Alta"
        })
    
    @Rule(Sistema(area='enfriamiento_1'),
        Estado(clave='signos_de_sobrecalentamiento', valor='si'),
        Estado(clave='temperatura_mangueras', valor='si'))
    def diagnostico_sistema_de_enfriamiento_termostato(self):
        self.diagnosticos_encontrados.append({
            'causa': "Termostato en mal estado",
            'solucion': "Cambiar el termostato",
            'severidad': "Alta"
        })

class SistemaEnfriamiento2(SistemaBase):
    def __init__(self):
        super().__init__()

    @Rule(Sistema(area='enfriamiento_2'))
    def iniciar_diagnostico_enfriamiento(self):
        print("Iniciando diagnóstico: Sistema Enfriamiento")

    @Rule(Sistema(area='enfriamiento_2'),
        NOT(Estado(clave='fugas_anticongelante')))
    def preguntar_sobre_fuga(self):
        self.declare(Pregunta(  
            clave='fugas_anticongelante',
            texto="¿La fuga de liquido verde o rojo siempre aparece despues de dejar el auto estacionado un tiempo?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='enfriamiento_2'),
        Estado(clave='fugas_anticongelante', valor='si'),
        NOT(Estado(clave='donde_fuga')))
    def preguntar_de_donde_fuga(self):
        self.declare(Pregunta(  
            clave='donde_fuga',
            texto="¿La fuga de liquido esta en la parte delantera del motor?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='enfriamiento_2'),
        Estado(clave='fugas_anticongelante', valor='si'),
        Estado(clave='donde_fuga', valor='no'),
        NOT(Estado(clave='fuga_cerca_motor')))
    def preguntar_temperatura_mangueras(self):
        self.declare(Pregunta(  
            clave='fuga_cerca_motor',
            texto="¿La fuga de liquido esta debajo del motor?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='enfriamiento_2'),
        Estado(clave='fugas_anticongelante', valor='si'),
        Estado(clave='donde_fuga', valor='si'))
    def diagnostico_sistema_de_enfriamiento_fuga_radiador(self):
        self.diagnosticos_encontrados.append({
            'causa': "Fuga en el radiador",
            'solucion': "Cambiar el radiador",
            'severidad': "Alta"
        })
    
    @Rule(Sistema(area='enfriamiento_2'),
        Estado(clave='fugas_anticongelante', valor='si'),
        Estado(clave='fuga_cerca_motor', valor='si'))
    def diagnostico_sistema_de_enfriamiento_fuga_manguera(self):
        self.diagnosticos_encontrados.append({
            'causa': "Fuga en una manguera",
            'solucion': "Cmabiar la manguera en mal estado",
            'severidad': "Alta"
        })

class SistemaEnfriamiento3(SistemaBase):
    def __init__(self):
        super().__init__()

    @Rule(Sistema(area='enfriamiento_3'))
    def iniciar_diagnostico_enfriamiento(self):
        print("Iniciando diagnóstico: Sistema Enfriamiento")

    @Rule(Sistema(area='enfriamiento_3'),
        NOT(Estado(clave='ventilador_enciende')))
    def preguntar_sobre_fuga(self):
        self.declare(Pregunta(  
            clave='ventilador_enciende',
            texto="¿El ventilador enciende o gira?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='enfriamiento_3'),
        Estado(clave='ventilador_enciende', valor='no'),
        NOT(Estado(clave='energia_llega')))
    def preguntar_de_donde_fuga(self):
        self.declare(Pregunta(  
            clave='energia_llega',
            texto="¿Hay energia llegando al rele que activa el ventilador?",
            opciones=['si', 'no']
        ))

    @Rule(Sistema(area='enfriamiento_3'),
        Estado(clave='ventilador_enciende', valor='no'),
        Estado(clave='energia_llega', valor='si'),
        NOT(Estado(clave='directo_ventilador')))
    def preguntar_temperatura_mangueras(self):
        self.declare(Pregunta(  
            clave='directo_ventilador',
            texto="¿El ventilador enciende si lo alimentas directamente?",
            opciones=['si', 'no']
        ))

    #Diagnostico

    @Rule(Sistema(area='enfriamiento_3'),
        Estado(clave='ventilador_enciende', valor='no'),
        Estado(clave='energia_llega', valor='no'))
    def diagnostico_sistema_de_enfriamiento_fusible_quemado(self):
        self.diagnosticos_encontrados.append({
            'causa': "Fusible quemado",
            'solucion': "Cambiar fusible",
            'severidad': "Alta"
        })

    @Rule(Sistema(area='enfriamiento_3'),
        Estado(clave='ventilador_enciende', valor='no'),
        Estado(clave='energia_llega', valor='si'),
        Estado(clave='directo_ventilador',valor = 'si'))
    def diagnostico_sistema_de_enfriamiento_rele_quemado(self):
        self.diagnosticos_encontrados.append({
            'causa': "Rele de ventilador en mal estado",
            'solucion': "Cambiar el rele en mal estado",
            'severidad': "Alta"
        })

    @Rule(Sistema(area='enfriamiento_3'),
        Estado(clave='ventilador_enciende', valor='no'),
        Estado(clave='energia_llega', valor='si'),
        Estado(clave='directo_ventilador', valor='no'))
    def diagnostico_sistema_de_enfriamiento_motor_malo(self):
        self.diagnosticos_encontrados.append({
            'causa': "Motor de ventilador en mal estado",
            'solucion': "Cambiar motor de ventilador",
            'severidad': "Alta"
        })




