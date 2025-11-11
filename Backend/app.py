import tkinter as tk
from tkinter import ttk, messagebox
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
from hechos import Vehiculo, Estado, Sistema 

class Coordinador:
    def __init__(self, vehiculo):
        self.vehiculo = vehiculo
        self.router = RouterDiagnosticos()
        
        # Se generan todos los sistemas con sus clases
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
            'direccion_1': SistemaDireccion1(),
        }

        # Para almacenar los sistemas activados y diagnosticos
        self.sistemas_activados = []
        self.diagnosticos_finales = []
        
        # Se resetea el router y se declara el vehículo
        self.router.reset()
        self.router.declare(self.vehiculo)

    def procesar(self, respuesta=None):
        """Procesa la siguiente etapa del diagnóstico"""
        
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
            
            print(f"Sistemas activados por el router: {self.sistemas_activados}")
            respuesta = None

        # Ejecuta los sistemas activados
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

            # Comienza las preguntas del sistema actual
            sistema.run()

            # Obtiene la siguiente pregunta
            pregunta = sistema.obtener_pregunta_actual()
            if pregunta:
                sistema.limpiar_pregunta_actual()
                return {'pregunta': pregunta}
            
            # Obtiene los diagnósticos
            diags = sistema.obtener_diagnosticos()
            for diag in diags:
                if 'sistema' not in diag:
                    diag['sistema'] = sistema_nombre.capitalize()
            
            print(f"Diagnósticos de '{sistema_nombre}': {diags}")
            self.diagnosticos_finales.extend(diags)
            
            # Popea el sistema activado
            self.sistemas_activados.pop(0)
            respuesta = None 

        return {'diagnosticos': self.diagnosticos_finales or [{'causa': 'No se encontraron diagnósticos.', 'solucion': 'Los sistemas no reportaron fallas.', 'severidad': 'Baja'}]}

    def _transferir_hechos(self, origen, destino, sistema_nombre):
        """Transfiere hechos relevantes del router al especialista"""
        destino.declare(self.vehiculo)
        destino.declare(Sistema(area=sistema_nombre))
        
        # Transferir todos los hechos Estado del router
        estados_transferidos = 0
        for hecho in origen.facts.values():
            if isinstance(hecho, Estado):
                hecho_dict = {k: v for k, v in hecho.items()}
                destino.declare(Estado(**hecho_dict))
                estados_transferidos += 1
                print(f"  → Transferido: Estado({hecho_dict})")
        
        print(f"Hechos transferidos a {destino.__class__.__name__}: {estados_transferidos} estados")


class ModernApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🔧 Asistente Mecánico Inteligente")
        
        # Configurar pantalla completa
        self.state('zoomed')
        self.configure(bg='#f8f9fa')
        
        # Configurar estilo moderno
        self._configurar_estilos()

        # Configurar el header
        header_frame = tk.Frame(self, bg='#2c3e50', height=80)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Configurar los labels del header
        ttk.Label(header_frame, text="🔧 Asistente Mecánico Inteligente", 
                 style="Header.TLabel", background='#2c3e50').pack(expand=True)
        ttk.Label(header_frame, text="Sistema Experto de Diagnóstico Automotriz", 
                 style="Subheader.TLabel", background='#2c3e50').pack(expand=True)
        
        # Container para los frames
        self.main_frame_container = tk.Frame(self, bg='#f8f9fa')
        self.main_frame_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Posicionamiento de frames
        self.frames = {}
        for F in (FrameVehiculo, FramePregunta, FrameDiagnostico):
            frame = F(self.main_frame_container, self)
            self.frames[F] = frame
            # Posicionar en grid todos en la misma celda
            frame.grid(row=0, column=0, sticky="nsew")

        # configuracion de columnas y filas
        self.main_frame_container.grid_rowconfigure(0, weight=1)
        self.main_frame_container.grid_columnconfigure(0, weight=1)

        self.coordinador = None
        self.pregunta_actual = None
        
        # Muestra el frame
        self.mostrar_frame(FrameVehiculo)
        
        # Atajos de teclado
        self.bind('<F11>', lambda e: self.toggle_fullscreen())
        self.bind('<Escape>', lambda e: self.attributes('-fullscreen', False))

    def toggle_fullscreen(self):
        self.attributes('-fullscreen', not self.attributes('-fullscreen'))

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores modernos
        colores = {
            'primary': '#3498db',
            'success': '#2ecc71',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'dark': '#2c3e50',
            'light': '#ecf0f1'
        }
        
        # Configurar estilos
        style.configure("Card.TFrame", background='white', relief='raised', borderwidth=1)
        style.configure("Header.TLabel", font=('Segoe UI', 24, 'bold'), foreground='white')
        style.configure("Subheader.TLabel", font=('Segoe UI', 12), foreground='#bdc3c7')
        style.configure("Title.TLabel", font=('Segoe UI', 18, 'bold'), foreground='#2c3e50')
        style.configure("Normal.TLabel", font=('Segoe UI', 11), foreground='#34495e')
        
        # Botones modernos
        style.configure("Primary.TButton", font=('Segoe UI', 11, 'bold'), 
                    padding=(20, 10), background=colores['primary'], 
                    foreground='white', borderwidth=0, focuscolor='none')
        style.map("Primary.TButton",
                background=[('active', '#2980b9'), ('pressed', '#21618c')])
        
        style.configure("Success.TButton", font=('Segoe UI', 11, 'bold'),
                    padding=(20, 10), background=colores['success'],
                    foreground='white', borderwidth=0)
        style.map("Success.TButton",
                background=[('active', '#27ae60'), ('pressed', '#219653')])
        
        style.configure("Small.TButton", font=('Segoe UI', 10),
                    padding=(5, 2), background=colores['dark'],
                    foreground='white')
        style.map("Small.TButton",
                background=[('active', '#34495e')])
        
        # Entradas modernas
        style.configure("Modern.TEntry", font=('Segoe UI', 11), 
                    padding=(10, 8), borderwidth=1, relief='flat',
                    fieldbackground='#f8f9fa')
        
        # Checkbuttons y Radiobuttons modernos
        style.configure("Modern.TCheckbutton", 
                    font=('Segoe UI', 11),  
                    background='white', 
                    foreground='#2c3e50',
                    padding=(8, 8))
        
        style.configure("Modern.TRadiobutton",
                    font=('Segoe UI', 11),
                    background='white',
                    foreground='#2c3e50',
                    padding=(8, 8))

    def mostrar_frame(self, frame_clase):
        
        for frame in self.frames.values():
            frame.grid_remove()
        
        frame = self.frames[frame_clase]
        frame.grid()

    def iniciar_diagnostico(self, vehiculo_data):
        vehiculo = Vehiculo(
            marca=vehiculo_data['marca'] or "Desconocido",
            modelo=vehiculo_data['modelo'] or "Desconocido",
            anio=vehiculo_data['anio'] or "2000"
        )
        self.coordinador = Coordinador(vehiculo)
        resultado = self.coordinador.procesar()
        self.procesar_resultado(resultado)

    def enviar_respuesta(self, clave, valor):
        if not valor:
            messagebox.showwarning("Opción Requerida", "Por favor, selecciona al menos una opción.")
            return
        respuesta = {'clave': clave, 'valor': valor}
        resultado = self.coordinador.procesar(respuesta)
        self.procesar_resultado(resultado)

    def procesar_resultado(self, resultado):
        if 'pregunta' in resultado:
            self.frames[FramePregunta].actualizar_pregunta(resultado['pregunta'])
            self.mostrar_frame(FramePregunta)
        elif 'diagnosticos' in resultado:
            self.frames[FrameDiagnostico].mostrar_diagnosticos(resultado['diagnosticos'])
            self.mostrar_frame(FrameDiagnostico)
        else:
            messagebox.showerror("Error", "Ocurrió un error inesperado en el motor.")

    def reiniciar(self):
        self.coordinador = None
        self.pregunta_actual = None
        self.frames[FrameVehiculo].limpiar_campos()
        self.mostrar_frame(FrameVehiculo)


class FrameVehiculo(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Card.TFrame")
        self.controller = controller
        
        # Configurar expansión
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self._crear_interfaz()

    def _crear_interfaz(self):
        # Contenedor principal que se expande
        main_content = ttk.Frame(self, style="Card.TFrame")
        main_content.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_content.grid_rowconfigure(2, weight=1)
        main_content.grid_columnconfigure(0, weight=1)
        
        # Título
        ttk.Label(main_content, text="🚗 Datos del Vehículo", style="Title.TLabel").grid(row=0, column=0, pady=30)
        
        ttk.Label(main_content, text="Complete la información de su vehículo para comenzar el diagnóstico:", 
                 style="Normal.TLabel").grid(row=1, column=0, pady=10)
        
        # Formulario
        form_container = ttk.Frame(main_content, style="Card.TFrame")
        form_container.grid(row=2, column=0, sticky="nsew", pady=20, padx=40)
        form_container.grid_rowconfigure(3, weight=1)
        form_container.grid_columnconfigure(0, weight=1)
        
        # Campos del formulario
        campos = [
            ("🏷️ Marca:", "marca_var"),
            ("🚀 Modelo:", "modelo_var"), 
            ("📅 Año:", "anio_var")
        ]
        
        for i, (texto, var_name) in enumerate(campos):
            row_frame = ttk.Frame(form_container, style="Card.TFrame")
            row_frame.grid(row=i, column=0, sticky='ew', pady=12)
            row_frame.grid_columnconfigure(1, weight=1)
            
            ttk.Label(row_frame, text=texto, style="Normal.TLabel", 
                     width=12, anchor='e').grid(row=0, column=0, padx=(0, 10))
            
            var = tk.StringVar()
            setattr(self, var_name, var)
            
            entry = ttk.Entry(row_frame, textvariable=var, style="Modern.TEntry", 
                             font=('Segoe UI', 11))
            entry.grid(row=0, column=1, sticky='ew', ipady=8)
        
        # Botón de inicio
        btn_container = ttk.Frame(form_container, style="Card.TFrame")
        btn_container.grid(row=4, column=0, sticky='s', pady=30)
        
        ttk.Button(btn_container, text="🎯 Comenzar Diagnóstico", 
                  command=self.iniciar, style="Primary.TButton").pack(pady=10)
        
    def iniciar(self):
        datos = {
            'marca': self.marca_var.get(),
            'modelo': self.modelo_var.get(),
            'anio': self.anio_var.get()
        }
        # Lo comente para estar haciendo pruebas y no tener que estar poniendo los datos a cada rato jksjsk
        #if not all(datos.values()):
            #messagebox.showwarning("Datos Incompletos", "Por favor, complete todos los campos.")
            #return
        self.controller.iniciar_diagnostico(datos)
            
    def limpiar_campos(self):
        self.marca_var.set("")
        self.modelo_var.set("")
        self.anio_var.set("")


class FramePregunta(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Card.TFrame")
        self.controller = controller
        self.pregunta_actual = None
        self.opciones_vars = []
        self._crear_interfaz()

    def _crear_interfaz(self):
        # Configurar expansión del frame principal
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Contenedor principal
        main_content = ttk.Frame(self, style="Card.TFrame")
        main_content.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_content.grid_rowconfigure(2, weight=1)
        main_content.grid_columnconfigure(0, weight=1)
        
        # Icono de pregunta
        self.icono_label = ttk.Label(main_content, text="❓", font=('Segoe UI', 24),
                                background='white')
        self.icono_label.grid(row=0, column=0, pady=(10, 0))
        
        # Pregunta
        self.label_pregunta = ttk.Label(main_content, text="Pregunta...", 
                                    style="Title.TLabel", wraplength=700,
                                    justify='center')
        self.label_pregunta.grid(row=1, column=0, pady=15, padx=30)
        
        self.opciones_container = ttk.Frame(main_content, style="Card.TFrame")
        self.opciones_container.grid(row=2, column=0, sticky="nsew", pady=20, padx=20)
        
        # Crear un Frame con Scrollbar
        self._crear_scrollable_area()
        
        # Botón siguiente
        btn_container = ttk.Frame(main_content, style="Card.TFrame")
        btn_container.grid(row=3, column=0, pady=20)
        
        self.boton_siguiente = ttk.Button(btn_container, text="➡️ Siguiente", 
                                        command=self.responder, style="Success.TButton")
        self.boton_siguiente.pack(ipadx=20, ipady=10)

    def _crear_scrollable_area(self):
        """Crea un área scrollable sin espacio en blanco"""
        # Frame principal para el área scrollable
        scroll_frame = ttk.Frame(self.opciones_container, style="Card.TFrame")
        scroll_frame.pack(fill="both", expand=True)
        
        # Crear Scrollbar
        scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        
        # Crear Canvas
        self.canvas = tk.Canvas(
            scroll_frame, 
            bg='white', 
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Configurar scrollbar
        scrollbar.config(command=self.canvas.yview)
        
        # Crear frame interno para las opciones
        self.scrollable_frame = ttk.Frame(self.canvas, style="Card.TFrame")
        
        # Crear ventana en el canvas
        self.canvas_frame = self.canvas.create_window(
            (0, 0), 
            window=self.scrollable_frame, 
            anchor="nw",
            tags="scrollable_frame"
        )
        
        # Configurar eventos para ajuste automático del ancho
        def configurar_scroll_region(event):
            self.canvas.itemconfig("scrollable_frame", width=event.width)
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        def ajustar_ancho_frame(event):
            self.canvas.itemconfig("scrollable_frame", width=event.width)
        
        self.canvas.bind("<Configure>", ajustar_ancho_frame)
        self.scrollable_frame.bind("<Configure>", configurar_scroll_region)

    def actualizar_pregunta(self, pregunta):
        self.pregunta_actual = pregunta
        self.label_pregunta.config(text=pregunta['texto'])
        
        # Limpiar opciones anteriores
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.opciones_vars = []
        
        es_multiselect = (pregunta['clave'] == 'sintoma_general')
        
        # Configurar grid para 3 columnas
        for i in range(3):
            self.scrollable_frame.columnconfigure(i, weight=1)

        padding_x = 15
        padding_y = 8
        
        if es_multiselect:
            for idx, opcion in enumerate(pregunta['opciones']):
                var = tk.StringVar(value="")
                fila = idx // 3
                columna = idx % 3
                
                texto_formateado = self._formatear_texto_opcion(opcion)
                
                cb = ttk.Checkbutton(self.scrollable_frame, 
                                text=texto_formateado,
                                variable=var, 
                                onvalue=opcion, 
                                offvalue="",
                                style="Modern.TCheckbutton",
                                width=32)
                cb.grid(row=fila, column=columna, sticky='w', padx=padding_x, pady=padding_y)
                self.opciones_vars.append(var)
        else:
            self.respuesta_var = tk.StringVar(value="")
            for idx, opcion in enumerate(pregunta['opciones']):
                fila = idx // 3
                columna = idx % 3
                
                texto_formateado = self._formatear_texto_opcion(opcion)
                
                rb = ttk.Radiobutton(self.scrollable_frame, 
                                text=texto_formateado,
                                variable=self.respuesta_var, 
                                value=opcion,
                                style="Modern.TRadiobutton",
                                width=32)
                rb.grid(row=fila, column=columna, sticky='w', padx=padding_x, pady=padding_y)
            self.opciones_vars = [self.respuesta_var]
        
        # Forzar actualización del layout
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.yview_moveto(0)

    def _formatear_texto_opcion(self, texto):
        """Formatea el texto de las opciones para mejor legibilidad"""
        texto = texto.replace('_', ' ').title()
        
        palabras = texto.split()
        if len(palabras) > 4:
            puntos_division = [3, 4]
            for punto in puntos_division:
                if punto < len(palabras):
                    if punto + 1 < len(palabras) and len(palabras[punto]) > 2:
                        texto = ' '.join(palabras[:punto]) + '\n' + ' '.join(palabras[punto:])
                        break
        
        return texto

    def responder(self):
        clave = self.pregunta_actual['clave']
        valor = ""
        
        es_multiselect = (self.pregunta_actual['clave'] == 'sintoma_general')
        
        if es_multiselect:
            seleccionados = [var.get() for var in self.opciones_vars if var.get()]
            if not seleccionados:
                messagebox.showwarning("Selección Requerida", "Por favor, seleccione al menos un síntoma.")
                return
            valor = ",".join(seleccionados)
        else:
            valor = self.opciones_vars[0].get()
            if not valor:
                messagebox.showwarning("Selección Requerida", "Por favor, seleccione una opción.")
                return
            
        self.controller.enviar_respuesta(clave, valor)


class FrameDiagnostico(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Card.TFrame")
        self.controller = controller
        self._crear_interfaz()

    def _crear_interfaz(self):
        # Header de resultados
        ttk.Label(self, text="📊 Diagnóstico Final", style="Title.TLabel").pack(pady=20)
        
        # Contenedor de resultados con scroll
        result_container = ttk.Frame(self, style="Card.TFrame")
        result_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.text_resultados = tk.Text(result_container, height=20, width=70, wrap='word',
                                      font=('Segoe UI', 10), bg='#f8f9fa', 
                                      borderwidth=0, highlightthickness=0,
                                      padx=15, pady=15)
        
        scrollbar = ttk.Scrollbar(result_container, orient="vertical", command=self.text_resultados.yview)
        self.text_resultados.configure(yscrollcommand=scrollbar.set)
        
        self.text_resultados.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configurar tags para formato
        self.text_resultados.tag_configure("sistema", font=('Segoe UI', 14, 'bold'), 
                                         foreground="#2c3e50", spacing3=10)
        self.text_resultados.tag_configure("causa", font=('Segoe UI', 11, 'bold'),
                                         foreground="#34495e")
        self.text_resultados.tag_configure("normal", font=('Segoe UI', 10),
                                         foreground="#2c3e50")
        self.text_resultados.tag_configure("severidad_alta", font=('Segoe UI', 9, 'bold'),
                                         foreground="#e74c3c")
        self.text_resultados.tag_configure("severidad_media", font=('Segoe UI', 9, 'bold'),
                                         foreground="#f39c12")
        self.text_resultados.tag_configure("severidad_baja", font=('Segoe UI', 9, 'bold'),
                                         foreground="#27ae60")
        
        self.text_resultados.config(state='disabled')
        
        # Botones de acción
        btn_frame = ttk.Frame(self, style="Card.TFrame")
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="🔄 Realizar Otro Diagnóstico", 
                  command=lambda: self.controller.reiniciar(), style="Primary.TButton").pack(side='left', padx=10)

    def mostrar_diagnosticos(self, diagnosticos):
        self.text_resultados.config(state='normal')
        self.text_resultados.delete('1.0', tk.END)
        
        if not diagnosticos:
            self.text_resultados.insert(tk.END, "✅ No se encontraron diagnósticos para los síntomas proporcionados.\n\n", "normal")
            self.text_resultados.insert(tk.END, "El vehículo parece estar en buen estado o los síntomas no son críticos.", "normal")
            self.text_resultados.config(state='disabled')
            return

        for diag in diagnosticos:
            sistema = diag.get('sistema', 'General')
            causa = diag.get('causa', 'N/A')
            solucion = diag.get('solucion', 'N/A')
            severidad = diag.get('severidad', 'Media').lower()

            # Determinar tag de severidad
            severidad_tag = f"severidad_{severidad}"
            if severidad_tag not in ["severidad_alta", "severidad_media", "severidad_baja"]:
                severidad_tag = "severidad_media"

            self.text_resultados.insert(tk.END, f"🔧 {sistema}\n", "sistema")
            self.text_resultados.insert(tk.END, f"   Nivel de gravedad: ", "normal")
            self.text_resultados.insert(tk.END, f"{severidad.upper()}\n", severidad_tag)
            self.text_resultados.insert(tk.END, f"   🔍 Causa identificada:\n", "causa")
            self.text_resultados.insert(tk.END, f"   {causa}\n\n", "normal")
            self.text_resultados.insert(tk.END, f"   🛠️ Solución recomendada:\n", "causa")
            self.text_resultados.insert(tk.END, f"   {solucion}\n\n", "normal")
            self.text_resultados.insert(tk.END, "─" * 30 + "\n\n", "normal")
            
        self.text_resultados.config(state='disabled')


if __name__ == "__main__":
    app = ModernApp()
    app.mainloop()