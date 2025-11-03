import tkinter as tk
from tkinter import ttk, messagebox
from core.router import RouterDiagnosticos
from sistemas.motor import SistemaMotor
from sistemas.transmision import SistemaTransmision
from hechos import Vehiculo, Estado, Sistema 

class Coordinador:
    def __init__(self, vehiculo):
        self.vehiculo = vehiculo
        self.router = RouterDiagnosticos()
        self.sistemas_especialistas = {
            'motor': SistemaMotor(),
            'transmision': SistemaTransmision()
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
        
    
        for sintoma in origen.obtener_sintomas_ingresados():
            destino.declare(Estado(clave=sintoma, valor=True)) 
        print(f"Hechos transferidos a {destino.__class__.__name__}")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Asistente de Diagnóstico Automotriz")
        self.geometry("600x650")
        
        # Estilo
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure("TButton", padding=6, relief="flat", background="#007bff", foreground="white")
        style.map("TButton", background=[('active', '#0056b3')])
        style.configure("TLabel", padding=5, font=('Helvetica', 10))
        style.configure("Header.TLabel", font=('Helvetica', 16, 'bold'))

        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.frames = {}
        for F in (FrameVehiculo, FramePregunta, FrameDiagnostico):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.coordinador = None
        self.pregunta_actual = None
        
        self.mostrar_frame(FrameVehiculo)

    def mostrar_frame(self, frame_clase):
        """Muestra el frame (pantalla) solicitado"""
        frame = self.frames[frame_clase]
        frame.tkraise()

    def iniciar_diagnostico(self, vehiculo_data):
        """Se llama desde FrameVehiculo"""
        vehiculo = Vehiculo(
            marca=vehiculo_data['marca'] or "Desconocido",
            modelo=vehiculo_data['modelo'] or "Desconocido",
            anio=vehiculo_data['anio'] or "2000"
        )
        self.coordinador = Coordinador(vehiculo)
        
        resultado = self.coordinador.procesar()
        self.procesar_resultado(resultado)

    def enviar_respuesta(self, clave, valor):
        """Se llama desde FramePregunta"""
        if not valor:
             messagebox.showwarning("Opción Requerida", "Por favor, selecciona al menos una opción.")
             return
             
        respuesta = {'clave': clave, 'valor': valor}
        resultado = self.coordinador.procesar(respuesta)
        self.procesar_resultado(resultado)

    def procesar_resultado(self, resultado):
        """Decide qué pantalla mostrar basado en el resultado del motor"""
        if 'pregunta' in resultado:
            self.frames[FramePregunta].actualizar_pregunta(resultado['pregunta'])
            self.mostrar_frame(FramePregunta)
        elif 'diagnosticos' in resultado:
            self.frames[FrameDiagnostico].mostrar_diagnosticos(resultado['diagnosticos'])
            self.mostrar_frame(FrameDiagnostico)
        else:
            messagebox.showerror("Error", "Ocurrió un error inesperado en el motor.")

    def reiniciar(self):
        """Reinicia la aplicación a la pantalla inicial"""
        self.coordinador = None
        self.pregunta_actual = None
        self.frames[FrameVehiculo].limpiar_campos()
        self.mostrar_frame(FrameVehiculo)

class FrameVehiculo(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        ttk.Label(self, text="Bienvenido al Asistente", style="Header.TLabel").pack(pady=10)
        ttk.Label(self, text="Para comenzar, ingrese los datos de su vehículo:").pack(pady=5)
        
        form_frame = ttk.Frame(self)
        form_frame.pack(pady=10, fill='x', padx=20)
        
        ttk.Label(form_frame, text="Marca:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.marca_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.marca_var).grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        
        ttk.Label(form_frame, text="Modelo:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.modelo_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.modelo_var).grid(row=1, column=1, sticky='ew', padx=5, pady=5)
        
        ttk.Label(form_frame, text="Año:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.anio_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.anio_var).grid(row=2, column=1, sticky='ew', padx=5, pady=5)
        
        form_frame.columnconfigure(1, weight=1)
        
        ttk.Button(self, text="Comenzar Diagnóstico", command=self.iniciar).pack(pady=20, ipadx=10, ipady=5)

    def iniciar(self):
        datos = {
            'marca': self.marca_var.get(),
            'modelo': self.modelo_var.get(),
            'anio': self.anio_var.get()
        }
        self.controller.iniciar_diagnostico(datos)
        
    def limpiar_campos(self):
        self.marca_var.set("")
        self.modelo_var.set("")
        self.anio_var.set("")


class FramePregunta(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.pregunta_actual = None
        self.opciones_vars = []
        
        self.label_pregunta = ttk.Label(self, text="Pregunta...", style="Header.TLabel", wraplength=450)
        self.label_pregunta.pack(pady=20)
        
        self.opciones_frame = ttk.Frame(self)
        self.opciones_frame.pack(pady=10, fill='x', padx=30)
        
        self.boton_siguiente = ttk.Button(self, text="Siguiente", command=self.responder)
        self.boton_siguiente.pack(pady=20, ipadx=10, ipady=5)

    def actualizar_pregunta(self, pregunta):
        self.pregunta_actual = pregunta
        self.label_pregunta.config(text=pregunta['texto'])
        
        for widget in self.opciones_frame.winfo_children():
            widget.destroy()
        
        self.opciones_vars = []
        
        es_multiselect = (pregunta['clave'] == 'sintoma_general')
        
        if es_multiselect:
            for opcion in pregunta['opciones']:
                var = tk.StringVar(value="")
                cb = ttk.Checkbutton(self.opciones_frame, text=opcion.replace('_', ' '),
                                     variable=var, onvalue=opcion, offvalue="")
                cb.pack(anchor='w', pady=3)
                self.opciones_vars.append(var)
        else:
            self.respuesta_var = tk.StringVar(value="")
            for opcion in pregunta['opciones']:
                rb = ttk.Radiobutton(self.opciones_frame, text=opcion.replace('_', ' '),
                                     variable=self.respuesta_var, value=opcion)
                rb.pack(anchor='w', pady=3)
            self.opciones_vars = [self.respuesta_var] 

    def responder(self):
        clave = self.pregunta_actual['clave']
        valor = ""
        
        es_multiselect = (self.pregunta_actual['clave'] == 'sintoma_general')
        
        if es_multiselect:
            seleccionados = [var.get() for var in self.opciones_vars if var.get()]
            valor = ",".join(seleccionados)
        else:
            valor = self.opciones_vars[0].get() 
            
        self.controller.enviar_respuesta(clave, valor)


class FrameDiagnostico(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        ttk.Label(self, text="Diagnóstico Final", style="Header.TLabel").pack(pady=10)
        
        self.text_resultados = tk.Text(self, height=20, width=60, wrap='word',
                                       borderwidth=0, highlightthickness=0)
        self.text_resultados.pack(pady=10, padx=20, fill="both", expand=True)

        self.text_resultados.tag_configure("sistema", font=('Helvetica', 12, 'bold'), foreground="#007bff")
        self.text_resultados.tag_configure("causa", font=('Helvetica', 10, 'bold'))
        self.text_resultados.tag_configure("normal", font=('Helvetica', 10))
        self.text_resultados.tag_configure("severidad", font=('Helvetica', 9, 'italic'), foreground="#dc3545")
        
        self.text_resultados.config(state='disabled') 
        
        ttk.Button(self, text="Realizar Otro Diagnóstico", command=lambda: controller.reiniciar()).pack(pady=20)

    def mostrar_diagnosticos(self, diagnosticos):
        self.text_resultados.config(state='normal') 
        self.text_resultados.delete('1.0', tk.END) 
        
        if not diagnosticos:
            self.text_resultados.insert(tk.END, "No se encontraron diagnósticos para los síntomas proporcionados.", "normal")
            self.text_resultados.config(state='disabled')
            return

        for diag in diagnosticos:
            sistema = diag.get('sistema', 'General')
            causa = diag.get('causa', 'N/A')
            solucion = diag.get('solucion', 'N/A')
            severidad = diag.get('severidad', 'N/A')

            self.text_resultados.insert(tk.END, f"SISTEMA: {sistema}\n", "sistema")
            self.text_resultados.insert(tk.END, f"  Gravedad: {severidad}\n", "severidad")
            self.text_resultados.insert(tk.END, f"  Causa: ", "causa")
            self.text_resultados.insert(tk.END, f"{causa}\n", "normal")
            self.text_resultados.insert(tk.END, f"  Solución: ", "causa")
            self.text_resultados.insert(tk.END, f"{solucion}\n\n", "normal")
            
        self.text_resultados.config(state='disabled') 


if __name__ == "__main__":
    app = App()
    app.mainloop()

