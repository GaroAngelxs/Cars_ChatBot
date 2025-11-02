from core.router import RouterDiagnosticos
from sistemas.motor import SistemaMotor
from hechos import Vehiculo, Sistema

class CoordinadorDiagnosticos:
    def __init__(self):
        self.router = RouterDiagnosticos()
        self.sistemas = {
            'motor': SistemaMotor(),
        }
    
    def diagnosticar(self, vehiculo):
        print("Fase 1: Identificando sistemas afectados...")
        
        # Fase 1: Router identifica MÚLTIPLES sistemas
        self.router.reset()
        self.router.declare(vehiculo)
        
        # Ejecutar router para identificar todos los sistemas
        self._ejecutar_sistema_con_depuracion(self.router, "router")
        sistemas_activados = self.router.obtener_sistemas_activados()
        
        if not sistemas_activados:
            print("No se identificaron sistemas para diagnosticar")
            return []
        
        print(f"Sistemas a diagnosticar: {', '.join(sistemas_activados)}")
        
        # Fase 2: Ejecutar diagnósticos para CADA sistema
        todos_diagnosticos = []
        
        for sistema_nombre in sistemas_activados:
            if sistema_nombre in self.sistemas:
                print(f"\nDiagnosticando sistema: {sistema_nombre.upper()}")
                sistema = self.sistemas[sistema_nombre]
                sistema.reset()
                
                # TRANSFERIR hechos de forma MANUAL y DIRECTA
                self._transferir_hechos_manual(self.router, sistema, sistema_nombre)
                
                # Ejecutar sistema específico
                diagnosticos = self._ejecutar_sistema_con_depuracion(sistema, sistema_nombre)
                
                # Asegurar que cada diagnóstico tenga el campo 'sistema'
                for diag in diagnosticos:
                    if 'sistema' not in diag:
                        diag['sistema'] = sistema_nombre.capitalize()
                
                todos_diagnosticos.extend(diagnosticos)
        
        return todos_diagnosticos

    def _transferir_hechos_manual(self, origen, destino, sistema_nombre):
        """Transferencia MANUAL y DIRECTA de hechos - SIN iterar sobre facts"""
        print(f"   Transferiendo hechos manualmente...")
        
        # 1. Transferir el VEHICULO directamente
        destino.declare(Vehiculo(
            marca='Nissan',  # Estos valores deberían venir del router, pero por ahora los ponemos fijos
            modelo='Sentra', 
            anio='2018'
        ))
        print(f"      Vehículo transferido")
        
        # 2. Transferir el SISTEMA activado
        destino.declare(Sistema(area=sistema_nombre))
        print(f"      Sistema transferido: {sistema_nombre}")
        
        # DEBUG: Mostrar qué hechos quedaron
        print(f"   Hechos en sistema {sistema_nombre}:")
        for hecho in destino.facts:
            if hasattr(hecho, '__factid__'):
                if hasattr(hecho, 'marca'):
                    print(f"      - Vehiculo: {hecho.marca} {hecho.modelo}")
                elif hasattr(hecho, 'area'):
                    print(f"      - Sistema: {hecho.area}")
                else:
                    print(f"      - {type(hecho).__name__}")

    def _ejecutar_sistema_con_depuracion(self, sistema, nombre_sistema):
        """Ejecuta un sistema con información de depuración"""
        print(f"   Ejecutando motor de {nombre_sistema}...")
        
        intentos = 0
        max_intentos = 15  # Aumentamos por si hay más preguntas
        
        while intentos < max_intentos:
            intentos += 1
            
            # DEBUG: Mostrar estado actual
            print(f"   Intento {intentos} - Hechos: {len(list(sistema.facts))}")
            
            # Ejecutar el motor
            sistema.run()
            
            # Verificar si hay diagnósticos
            if sistema.diagnosticos_encontrados:
                print(f"   Se encontraron {len(sistema.diagnosticos_encontrados)} diagnósticos")
                for i, diag in enumerate(sistema.diagnosticos_encontrados):
                    print(f"      {i+1}. {diag.get('causa', 'Sin causa')}")
                return sistema.diagnosticos_encontrados
            
            # Verificar si hay pregunta pendiente
            if sistema.pregunta_actual:
                print(f"   Pregunta detectada: {sistema.pregunta_actual['clave']}")
                pregunta = sistema.pregunta_actual
                self._mostrar_pregunta(pregunta)
                respuesta = self._obtener_respuesta(pregunta)
                
                # Crear el nuevo hecho
                from hechos import Estado
                nuevo_hecho = Estado(clave=pregunta['clave'], valor=respuesta)
                
                sistema.declare(nuevo_hecho)
                sistema.pregunta_actual = None
                print(f"   Respuesta registrada: {respuesta}")
                
                continue
            
            # Si no hay diagnósticos ni preguntas, salir
            print(f"   No hay más actividad en {nombre_sistema}")
            break
        
        return sistema.diagnosticos_encontrados or []

    def _mostrar_pregunta(self, pregunta):
        print(f"\n{pregunta['texto']}")
        print(f"   Opciones: {', '.join(pregunta['opciones'])}")

    def _obtener_respuesta(self, pregunta):
        while True:
            respuesta = input("   Su respuesta: ").strip().lower()
            if respuesta in pregunta['opciones']:
                return respuesta
            print(f"   Por favor, elige entre: {', '.join(pregunta['opciones'])}")

def mostrar_bienvenida():
    print("=" * 60)
    print("           ASISTENTE AUTOMOTRIZ INTELIGENTE 🚗")
    print("=" * 60)
    print("Bienvenido! Soy tu asistente para diagnóstico de vehículos.")
    print("Te haré preguntas para identificar problemas en tu auto.")
    print()

def obtener_datos_vehiculo():
    print("Primero, necesito algunos datos de tu vehículo:")
    marca = input("   • Marca: ").strip() or "Desconocida"
    modelo = input("   • Modelo: ").strip() or "Desconocido"
    anio = input("   • Año: ").strip() or "Desconocido"
    
    print(f"   Vehículo registrado: {marca} {modelo} {anio}")
    return Vehiculo(marca=marca, modelo=modelo, anio=anio)

def mostrar_diagnosticos(diagnosticos):
    if not diagnosticos:
        print("\nNo se encontraron diagnósticos para los síntomas proporcionados.")
        return
    
    print("\n" + "=" * 60)
    print("DIAGNÓSTICOS FINALES")
    print("=" * 60)
    
    for i, diag in enumerate(diagnosticos, 1):
        sistema = diag.get('sistema', 'Sistema no especificado')
        causa = diag.get('causa', 'Causa no especificada')
        solucion = diag.get('solucion', 'Solución no especificada')
        severidad = diag.get('severidad', 'No especificada')
        
        print(f"\n{i}. SISTEMA: {sistema}")
        print(f"   CAUSA: {causa}")
        print(f"   SOLUCIÓN: {solucion}")
        print(f"   GRAVEDAD: {severidad}")

def preguntar_continuar():
    print("\n" + "=" * 50)
    respuesta = input("¿Deseas realizar otro diagnóstico? (sí/no): ").strip().lower()
    return respuesta in ['sí', 'si', 's', 'yes', 'y']

def main():
    mostrar_bienvenida()
    coordinador = CoordinadorDiagnosticos()
    
    while True:
        try:
            # Obtener datos del vehículo
            vehiculo = obtener_datos_vehiculo()
            
            # Realizar diagnóstico completo
            diagnosticos = coordinador.diagnosticar(vehiculo)
            
            # Mostrar resultados
            mostrar_diagnosticos(diagnosticos)
            
            # Preguntar si desea continuar
            if not preguntar_continuar():
                print("\n" + "=" * 60)
                print("¡Gracias por usar el Asistente Automotriz!")
                print("¡Que tengas un buen día!")
                print("=" * 60)
                break
                
        except KeyboardInterrupt:
            print("\n\nDiagnóstico interrumpido por el usuario.")
            break
        except Exception as e:
            print(f"\nError inesperado: {e}")
            import traceback
            traceback.print_exc()
            print("Por favor, intenta nuevamente.")
            continue

if __name__ == "__main__":
    main()