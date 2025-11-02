from motor import AsistenteAutomotriz
from hechos import Vehiculo, Sintoma, Estado


def simular_chatbot(motor, hechos_iniciales):

    motor.reset()
    motor.diagnosticos_encontrados = []
    motor.pregunta_actual = None
    
    print(f" CHATBOT:...")
    for hecho in hechos_iniciales:
        motor.declare(hecho)
        print(f"   -> Hecho declarado: {hecho}")

    while True:
        motor.run() 

        if motor.diagnosticos_encontrados:
            print("\n DIAGNÓSTICO FINAL DEL ASISTENTE:")
            for diag in motor.diagnosticos_encontrados:
                print(f"   - Causa: {diag['causa']}")
                print(f"   - Solución: {diag['solucion']}")
                print(f"   - Severidad: {diag['severidad']}")
            break 

        elif motor.pregunta_actual:
            pregunta = motor.pregunta_actual
            print(f"\ PREGUNTA DEL ASISTENTE:")
            print(f"   {pregunta['texto']}")
            print(f"   Opciones: {pregunta['opciones']}")
            
            respuesta_usuario = input("   Respuesta del usuario: ")
            
            motor.pregunta_actual = None
            
            nuevo_hecho = Estado(clave=pregunta['clave'], valor=respuesta_usuario)
            motor.declare(nuevo_hecho)
            print(f"   -> Hecho declarado: {nuevo_hecho}")
        
        else:
            print("\n CHATBOT: No se pudo encontrar un diagnóstico con la información proporcionada.")
            break


if __name__ == "__main__":

    asistente = AsistenteAutomotriz()
    print("======================================================")
    print("=== SIMULACIÓN 1: CHECKBOX DE 'CHIRRIDO AL FRENAR' ===")
    print("======================================================")
    
    hechos_simples = [
        Vehiculo(marca='Nissan', modelo='Sentra', anio=2018),
        Sintoma(descripcion='chirrido_al_frenar')
    ]
    simular_chatbot(asistente, hechos_simples)
    

    print("\n\n==========================================================")
    print("=== SIMULACIÓN 2: ÁRBOL DE 'SE SOBRECALIENTA'        ===")
    print("=== (Usuario responde 'no' y luego 'si')           ===")
    print("==========================================================")
    
    hechos_complejos = [
        Vehiculo(marca='VW', modelo='Jetta', anio=2010),
        Sintoma(descripcion='se_sobrecalienta')
    ]
    
    simular_chatbot(asistente, hechos_complejos)
