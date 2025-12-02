# Imports

import flet as ft
from core.router import RouterDiagnosticos
from sistemas.motor import *
from sistemas.transmision import *
from sistemas.llantas import *
from sistemas.enfriamiento import *
from sistemas.electrico import *
from sistemas.frenos import *
from sistemas.combustible import *
from sistemas.escape import *
from sistemas.fluidos import *
from sistemas.aire_acondicionado import *
from sistemas.sensores_tablero import *
from sistemas.suspension import *
from sistemas.direccion import *
from sistemas.mantenimiento_general import Mantenimiento_General
from hechos import Vehiculo, Estado, Sistema 

# ==========================================
# Logica Clase Coordinador (Backend)
# ==========================================
class Coordinador:
    def __init__(self, vehiculo):
        self.vehiculo = vehiculo
        self.router = RouterDiagnosticos()
        
        self.sistemas_especialistas = {
            'motor_1': SistemaMotor1(),
            'motor_2': SistemaMotor2(),
            'motor_3': SistemaMotor3(),
            'motor_4': SistemaMotor4(),
            'motor_5': SistemaMotor5(),
            'motor_6': SistemaMotor6(),
            'transmision_1': SistemaTransmision1(),
            'transmision_2': SistemaTransmision2(),
            'transmision_3': SistemaTransmision3(),
            'transmision_4': SistemaTransmision4(),
            'llantas_1': SistemaLlantas1(),
            'llantas_2': SistemaLlantas2(),
            'llantas_3': SistemaLlantas3(),
            'enfriamiento_1': SistemaEnfriamiento1(),
            'enfriamiento_2': SistemaEnfriamiento2(),
            'enfriamiento_3': SistemaEnfriamiento3(),
            'electrico_1': SistemaElectrico1(),
            'electrico_2': SistemaElectrico2(),
            'electrico_3': SistemaElectrico3(),
            'electrico_4': SistemaElectrico4(),
            'frenos_1': SistemaFrenos1(),
            'frenos_2': SistemaFrenos2(),
            'frenos_3': SistemaFrenos3(),
            'frenos_4': SistemaFrenos4(),
            'combustible_1': SistemaCombustible1(),
            'combustible_2': SistemaCombustible2(),
            'combustible_3': SistemaCombustible3(),
            'combustible_4': SistemaCombustible4(),
            'escape_1': SistemaEscape1(),
            'escape_2': SistemaEscape2(),
            'escape_3': SistemaEscape3(),
            'fluidos_1': SistemaFluidos1(),
            'fluidos_2': SistemaFluidos2(),
            'fluidos_3': SistemaFluidos3(),
            'fluidos_4': SistemaFluidos4(),
            'acondicionado_1': SistemaAcondicionado1(),
            'acondicionado_2': SistemaAcondicionado2(),
            'acondicionado_3': SistemaAcondicionado3(),
            'acondicionado_4': SistemaAcondicionado4(),
            'sensores_1': SistemaSensores1(),
            'sensores_2': SistemaSensores2(),
            'sensores_3': SistemaSensores3(),
            'sensores_4': SistemaSensores4(),
            'sensores_5': SistemaSensores5(),
            'suspension_1': SistemaSuspension1(),
            'suspension_2': SistemaSuspension2(),
            'suspension_3': SistemaSuspension3(),
            'suspension_4': SistemaSuspension4(),
            'direccion_1': SistemaDireccion1(),
            'mantenimiento_general': Mantenimiento_General()
        }

        self.sistemas_activados = []
        self.diagnosticos_finales = []
        
        self.router.reset()
        self.router.declare(self.vehiculo)

    def procesar(self, respuesta=None):
        if not self.sistemas_activados:
            if respuesta:
                self.router.declare(Estado(clave=respuesta['clave'], valor=respuesta['valor']))
                self.router.run()
            
            self.router.run()
            
            pregunta = self.router.obtener_pregunta_actual()
            if pregunta:
                self.router.limpiar_pregunta_actual()
                return {'pregunta': pregunta}
            
            self.sistemas_activados = list(self.router.obtener_sistemas_activados())
            if not self.sistemas_activados:
                return {'diagnosticos': [{'causa': 'No se identificaron sistemas afectados.', 'solucion': 'Intente con otros síntomas.', 'severidad': 'Baja'}]}
            
            print(f"Sistemas activados: {self.sistemas_activados}")
            respuesta = None

        while self.sistemas_activados:
            sistema_nombre = self.sistemas_activados[0]
            
            if sistema_nombre not in self.sistemas_especialistas:
                print(f"Advertencia: No se encontró el motor especialista para '{sistema_nombre}'")
                self.sistemas_activados.pop(0)
                continue

            sistema = self.sistemas_especialistas[sistema_nombre]

            if not hasattr(sistema, '_inicializado'):
                sistema.reset()
                self._transferir_hechos(self.router, sistema, sistema_nombre)
                setattr(sistema, '_inicializado', True)

            if respuesta:
                sistema.declare(Estado(clave=respuesta['clave'], valor=respuesta['valor']))

            sistema.run()

            pregunta = sistema.obtener_pregunta_actual()
            if pregunta:
                sistema.limpiar_pregunta_actual()
                return {'pregunta': pregunta}
            
            diags = sistema.obtener_diagnosticos()
            for diag in diags:
                if 'sistema' not in diag:
                    diag['sistema'] = sistema_nombre.replace('_', ' ').capitalize()
            
            self.diagnosticos_finales.extend(diags)
            self.sistemas_activados.pop(0)
            respuesta = None 

        return {'diagnosticos': self.diagnosticos_finales or [{'causa': 'No se encontraron problemas específicos.', 'solucion': 'El sistema no detectó fallas con la información dada.', 'severidad': 'Baja'}]}

    def _transferir_hechos(self, origen, destino, sistema_nombre):
        destino.declare(self.vehiculo)
        destino.declare(Sistema(area=sistema_nombre))
        for hecho in origen.facts.values():
            if isinstance(hecho, Estado):
                hecho_dict = {k: v for k, v in hecho.items()}
                destino.declare(Estado(**hecho_dict))

# ==========================================
# INTERFAZ GRÁFICA (Frontend)
# ==========================================

def main(page: ft.Page):
    # Configuraciones del front
    page.title = "Sistema Experto Automotriz"
    page.window_width = 900
    page.window_height = 750
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    
    COLOR_BG_MAIN = "#E3F2FD"    
    COLOR_HEADER = '#1565C0'      
    COLOR_ACCENT = '#1976D2'       
    COLOR_CONFIRM = '#2196F3'     
    COLOR_BG_CARD = '#ffffff'      
    COLOR_BG_INTERNAL = "#BBDEFB"  
    COLOR_TEXT_SUBTLE = ft.Colors.BLUE_GREY_700 
    SHADOW_COLOR = "#33000000"     
    page.bgcolor = COLOR_BG_MAIN

    # Estados
    state = {
        "coordinador": None,
        "vehiculo_data": None,
        "pregunta_actual": None
    }

    # Barra de progreso azul
    progress_bar = ft.ProgressBar(width=None, value=0, color=COLOR_ACCENT, bgcolor=COLOR_BG_INTERNAL)
    
    # Contenedor principal del contenido
    content_container = ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        padding=20
    )

    # Funciones de logica

    def mostrar_mensaje(texto, color=ft.Colors.RED): 
        page.snack_bar = ft.SnackBar(ft.Text(texto), bgcolor=color)
        page.snack_bar.open = True
        page.update()

    def actualizar_progreso(valor):
        progress_bar.value = valor
        page.update()

    def iniciar_diagnostico(e):
        marca = input_marca.value
        modelo = input_modelo.value
        anio = input_anio.value

        state["vehiculo_data"] = {'marca': marca, 'modelo': modelo, 'anio': anio}
        
        vehiculo = Vehiculo(
            marca=marca or "Desconocido",
            modelo=modelo or "Desconocido",
            anio=anio or "0000"
        )
        
        state["coordinador"] = Coordinador(vehiculo)
        resultado = state["coordinador"].procesar()
        procesar_resultado(resultado)

    def reiniciar(e):
        state["coordinador"] = None
        if state["vehiculo_data"]:
            vehiculo = Vehiculo(
                marca=state["vehiculo_data"]['marca'] or "Desconocido",
                modelo=state["vehiculo_data"]['modelo'] or "Desconocido",
                anio=state["vehiculo_data"]['anio'] or "0000"
            )
            state["coordinador"] = Coordinador(vehiculo)
            resultado = state["coordinador"].procesar()
            procesar_resultado(resultado)
        else:
            mostrar_pantalla_vehiculo()

    def procesar_resultado(resultado):
        if 'pregunta' in resultado:
            mostrar_pantalla_pregunta(resultado['pregunta'])
        elif 'diagnosticos' in resultado:
            mostrar_pantalla_diagnostico(resultado['diagnosticos'])
        else:
            mostrar_mensaje("Error Crítico: Estado inválido del motor de inferencia.")

    def enviar_respuesta(clave, valor):
        if not valor:
            mostrar_mensaje("Por favor, selecciona una opción para continuar.", ft.Colors.ORANGE) 
            return
            
        respuesta = {'clave': clave, 'valor': valor}
        resultado = state["coordinador"].procesar(respuesta)
        procesar_resultado(resultado)

    # Pantallas

    # 1. Pantalla de Vehículo
    input_marca = ft.TextField(label="Marca", width=300, border_color=COLOR_ACCENT, focused_border_color=COLOR_HEADER)
    input_modelo = ft.TextField(label="Modelo", width=300, border_color=COLOR_ACCENT, focused_border_color=COLOR_HEADER)
    input_anio = ft.TextField(label="Año", width=300, border_color=COLOR_ACCENT, focused_border_color=COLOR_HEADER)

    def mostrar_pantalla_vehiculo():
        actualizar_progreso(0.1)
        
        input_marca.value = ""
        input_modelo.value = ""
        input_anio.value = ""

        content = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.DIRECTIONS_CAR_FILLED, size=60, color=COLOR_ACCENT),
                ft.Text("Nuevo Diagnóstico", size=24, weight=ft.FontWeight.BOLD, color=COLOR_HEADER),
                ft.Text("Ingresa los datos del auto para configurar el experto", size=14, color=COLOR_TEXT_SUBTLE),
                ft.Divider(height=20, color="transparent"),
                input_marca,
                input_modelo,
                input_anio,
                ft.Divider(height=20, color="transparent"),
                ft.ElevatedButton(
                    "Iniciar Análisis", 
                    icon=ft.Icons.PLAY_ARROW,
                    on_click=iniciar_diagnostico,
                    style=ft.ButtonStyle(
                        bgcolor=COLOR_ACCENT, 
                        color="white", 
                        padding=20,
                        shape=ft.RoundedRectangleBorder(radius=8)
                    ),
                    width=300
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            bgcolor=COLOR_BG_CARD,
            padding=40,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=15, color=SHADOW_COLOR),
            width=500
        )
        content_container.content = content
        page.update()

    # 2. Pantalla de Preguntas
    def mostrar_pantalla_pregunta(pregunta):
        actualizar_progreso(0.5)
        state["pregunta_actual"] = pregunta
        
        opciones_container = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, height=300)
        es_multiselect = (pregunta['clave'] == 'sintoma_general')
        controles_opciones = []

        def fmt(txt): return txt.replace('_', ' ').capitalize()

        if es_multiselect:
            for opcion in pregunta['opciones']:

                cb = ft.Checkbox(label=fmt(opcion), value=False, active_color=COLOR_ACCENT, check_color=ft.Colors.WHITE)
                cb.data = opcion
                controles_opciones.append(cb)
                
                card = ft.Container(
                    content=cb,
                    bgcolor=COLOR_BG_MAIN, 
                    padding=10,
                    border_radius=5,
                    border=ft.border.all(1, ft.Colors.BLUE_GREY_200)
                )
                opciones_container.controls.append(card)
        else:
            radio_group = ft.RadioGroup(content=ft.Column())
            for opcion in pregunta['opciones']:
                rb = ft.Radio(value=opcion, label=fmt(opcion), active_color=COLOR_ACCENT)
                
                card = ft.Container(
                    content=rb,
                    bgcolor=COLOR_BG_MAIN,
                    padding=10,
                    border_radius=5
                )
                radio_group.content.controls.append(card)
            
            controles_opciones.append(radio_group)
            opciones_container.controls.append(radio_group)

        def on_confirmar(e):
            clave = pregunta['clave']
            valor = ""
            if es_multiselect:
                seleccionados = [c.data for c in controles_opciones if c.value]
                valor = ",".join(seleccionados)
            else:
                valor = controles_opciones[0].value

            enviar_respuesta(clave, valor)

        content = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.QUESTION_ANSWER, size=40, color=COLOR_ACCENT),
                    ft.Container(
                        content=ft.Text(pregunta['texto'], size=20, weight=ft.FontWeight.BOLD, color=COLOR_HEADER),
                        expand=True, padding=ft.padding.only(left=10)
                    )
                ], alignment=ft.MainAxisAlignment.START),
                ft.Divider(color=ft.Colors.BLUE_GREY_100),
                opciones_container,
                ft.Divider(height=20, color="transparent"),
                ft.ElevatedButton(
                    "Confirmar Respuesta",
                    icon=ft.Icons.CHECK,
                    on_click=on_confirmar,
                    style=ft.ButtonStyle(bgcolor=COLOR_CONFIRM, color="white", padding=20),
                    width=None,
                    expand=True
                )
            ]),
            bgcolor=COLOR_BG_CARD,
            padding=40,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=15, color=SHADOW_COLOR),
            width=600,
            height=600
        )
        content_container.content = content
        page.update()

    # 3. Pantalla de Resultados
    def mostrar_pantalla_diagnostico(diagnosticos):
        actualizar_progreso(1.0)
        
        lista_resultados = ft.ListView(expand=True, spacing=10, padding=10)

        if not diagnosticos:
            lista_resultados.controls.append(ft.Text("No se encontraron fallas críticas.", size=18, color=COLOR_HEADER))
        else:
            for i, diag in enumerate(diagnosticos, 1):
                sistema = diag.get('sistema', 'General')
                sev = diag.get('severidad', 'Baja')
                
                color_sev = ft.Colors.GREEN_700
                bg_sev = ft.Colors.GREEN_50
                if sev.lower() == 'media': color_sev, bg_sev = ft.Colors.ORANGE_800, ft.Colors.ORANGE_50
                if sev.lower() == 'alta': color_sev, bg_sev = ft.Colors.DEEP_ORANGE_800, ft.Colors.DEEP_ORANGE_50
                if sev.lower() == 'critica': color_sev, bg_sev = ft.Colors.RED_800, ft.Colors.RED_50

                card = ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(f"{i}. Sistema: {sistema}", size=16, weight=ft.FontWeight.BOLD, color=COLOR_HEADER),
                            ft.Container(
                                content=ft.Text(sev.upper(), color=color_sev, size=12, weight=ft.FontWeight.BOLD),
                                bgcolor=bg_sev, padding=5, border_radius=5
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Divider(color=ft.Colors.BLUE_GREY_50),
                        ft.Text("CAUSA PROBABLE:", size=12, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_SUBTLE),
                        ft.Text(diag.get('causa'), size=14, color=ft.Colors.BLACK87),
                        ft.Divider(height=5, color="transparent"),
                        ft.Text("SOLUCIÓN RECOMENDADA:", size=12, weight=ft.FontWeight.BOLD, color=COLOR_TEXT_SUBTLE),
                        ft.Text(diag.get('solucion'), size=14, color=ft.Colors.BLACK87),
                    ]),
                    bgcolor=COLOR_BG_CARD,
                    padding=20,
                    border_radius=8,
                    border=ft.border.all(1, ft.Colors.BLUE_GREY_100)
                )
                lista_resultados.controls.append(card)

        content = ft.Container(
            content=ft.Column([
                 ft.Row([
                    ft.Icon(ft.Icons.ASSESSMENT, size=32, color=COLOR_HEADER),
                    ft.Text("Informe de Diagnóstico", size=24, weight=ft.FontWeight.BOLD, color=COLOR_HEADER),
                ], spacing=10),
                ft.Divider(color=ft.Colors.BLUE_GREY_200),
                ft.Container(content=lista_resultados, expand=True, bgcolor=COLOR_BG_MAIN, border_radius=8),
                ft.Divider(height=20, color="transparent"),
                ft.ElevatedButton(
                    "Nuevo Diagnóstico",
                    icon=ft.Icons.REFRESH,
                    on_click=reiniciar,
                    style=ft.ButtonStyle(bgcolor=COLOR_ACCENT, color="white", padding=20),
                    width=None
                )
            ]),
            bgcolor=COLOR_BG_CARD,
            padding=30,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=15, color=SHADOW_COLOR),
            width=700,
            height=650
        )
        content_container.content = content
        page.update()

    # Layout Principal
    
    # Header 
    header = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.BUILD_CIRCLE, size=36, color="white"),
            ft.Column([
                ft.Text("ASISTENTE MECÁNICO", size=18, weight=ft.FontWeight.BOLD, color="white"),
                ft.Text("Sistema Inteligente de Diagnóstico", size=12, color=COLOR_BG_INTERNAL)
            ], spacing=2)
        ], alignment=ft.MainAxisAlignment.START, spacing=15),
        bgcolor=COLOR_HEADER,
        padding=ft.padding.symmetric(horizontal=20, vertical=15),
        width=float('inf'),
        shadow=ft.BoxShadow(blur_radius=5, color=SHADOW_COLOR, offset=ft.Offset(0,2))
    )

    page.add(
        ft.Column([
            header,
            progress_bar,
            content_container
        ], expand=True, spacing=0)
    )

    mostrar_pantalla_vehiculo()

if __name__ == "__main__":
    ft.app(target=main)