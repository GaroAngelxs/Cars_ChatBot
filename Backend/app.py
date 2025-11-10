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


from hechos import Vehiculo, Estado, Sistema 

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
            'combustible_4': SistemaCombustible4()
        }
        self.sistemas_activados = []
        self.diagnosticos_finales = []
        
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

        # --- Fase 2: Ejecutar SISTEMAS ESPECIALISTAS ---
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
                    diag['sistema'] = sistema_nombre.capitalize()
            
            print(f"Diagnósticos de '{sistema_nombre}': {diags}")
            self.diagnosticos_finales.extend(diags)
            
            self.sistemas_activados.pop(0)
            respuesta = None 

        return {'diagnosticos': self.diagnosticos_finales or [{'causa': 'No se encontraron diagnósticos.', 'solucion': 'Los sistemas no reportaron fallas.', 'severidad': 'Baja'}]}

    def _transferir_hechos(self, origen, destino, sistema_nombre):
        """Transfiere hechos relevantes del router al especialista"""
        destino.declare(self.vehiculo)
        destino.declare(Sistema(area=sistema_nombre))
        
        # Transferir TODOS los hechos Estado del router
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
        self.geometry("800x700")
        self.configure(bg='#f8f9fa')
        
        # Configurar estilo moderno
        self._configurar_estilos()
        
        # Frame principal con gradiente
        self.main_container = tk.Frame(self, bg='#f8f9fa')
        self.main_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Header con gradiente
        self.header = tk.Frame(self.main_container, bg='#2c3e50', height=80)
        self.header.pack(fill="x", padx=0, pady=0)
        self.header.pack_propagate(False)
        
        ttk.Label(self.header, text="🔧 Asistente Mecánico Inteligente", 
                 style="Header.TLabel", background='#2c3e50').pack(expand=True)
        ttk.Label(self.header, text="Sistema Experto de Diagnóstico Automotriz", 
                 style="Subheader.TLabel", background='#2c3e50').pack(expand=True)
        
        # Container para los frames
        self.container = ttk.Frame(self.main_container, style="Card.TFrame")
        self.container.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.frames = {}
        for F in (FrameVehiculo, FramePregunta, FrameDiagnostico):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.coordinador = None
        self.pregunta_actual = None
        
        self.mostrar_frame(FrameVehiculo)

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
        
        # Entradas modernas
        style.configure("Modern.TEntry", font=('Segoe UI', 11), 
                       padding=(10, 8), borderwidth=1, relief='flat',
                       fieldbackground='#f8f9fa')
        
        # Checkbuttons y Radiobuttons modernos
        style.configure("Modern.TCheckbutton", font=('Segoe UI', 10), 
                       background='white', foreground='#2c3e50')
        style.configure("Modern.TRadiobutton", font=('Segoe UI', 10),
                       background='white', foreground='#2c3e50')

    def mostrar_frame(self, frame_clase):
        frame = self.frames[frame_clase]
        frame.tkraise()

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
        self._crear_interfaz()

    def _crear_interfaz(self):
        # Título
        ttk.Label(self, text="🚗 Datos del Vehículo", style="Title.TLabel").pack(pady=30)
        
        ttk.Label(self, text="Complete la información de su vehículo para comenzar el diagnóstico:", 
                 style="Normal.TLabel").pack(pady=10)
        
        # Formulario en contenedor con sombra
        form_container = ttk.Frame(self, style="Card.TFrame")
        form_container.pack(pady=20, padx=40, fill='x')
        
        # Campos del formulario
        campos = [
            ("🏷️ Marca:", "marca_var"),
            ("🚀 Modelo:", "modelo_var"), 
            ("📅 Año:", "anio_var")
        ]
        
        for i, (texto, var_name) in enumerate(campos):
            row_frame = ttk.Frame(form_container, style="Card.TFrame")
            row_frame.pack(fill='x', pady=12)
            
            ttk.Label(row_frame, text=texto, style="Normal.TLabel", 
                     width=12, anchor='e').pack(side='left', padx=(0, 10))
            
            var = tk.StringVar()
            setattr(self, var_name, var)
            
            entry = ttk.Entry(row_frame, textvariable=var, style="Modern.TEntry", 
                             font=('Segoe UI', 11))
            entry.pack(side='left', fill='x', expand=True, ipady=8)
        
        # Botón de inicio
        btn_frame = ttk.Frame(self, style="Card.TFrame")
        btn_frame.pack(pady=30)
        
        ttk.Button(btn_frame, text="🎯 Comenzar Diagnóstico", 
                  command=self.iniciar, style="Primary.TButton").pack(pady=10)

    def iniciar(self):
        datos = {
            'marca': self.marca_var.get(),
            'modelo': self.modelo_var.get(),
            'anio': self.anio_var.get()
        }
        #Lo comente para estar haciendo pruebas y no tener que estar poniendo los datos a cada rato jksjsk
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
        # Icono de pregunta
        self.icono_label = ttk.Label(self, text="❓", font=('Segoe UI', 24),
                                background='white')
        self.icono_label.pack(pady=20)
        
        # Pregunta
        self.label_pregunta = ttk.Label(self, text="Pregunta...", 
                                    style="Title.TLabel", wraplength=600,
                                    justify='center')
        self.label_pregunta.pack(pady=10, padx=30)
        
        # Contenedor de opciones con scroll
        opciones_container = ttk.Frame(self, style="Card.TFrame")
        opciones_container.pack(pady=20, padx=40, fill='both', expand=True)
        
        # Canvas y scrollbar para opciones largas
        self.canvas = tk.Canvas(opciones_container, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(opciones_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style="Card.TFrame")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botón siguiente
        self.boton_siguiente = ttk.Button(self, text="➡️ Siguiente", 
                                        command=self.responder, style="Success.TButton")
        self.boton_siguiente.pack(pady=20, ipadx=20, ipady=10)

    def actualizar_pregunta(self, pregunta):
        self.pregunta_actual = pregunta
        self.label_pregunta.config(text=pregunta['texto'])
        
        # Limpiar opciones anteriores
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.opciones_vars = []
        
        es_multiselect = (pregunta['clave'] == 'sintoma_general')
        
        if es_multiselect:
            for opcion in pregunta['opciones']:
                var = tk.StringVar(value="")
                cb = ttk.Checkbutton(self.scrollable_frame, 
                                text=opcion.replace('_', ' '),
                                variable=var, 
                                onvalue=opcion, 
                                offvalue="",
                                style="Modern.TCheckbutton")
                cb.pack(anchor='w', pady=8, padx=10)  # Más espacio: pady=8
                self.opciones_vars.append(var)
        else:
            self.respuesta_var = tk.StringVar(value="")
            for opcion in pregunta['opciones']:
                rb = ttk.Radiobutton(self.scrollable_frame, 
                                text=opcion.replace('_', ' '),
                                variable=self.respuesta_var, 
                                value=opcion,
                                style="Modern.TRadiobutton")
                rb.pack(anchor='w', pady=10, padx=15)  # Más espacio: pady=10, padx=15
            self.opciones_vars = [self.respuesta_var]

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
        
        # Text area con mejor estilo
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