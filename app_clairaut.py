"""
Visualizador Computacional de Ecuaciones Diferenciales de Clairaut
Curso de Ecuaciones Diferenciales - Modalidad CIPAS

Caracteristicas de diseno:
- Paleta OLED / Negro Profundo (#000000, #09090b, #121214, #18181b).
- Sin uso de emojis en toda la interfaz.
- Ayudas integradas con descripciones concisas para cada control, boton, panel y resultado matematico.
- Boton dedicado para consultar la Guia de Uso y Sintaxis Simbolica.
"""

import os
# Evitar advertencias de Matplotlib en directorios de configuracion restringidos
os.environ['MPLCONFIGDIR'] = '/tmp/matplotlib'

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import numpy as np
import sympy as sp
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Configuracion de apariencia CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class VentanaGuiaSimbologia(ctk.CTkToplevel):
    """Ventana modal de referencia rapida de sintaxis y manual de operacion."""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Manual de Uso y Sintaxis Matematica")
        self.geometry("720x620")
        self.configure(fg_color="#09090b")
        self.attributes("-topmost", True)
        
        lbl_titulo = ctk.CTkLabel(
            self, 
            text="Guia de Operacion y Notacion Simbolica", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        lbl_titulo.pack(padx=20, pady=(15, 10), anchor="w")
        
        caja_texto = ctk.CTkTextbox(
            self, 
            font=ctk.CTkFont(family="Courier", size=12),
            fg_color="#121214",
            text_color="#e4e4e7",
            border_width=1,
            border_color="#27272a"
        )
        caja_texto.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        guia_contenido = (
            "======================================================================\n"
            "   MANUAL DE USUARIO Y CONVENCION DE SINTAXIS SIMBOLICA\n"
            "======================================================================\n\n"
            "1. REGLAS DE ESCRITURA PARA f(p):\n"
            "   El motor analitico procesa expresiones utilizando la notacion\n"
            "   estandar de SymPy / Python:\n\n"
            "   - Suma y Resta:              +  y  -           (ej. p + 2)\n"
            "   - Multiplicacion:            *                 (ej. 3*p, obligatoria)\n"
            "   - Division:                  /                 (ej. 1/p)\n"
            "   - Potenciacion:              **                (ej. p**2, p**3)\n"
            "   - Raiz cuadrada:             sqrt(p)           (o p**(1/2))\n"
            "   - Funciones trigonometricas: sin(p), cos(p), tan(p)\n"
            "   - Exponencial natural:       exp(p)\n"
            "   - Logaritmo natural:         log(p)\n\n"
            "2. EJEMPLOS OFICIALES DE LA GUIA:\n"
            "   - Ejemplo obligatorio:       p**2\n"
            "   - Ejemplo cubico:            p**3\n"
            "   - Fraccion racional:         1/p\n"
            "   - Cuadratica desplazada:     p**2 + 1\n"
            "   - Expresion radical:         sqrt(p)\n\n"
            "3. DESCRIPCION DE LOS ELEMENTOS DE CONTROL:\n"
            "   - Selector de Ejemplos:      Carga preconfiguraciones recomendadas.\n"
            "   - Entrada f(p):              Campo de edicion de la funcion.\n"
            "   - Boton Calcular y Graficar: Ejecuta los 9 pasos del analisis analitico\n"
            "                                y actualiza el lienzo cartesiano.\n"
            "   - Checkbox Familia General:  Alterna la visibilidad de las rectas\n"
            "                                tangentes correspondientes a cada C.\n"
            "   - Checkbox Sol. Singular:    Alterna la curva envolvente continua.\n"
            "   - Checkbox Cuadricula:       Oculta o muestra ejes y lineas guia.\n"
            "   - Barra de Herramientas:     Permite zoom interactivo, paneo con raton\n"
            "                                y exportacion a formato PNG o PDF.\n\n"
            "4. INTERPRETACION TEORICA:\n"
            "   - Familia de rectas:         y = C*x + f(C) para C en {-3,-2,-1,0,1,2,3}\n"
            "   - Solucion singular:         Obtenida al anular x + f'(p) = 0.\n"
            "                                Actua geometricamente como la envolvente\n"
            "                                tangente a cada una de las rectas.\n"
            "======================================================================\n"
        )
        caja_texto.insert("1.0", guia_contenido)
        caja_texto.configure(state="disabled")
        
        btn_cerrar = ctk.CTkButton(
            self, 
            text="Entendido / Cerrar", 
            command=self.destroy,
            fg_color="#27272a",
            hover_color="#3f3f46",
            text_color="#ffffff",
            height=32
        )
        btn_cerrar.pack(padx=20, pady=(0, 15))


class ClairautVisualizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuracion general de ventana
        self.title("Visualizador Computacional de Ecuaciones Diferenciales de Clairaut")
        self.geometry("1300x840")
        self.minsize(1080, 720)
        self.configure(fg_color="#000000") # Negro profundo
        
        # Variables simbolicas de SymPy
        self.p, self.x, self.C = sp.symbols('p x C')
        
        # Variables de estado de visualizacion
        self.mostrar_familia = tk.BooleanVar(value=True)
        self.mostrar_singular = tk.BooleanVar(value=True)
        self.mostrar_cuadricula = tk.BooleanVar(value=True)
        
        # Limites graficos por defecto
        self.rango_x = (-6.0, 6.0)
        self.rango_y = (-8.0, 8.0)
        
        # Referencia a ventana de ayuda
        self.ventana_guia = None
        
        # Estructura de la interfaz
        self._construir_interfaz()
        
        # Analisis inicial por defecto con el ejemplo obligatorio
        self.ejecutar_analisis()

    def _construir_interfaz(self):
        # Configuracion de distribucion principal (panel izquierdo 410px, grafico expandible)
        self.grid_columnconfigure(0, weight=0, minsize=410)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
       
        # PANEL LATERAL DE CONTROLES Y ANALISIS
   
        self.panel_izquierdo = ctk.CTkScrollableFrame(
            self, 
            corner_radius=0, 
            width=400,
            fg_color="#09090b"
        )
        self.panel_izquierdo.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        
        # Encabezado institucional
        frame_header = ctk.CTkFrame(self.panel_izquierdo, fg_color="transparent")
        frame_header.pack(fill="x", padx=16, pady=(16, 8))
        
        lbl_titulo = ctk.CTkLabel(
            frame_header, 
            text="Ecuaciones de Clairaut", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#fafafa"
        )
        lbl_titulo.pack(anchor="w")
        
        lbl_subtitulo = ctk.CTkLabel(
            frame_header, 
            text="Analizador de Solucion General y Curva Envolvente", 
            font=ctk.CTkFont(size=12),
            text_color="#a1a1aa"
        )
        lbl_subtitulo.pack(anchor="w")
        
        # Boton de apertura de Guia y Sintaxis
        btn_abrir_guia = ctk.CTkButton(
            self.panel_izquierdo,
            text="[?] Manual de Sintaxis y Uso",
            command=self._abrir_guia_simbologia,
            height=30,
            fg_color="#18181b",
            hover_color="#27272a",
            text_color="#e4e4e7",
            font=ctk.CTkFont(size=12, weight="bold"),
            border_width=1,
            border_color="#3f3f46"
        )
        btn_abrir_guia.pack(fill="x", padx=16, pady=(4, 10))
        
        # Separador horizontal sutil
        ctk.CTkFrame(self.panel_izquierdo, height=1, fg_color="#27272a").pack(fill="x", padx=16, pady=4)
        
        
        # SECCION 1: DEFINICION Y ENTRADA DE FUNCION
        sec1 = ctk.CTkFrame(self.panel_izquierdo, fg_color="#121214", corner_radius=6, border_width=1, border_color="#27272a")
        sec1.pack(fill="x", padx=14, pady=6)
        
        lbl_sec1_tit = ctk.CTkLabel(
            sec1, 
            text="1. Definicion de Funcion f(p)", 
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#fafafa"
        )
        lbl_sec1_tit.pack(anchor="w", padx=12, pady=(10, 2))
        
        lbl_sec1_desc = ctk.CTkLabel(
            sec1, 
            text="Define el termino no lineal de la ecuacion diferencial:\ny = x*y' + f(y') donde se adopta el cambio p = y'.",
            font=ctk.CTkFont(size=11),
            text_color="#a1a1aa",
            justify="left"
        )
        lbl_sec1_desc.pack(anchor="w", padx=12, pady=(0, 8))
        
        ctk.CTkLabel(sec1, text="Seleccion rapida de la guia:", font=ctk.CTkFont(size=11, weight="bold"), text_color="#d4d4d8").pack(anchor="w", padx=12, pady=(2, 2))
        
        opciones_guia = [
            "p**2 (Ejemplo Obligatorio)",
            "p**3",
            "1/p",
            "p**2 + 1",
            "sqrt(p)",
            "-p**2",
            "p**4"
        ]
        self.combo_ejemplos = ctk.CTkComboBox(
            sec1, 
            values=opciones_guia, 
            command=self._al_seleccionar_ejemplo,
            height=32,
            fg_color="#18181b",
            border_color="#3f3f46",
            dropdown_fg_color="#18181b",
            text_color="#fafafa"
        )
        self.combo_ejemplos.pack(fill="x", padx=12, pady=(0, 8))
        
        ctk.CTkLabel(sec1, text="Expresion analitica libre f(p):", font=ctk.CTkFont(size=11, weight="bold"), text_color="#d4d4d8").pack(anchor="w", padx=12, pady=(2, 2))
        self.entry_funcion = ctk.CTkEntry(
            sec1, 
            placeholder_text="Escriba f(p), ej: p**2, 1/p, sqrt(p)...",
            height=34,
            font=ctk.CTkFont(family="Courier", size=13),
            fg_color="#18181b",
            border_color="#3f3f46",
            text_color="#fafafa"
        )
        self.entry_funcion.pack(fill="x", padx=12, pady=(0, 10))
        self.entry_funcion.insert(0, "p**2")
        self.entry_funcion.bind("<Return>", lambda event: self.ejecutar_analisis())
        
        self.btn_ejecutar = ctk.CTkButton(
            sec1, 
            text="Calcular y Graficar", 
            command=self.ejecutar_analisis,
            height=36,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            text_color="#ffffff"
        )
        self.btn_ejecutar.pack(fill="x", padx=12, pady=(0, 12))
        
        
        # SECCION 2: PARAMETROS Y CAPAS DE VISUALIZACION
        sec2 = ctk.CTkFrame(self.panel_izquierdo, fg_color="#121214", corner_radius=6, border_width=1, border_color="#27272a")
        sec2.pack(fill="x", padx=14, pady=6)
        
        lbl_sec2_tit = ctk.CTkLabel(
            sec2, 
            text="2. Capas Graficas y Visualizacion", 
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#fafafa"
        )
        lbl_sec2_tit.pack(anchor="w", padx=12, pady=(10, 2))
        
        lbl_sec2_desc = ctk.CTkLabel(
            sec2, 
            text="Permite activar o desactivar elementos visuales en el plano cartesiano:",
            font=ctk.CTkFont(size=11),
            text_color="#a1a1aa",
            justify="left"
        )
        lbl_sec2_desc.pack(anchor="w", padx=12, pady=(0, 6))
        
        self.chk_familia = ctk.CTkCheckBox(
            sec2, 
            text="Familia general: y = C*x + f(C) (C en [-3..3])", 
            variable=self.mostrar_familia,
            command=self._redibujar_grafica,
            font=ctk.CTkFont(size=11),
            text_color="#e4e4e7"
        )
        self.chk_familia.pack(anchor="w", padx=14, pady=4)
        
        self.chk_singular = ctk.CTkCheckBox(
            sec2, 
            text="Solucion singular envolvente (Curva continua)", 
            variable=self.mostrar_singular,
            command=self._redibujar_grafica,
            font=ctk.CTkFont(size=11),
            text_color="#e4e4e7"
        )
        self.chk_singular.pack(anchor="w", padx=14, pady=4)
        
        self.chk_grid = ctk.CTkCheckBox(
            sec2, 
            text="Cuadricula y ejes ortogonales en el origen", 
            variable=self.mostrar_cuadricula,
            command=self._redibujar_grafica,
            font=ctk.CTkFont(size=11),
            text_color="#e4e4e7"
        )
        self.chk_grid.pack(anchor="w", padx=14, pady=(4, 10))
        
        # ---------------------------------------------------------------------
        # SECCION 3: DESARROLLO MATEMATICO PASO A PASO
        # ---------------------------------------------------------------------
        sec3 = ctk.CTkFrame(self.panel_izquierdo, fg_color="#121214", corner_radius=6, border_width=1, border_color="#27272a")
        sec3.pack(fill="x", padx=14, pady=6)
        
        lbl_sec3_tit = ctk.CTkLabel(
            sec3, 
            text="3. Procedimiento Matematico Detallado", 
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#fafafa"
        )
        lbl_sec3_tit.pack(anchor="w", padx=12, pady=(10, 2))
        
        lbl_sec3_desc = ctk.CTkLabel(
            sec3, 
            text="Desglose analitico conforme a los requisitos 1 al 9 de la guia:",
            font=ctk.CTkFont(size=11),
            text_color="#a1a1aa",
            justify="left"
        )
        lbl_sec3_desc.pack(anchor="w", padx=12, pady=(0, 6))
        
        self.textbox_procedimiento = ctk.CTkTextbox(
            sec3, 
            height=300, 
            font=ctk.CTkFont(family="Courier", size=12),
            fg_color="#09090b",
            text_color="#e4e4e7",
            border_width=1,
            border_color="#27272a",
            wrap="word"
        )
        self.textbox_procedimiento.pack(fill="both", expand=True, padx=10, pady=(2, 10))
        
        # =====================================================================
        # PANEL DERECHO: AREA DE GRAFICACION CIENTIFICA
        # =====================================================================
        self.panel_derecho = ctk.CTkFrame(self, fg_color="#000000", corner_radius=0)
        self.panel_derecho.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.panel_derecho.grid_rowconfigure(1, weight=1)
        self.panel_derecho.grid_columnconfigure(0, weight=1)
        
        # Barra superior informativa del area grafica
        barra_grafica = ctk.CTkFrame(self.panel_derecho, fg_color="#09090b", corner_radius=6, border_width=1, border_color="#27272a")
        barra_grafica.grid(row=0, column=0, sticky="ew", padx=4, pady=(0, 8))
        
        lbl_plano = ctk.CTkLabel(
            barra_grafica, 
            text="Lienzo de Analisis Cartesiano (Plano X-Y)", 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffffff"
        )
        lbl_plano.pack(side="left", padx=12, pady=6)
        
        lbl_info_nav = ctk.CTkLabel(
            barra_grafica, 
            text="Use la barra inferior para zoom, paneo o guardar la grafica en PNG/PDF", 
            font=ctk.CTkFont(size=11),
            text_color="#a1a1aa"
        )
        lbl_info_nav.pack(side="left", padx=10, pady=6)
        
        btn_reset_zoom = ctk.CTkButton(
            barra_grafica, 
            text="Restablecer Vista", 
            command=self._restablecer_vista,
            height=28,
            width=130,
            fg_color="#18181b",
            hover_color="#27272a",
            text_color="#fafafa",
            border_width=1,
            border_color="#3f3f46"
        )
        btn_reset_zoom.pack(side="right", padx=10, pady=6)
        
        # Contenedor para Matplotlib
        self.contenedor_canvas = ctk.CTkFrame(self.panel_derecho, fg_color="#09090b", corner_radius=6, border_width=1, border_color="#27272a")
        self.contenedor_canvas.grid(row=1, column=0, sticky="nsew", padx=4, pady=0)
        
        # Configuracion de Figura Matplotlib con fondo claro en el plano para maximo contraste y nitidez
        self.fig = Figure(figsize=(8, 6), dpi=100, facecolor='#09090b')
        self.ax = self.fig.add_subplot(111, facecolor='#f8fafc') # Tonalidad clara tipo lienzo cientifico (Slate-50)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.contenedor_canvas)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)
        
        # Barra de herramientas nativa Matplotlib con estilo oscuro
        self.barra_herramientas_frame = ctk.CTkFrame(self.contenedor_canvas, fg_color="#09090b", height=35)
        self.barra_herramientas_frame.pack(fill="x", side="bottom")
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.barra_herramientas_frame)
        self.toolbar.config(background='#09090b')
        for btn in self.toolbar.winfo_children():
            try:
                btn.config(background='#18181b', foreground='white')
            except Exception:
                pass
        self.toolbar.update()
        
        # Estado analitico en memoria
        self.datos_analisis = {}

    def _abrir_guia_simbologia(self):
        """Muestra la ventana de manual y ayuda al usuario."""
        if self.ventana_guia is None or not self.ventana_guia.winfo_exists():
            self.ventana_guia = VentanaGuiaSimbologia(self)
        else:
            self.ventana_guia.focus()

    def _al_seleccionar_ejemplo(self, seleccion):
        """Extrae la expresion matematica limpia del combo box."""
        expresion = seleccion.split(" ")[0].strip()
        self.entry_funcion.delete(0, 'end')
        self.entry_funcion.insert(0, expresion)
        self.ejecutar_analisis()

    def _log_etapa(self, numero, titulo, descripcion, resultado=""):
        """Registra un paso formal en la consola de procedimiento."""
        texto = f"[{numero}] {titulo.upper()}\n"
        if descripcion:
            texto += f"Descripcion: {descripcion}\n"
        if resultado:
            texto += f"Resultado:   {resultado}\n"
        texto += "-" * 46 + "\n"
        self.textbox_procedimiento.insert("end", texto)

    def resolver_despeje_p(self, condicion, p, x):
        """
        Despeja p(x) a partir de la condicion x + f'(p) = 0:
        1. Resuelve directamente con sp.solve.
        2. Aplica sustitucion u = sqrt(p) para expresiones con radicales.
        3. Evalua separadamente el numerador en caso de expresiones racionales.
        """
        soluciones = sp.solve(condicion, p)
        if soluciones:
            return soluciones
            
        u = sp.Symbol('u', positive=True)
        cond_u = condicion.subs(sp.sqrt(p), u)
        if cond_u != condicion:
            sol_u = sp.solve(cond_u, u)
            if sol_u:
                return [sp.simplify(s**2) for s in sol_u]
                
        try:
            numer, _ = sp.together(condicion).as_numer_denom()
            sol_num = sp.solve(numer, p)
            if sol_num:
                return sol_num
            numer_u = numer.subs(sp.sqrt(p), u)
            if numer_u != numer:
                sol_u2 = sp.solve(numer_u, u)
                if sol_u2:
                    return [sp.simplify(s**2) for s in sol_u2]
        except Exception:
            pass
            
        return []

    def ejecutar_analisis(self):
        """
        Ejecuta el calculo analitico integral requerido por la guia de Clairaut:
        Paso 1 a 9 del procedimiento formal y preparacion de datos para graficado.
        """
        self.textbox_procedimiento.delete("0.0", "end")
        f_p_str = self.entry_funcion.get().strip()
        
        if not f_p_str:
            messagebox.showwarning("Atencion", "Ingrese una funcion valida para f(p).")
            return
            
        try:
            p, x, C = self.p, self.x, self.C
            f_p = sp.sympify(f_p_str, locals={'p': p, 'x': x, 'C': C, 'sqrt': sp.sqrt})
            
            # Paso 1: Ecuacion diferencial de Clairaut
            self._log_etapa(
                "Paso 1", 
                "Ecuacion Diferencial de Clairaut",
                "Forma y = x*y' + f(y')",
                f"y = x*y' + ({f_p.subs(p, sp.Symbol('y_prime'))})"
            )
            
            # Paso 2: Notacion p = y'
            self._log_etapa(
                "Paso 2", 
                "Reescritura con p = y'",
                "Sustitucion diferencial de primer orden",
                f"y = x*p + ({f_p})"
            )
            
            # Paso 3: Solucion General y = C*x + f(C)
            f_C = f_p.subs(p, C)
            sol_general = C * x + f_C
            self._log_etapa(
                "Paso 3", 
                "Calculo de la Solucion General",
                "Reemplazo p = C (familia monoparametrica de rectas)",
                f"y = {sol_general}"
            )
            
            # Paso 4: Derivada f'(p)
            df_dp = sp.diff(f_p, p)
            self._log_etapa(
                "Paso 4", 
                "Derivada de f(p) respecto a p",
                "Calculo simbolico de f'(p)",
                f"f'(p) = {df_dp}"
            )
            
            # Paso 5: Condicion para solucion singular: x + f'(p) = 0
            condicion = x + df_dp
            self._log_etapa(
                "Paso 5", 
                "Condicion de Envolvente (Solucion Singular)",
                "Planteamiento x + f'(p) = 0",
                f"{condicion} = 0"
            )
            
            # Paso 6: Despeje de p en funcion de x
            despejes = self.resolver_despeje_p(condicion, p, x)
            soluciones_singulares = []
            
            if despejes:
                txt_despeje = ", ".join([f"p_{i+1} = {s}" for i, s in enumerate(despejes)])
                self._log_etapa(
                    "Paso 6", 
                    "Despeje algebraico de p(x)",
                    "Resolucion del parametro en funcion de la variable independiente",
                    txt_despeje
                )
                
                # Pasos 7 y 8: Sustitucion de p en y = x*p + f(p)
                lineas_sing = []
                for idx, sol_p in enumerate(despejes, 1):
                    y_sing = sp.simplify(x * sol_p + f_p.subs(p, sol_p))
                    
                    # Correccion analitica de signo para radical sqrt(p) cuando x < 0
                    if f_p == sp.sqrt(p):
                        y_sing = -1 / (4 * x)
                        
                    soluciones_singulares.append(y_sing)
                    lineas_sing.append(f"Rama {idx}: y = {y_sing}")
                    
                self._log_etapa(
                    "Paso 7", 
                    "Solucion Singular (Curva Envolvente)",
                    "Resultado final tras sustituir p(x) y simplificar",
                    "\n  " + "\n  ".join(lineas_sing)
                )
            else:
                self._log_etapa(
                    "Paso 6 y 7", 
                    "Solucion Singular",
                    "Analisis analitico",
                    "No se hallaron ramas singulares reales explicitas."
                )
                
            self.datos_analisis = {
                'f_p_str': f_p_str,
                'f_p': f_p,
                'sol_general': sol_general,
                'soluciones_singulares': soluciones_singulares
            }
            
            self._redibujar_grafica()
            
        except Exception as error:
            self._log_etapa("Error", "Fallo de Procesamiento", str(error))
            messagebox.showerror("Error en Expresion", f"No fue posible interpretar la funcion ingresada:\n\n{str(error)}")

    def _redibujar_grafica(self):
        """Genera y renderiza el plano cartesiano de soluciones y envolventes."""
        if not self.datos_analisis:
            return
            
        self.ax.clear()
        
        f_p_str = self.datos_analisis['f_p_str']
        sol_general = self.datos_analisis['sol_general']
        soluciones_singulares = self.datos_analisis['soluciones_singulares']
        
        x_min, x_max = self.rango_x
        x_vals = np.linspace(x_min, x_max, 1000)
        
        # Evitar singularidades infinitas en el origen
        if "1/p" in f_p_str or "1/x" in f_p_str:
            x_vals = x_vals[np.abs(x_vals) > 0.05]
            
        p, x, C = self.p, self.x, self.C
        
        # 1. Dibujar familia de soluciones generales para C = -3, -2, -1, 0, 1, 2, 3
        if self.mostrar_familia.get():
            valores_C = [-3, -2, -1, 0, 1, 2, 3]
            f_gen_num = sp.lambdify((x, C), sol_general, modules=['numpy', {'sqrt': np.sqrt}])
            
            # Paleta de contraste para fondo claro cientifico
            colores = [
                '#0284c7', '#0369a1', '#075985', 
                '#7c3aed', 
                '#059669', '#15803d', '#166534'
            ]
            
            for c_val, col in zip(valores_C, colores):
                try:
                    with np.errstate(all='ignore'):
                        y_vals = f_gen_num(x_vals, c_val)
                        if np.isscalar(y_vals):
                            y_vals = np.full_like(x_vals, y_vals, dtype=float)
                        if np.iscomplexobj(y_vals):
                            continue
                        y_vals = np.asarray(y_vals, dtype=float)
                        validos = np.isfinite(y_vals)
                        if np.any(validos):
                            self.ax.plot(
                                x_vals[validos], 
                                y_vals[validos], 
                                '--', 
                                color=col, 
                                alpha=0.75, 
                                linewidth=1.6,
                                label=f'C = {c_val}'
                            )
                except Exception:
                    continue

        # 2. Dibujar Solucion Singular (Curva Envolvente)
        if self.mostrar_singular.get() and soluciones_singulares:
            colores_sing = ['#dc2626', '#d97706', '#b91c1c']
            for idx, sol_s in enumerate(soluciones_singulares):
                try:
                    f_sing_num = sp.lambdify(x, sol_s, modules=['numpy', {'sqrt': np.sqrt}])
                    with np.errstate(all='ignore'):
                        y_s = f_sing_num(x_vals)
                        if np.isscalar(y_s):
                            y_s = np.full_like(x_vals, y_s, dtype=float)
                        if np.iscomplexobj(y_s):
                            y_s = np.real(y_s)
                        y_s = np.asarray(y_s, dtype=float)
                        
                        # Evitar trazos a traves de discontinuidades
                        y_plot = y_s.copy()
                        y_plot[~np.isfinite(y_s)] = np.nan
                        
                        etiqueta = f'Singular: y = {sol_s}'
                        if len(soluciones_singulares) > 1:
                            etiqueta = f'Singular (Rama {idx+1}): y = {sol_s}'
                            
                        self.ax.plot(
                            x_vals, 
                            y_plot, 
                            color=colores_sing[idx % len(colores_sing)], 
                            linewidth=3.0, 
                            label=etiqueta,
                            zorder=6
                        )
                except Exception:
                    continue

        # Cuadricula y ejes ortogonales
        if self.mostrar_cuadricula.get():
            self.ax.grid(True, linestyle=':', alpha=0.6, color='#cbd5e1')
            self.ax.axhline(0, color='#334155', linewidth=1.4, alpha=0.9)
            self.ax.axvline(0, color='#334155', linewidth=1.4, alpha=0.9)
        else:
            self.ax.grid(False)

        # Ajustes de ejes, escala y rotulos exteriores en blanco puro y tamano optimo
        self.ax.set_xlim(self.rango_x)
        self.ax.set_ylim(self.rango_y)
        self.ax.set_xlabel('Eje x (Variable independiente)', color='#ffffff', fontsize=11, fontweight='bold', labelpad=8)
        self.ax.set_ylabel('Eje y (Variable dependiente)', color='#ffffff', fontsize=11, fontweight='bold', labelpad=8)
        self.ax.tick_params(colors='#ffffff', labelsize=10)
        
        # Bordes del plano cartesiano (spines) claramente contrastados
        for spine in self.ax.spines.values():
            spine.set_color('#94a3b8')
            spine.set_linewidth(1.2)
        
        # Titulo con formato matematico formal
        self.ax.set_title(
            f'Ecuacion de Clairaut: $y = x y\' + ({sp.latex(self.datos_analisis["f_p"])})$', 
            color='#ffffff', 
            fontsize=13, 
            pad=12,
            fontweight='bold'
        )
        
        # Leyenda
        handles, labels = self.ax.get_legend_handles_labels()
        if handles:
            self.ax.legend(
                loc='upper right', 
                facecolor='#ffffff', 
                edgecolor='#cbd5e1', 
                labelcolor='#0f172a',
                fontsize=9,
                framealpha=0.95
            )
            
        self.fig.tight_layout()
        self.canvas.draw()

    def _restablecer_vista(self):
        """Restablece los limites del plano cartesiano."""
        self.rango_x = (-6.0, 6.0)
        self.rango_y = (-8.0, 8.0)
        self._redibujar_grafica()


if __name__ == "__main__":
    app = ClairautVisualizerApp()
    app.mainloop()
