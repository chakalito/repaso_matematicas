import time
import random
import tkinter as tk
from tkinter import messagebox

from config import Configuracion, Utilidades
from operacionSuma import OperacionSuma
from operacionResta import OperacionResta
from operacionMultiplicacion import OperacionMultiplicacion
from operacionDivision import OperacionDivision

class JuegoOperacionesMatematicas:
    """Juego de operaciones matemáticas con rejilla triangular y selección aleatoria.
    
    Cuando se acierta, la celda se marca en verde y la operación ya no vuelve a aparecer.
    Si se falla, la celda se marca en rojo y la operación se reinserta en la lista de disponibles.
    """

    def __init__(self, root, tipo_operacion, callback_menu):
        self.root = root
        self.tipo_operacion = tipo_operacion
        self.callback_menu = callback_menu

        # Determinar el rango según el tipo de operación.
        if tipo_operacion in ("multiplicacion", "division"):
            inicio, fin = 2, 13
        else:
            inicio, fin = 1, 13

        # Instanciar la operación adecuada según el tipo.
        if tipo_operacion == "suma":
            self.controlador = OperacionSuma(inicio, fin)
        elif tipo_operacion == "resta":
            self.controlador = OperacionResta(inicio, fin)
        elif tipo_operacion == "multiplicacion":
            self.controlador = OperacionMultiplicacion(inicio, fin)
        elif tipo_operacion == "division":
            self.controlador = OperacionDivision(inicio, fin)
        else:
            raise ValueError("Tipo de operación no soportada.")

        self.root.title(Configuracion.TITULOS_OPERACIONES[tipo_operacion])
        self.root.configure(bg=Configuracion.COLOR_FONDO)

        self._inicializar_variables()
        self._crear_interfaz()
        self.iniciar_juego()
        self._configurar_reloj()

    def _inicializar_variables(self):
        """Inicializa las variables del juego."""
        self.aciertos = 0
        self.fallos = 0
        self.tiempo_inicio = time.time()
        self.operacion_actual = None
        self.casillas_practicadas = set()
        self.modo_competicion = False
        self.jugador_actual = 1
        self.puntos_jugador1 = 0
        self.puntos_jugador2 = 0

        # Se genera la lista de operaciones una única vez.
        self.lista_operaciones = self.controlador.generar_operaciones()
        self.operaciones_disponibles = self.lista_operaciones.copy()

    def _crear_etiqueta(self, parent, texto, font=None, fg=None, bg=None, **kwargs):
        """Crea una etiqueta con configuración centralizada."""
        return tk.Label(parent, text=texto,
                        font=font or Configuracion.FUENTE_NORMAL,
                        fg=fg or Configuracion.COLOR_TEXTO,
                        bg=bg or Configuracion.COLOR_FONDO,
                        **kwargs)

    def _crear_interfaz(self):
        """Construye la interfaz del juego."""
        self.frame_principal = tk.Frame(self.root, bg=Configuracion.COLOR_FONDO)
        self.frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._crear_titulo()
        self._crear_tabla_visual()
        self._crear_area_preguntas()
        self._crear_area_estadisticas()
        self._crear_menu()

    def _crear_titulo(self):
        """Crea el título decorado."""
        titulo_frame = tk.Frame(self.frame_principal, bg=Configuracion.COLOR_FONDO)
        titulo_frame.pack(pady=5)
        self._crear_etiqueta(titulo_frame, "✨", font=("Arial", 20), fg=Configuracion.COLOR_ROSA)\
            .pack(side=tk.LEFT, padx=5)
        self._crear_etiqueta(titulo_frame, Configuracion.TITULOS_OPERACIONES[self.tipo_operacion],
                             font=Configuracion.FUENTE_TITULO, fg=Configuracion.COLOR_TITULO)\
            .pack(side=tk.LEFT, padx=10)
        self._crear_etiqueta(titulo_frame, "✨", font=("Arial", 20), fg=Configuracion.COLOR_ROSA)\
            .pack(side=tk.LEFT, padx=5)

    def _crear_tabla_visual(self):
        """Crea la tabla visual triangular de operaciones."""
        self.tabla_frame = tk.Frame(self.frame_principal, bg=Configuracion.COLOR_FONDO)
        self.tabla_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        inicio = self.controlador.inicio
        self.celdas = {}
        # Se utiliza la lista de operaciones ya generada.
        for operacion in self.lista_operaciones:
            a, b = operacion
            row, col = a - inicio, b - inicio
            texto = self.controlador.formatear_celda(operacion)
            celda = self._crear_etiqueta(self.tabla_frame, texto,
                                         font=Configuracion.FUENTE_CELDA,
                                         bg=Configuracion.COLOR_NEUTRO,
                                         borderwidth=1, relief="solid",
                                         padx=5, pady=5)
            celda.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
            self.celdas[operacion] = celda

        dimension = self.controlador.fin - inicio
        for idx in range(dimension):
            self.tabla_frame.grid_rowconfigure(idx, weight=1)
            self.tabla_frame.grid_columnconfigure(idx, weight=1)

    def _crear_area_preguntas(self):
        """Crea el área de preguntas y respuestas."""
        self.frame_preguntas = tk.Frame(self.root, bg=Configuracion.COLOR_FONDO)
        self.frame_preguntas.pack(fill=tk.X, padx=10, pady=5)

        self.pregunta_var = tk.StringVar()
        self._crear_etiqueta(self.frame_preguntas, "", font=Configuracion.FUENTE_SUBTITULO,
                             fg=Configuracion.COLOR_TEXTO, textvariable=self.pregunta_var)\
            .pack(side=tk.LEFT, padx=5)

        self.respuesta_var = tk.StringVar()
        self.respuesta_entry = tk.Entry(self.frame_preguntas, textvariable=self.respuesta_var,
                                        font=Configuracion.FUENTE_SUBTITULO, width=8, bd=3)
        self.respuesta_entry.pack(side=tk.LEFT, padx=5)
        self.respuesta_entry.bind("<Return>", self.verificar_respuesta)

        tk.Button(self.frame_preguntas, text="✓ Comprobar",
                  command=self.verificar_respuesta,
                  font=Configuracion.FUENTE_NORMAL,
                  bg="#FFB6C1", fg=Configuracion.COLOR_TEXTO)\
            .pack(side=tk.LEFT, padx=5)

    def _crear_area_estadisticas(self):
        """Crea el área de estadísticas."""
        self.frame_stats = tk.Frame(self.root, bg=Configuracion.COLOR_CABECERA)
        self.frame_stats.pack(fill=tk.X, padx=10, pady=5)

        self.stats_var = tk.StringVar(value="Aciertos: 0 | Fallos: 0 | Tiempo: 00:00:00")
        self._crear_etiqueta(self.frame_stats, "", font=Configuracion.FUENTE_NORMAL,
                             bg=Configuracion.COLOR_CABECERA, fg=Configuracion.COLOR_TEXTO,
                             textvariable=self.stats_var)\
            .pack(fill=tk.X, padx=10, pady=5)

    def _crear_menu(self):
        """Crea el menú de opciones."""
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.opciones_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Opciones", menu=self.opciones_menu)
        self.opciones_menu.add_command(label="Reiniciar juego", command=self.reiniciar_juego)
        self.opciones_menu.add_command(label="Ver informe mágico", command=self.generar_informe)
        self.opciones_menu.add_separator()

        self.modo_menu = tk.Menu(self.opciones_menu, tearoff=0)
        self.opciones_menu.add_cascade(label="Modo de juego", menu=self.modo_menu)
        self.modo_menu.add_command(label="Modo duelo mágico (2 jugadores)", command=self.activar_modo_competicion)
        self.modo_menu.add_command(label="Modo individual", command=self.desactivar_modo_competicion)

        self.opciones_menu.add_separator()
        self.opciones_menu.add_command(label="Volver al castillo principal", command=self.volver_menu)
        self.opciones_menu.add_command(label="Salir", command=self.root.quit)

    def _configurar_reloj(self):
        """Configura la actualización periódica del reloj."""
        def actualizar_reloj():
            self.actualizar_estadisticas()
            self.root.after(1000, actualizar_reloj)
        self.root.after(1000, actualizar_reloj)

    def actualizar_estadisticas(self):
        """Actualiza las estadísticas de la sesión."""
        tiempo_transcurrido = time.time() - self.tiempo_inicio
        tiempo_formato = Utilidades.formatear_tiempo(tiempo_transcurrido)
        if self.modo_competicion:
            self.stats_var.set(
                f"👑 Jugador 1: {self.puntos_jugador1} pts | 👑 Jugador 2: {self.puntos_jugador2} pts | "
                f"Turno: Jugador {self.jugador_actual} | ⏰ {tiempo_formato}"
            )
        else:
            self.stats_var.set(
                f"✅ Aciertos: {self.aciertos} | ❌ Fallos: {self.fallos} | ⏰ {tiempo_formato}"
            )

    def iniciar_juego(self):
        """Resetea estadísticas y presenta la primera pregunta."""
        self.tiempo_inicio = time.time()
        self.aciertos = 0
        self.fallos = 0
        self.actualizar_estadisticas()
        self.generar_nueva_pregunta()
        self.respuesta_entry.focus_set()

    def generar_nueva_pregunta(self):
        """Selecciona al azar la siguiente operación de las disponibles."""
        if self.operaciones_disponibles:
            indice = random.randint(0, len(self.operaciones_disponibles) - 1)
            self.operacion_actual = self.operaciones_disponibles.pop(indice)
        else:
            self._mostrar_final_juego()
            return

        self.pregunta_var.set(self.controlador.formatear_pregunta(self.operacion_actual))
        self.respuesta_var.set("")
        self.respuesta_entry.focus_set()

    def _mostrar_final_juego(self):
        """Muestra el mensaje final y permite reiniciar o volver al menú."""
        total = len(self.casillas_practicadas)
        porcentaje = (self.aciertos / (self.aciertos + self.fallos)) * 100 if (self.aciertos + self.fallos) else 0

        if porcentaje >= 90:
            titulo = "¡Excelente trabajo mágico! 🌟✨"
            mensaje = "¡Has dominado las operaciones de forma extraordinaria!"
        elif porcentaje >= 75:
            titulo = "¡Muy buen trabajo! ✨"
            mensaje = "¡Has completado las operaciones con gran habilidad mágica!"
        else:
            titulo = "¡Lo has logrado! ✨"
            mensaje = "Con más práctica te convertirás en una gran princesa matemática!"

        mensaje += (f"\n\nOperaciones completadas: {total}"
                    f"\nAciertos: {self.aciertos}"
                    f"\nFallos: {self.fallos}"
                    f"\nPrecisión mágica: {porcentaje:.1f}%")

        if messagebox.askquestion(titulo, mensaje + "\n\n¿Deseas reiniciar la práctica?") == "yes":
            self.reiniciar_juego()
        else:
            self.volver_menu()

    def verificar_respuesta(self, event=None):
        """Verifica la respuesta del usuario."""
        if not self.operacion_actual:
            return

        try:
            respuesta_usuario = int(self.respuesta_var.get().strip())
        except ValueError:
            messagebox.showwarning("Error", "Introduce un número entero.")
            self.respuesta_var.set("")
            self.respuesta_entry.focus_set()
            return

        respuesta_correcta = self.controlador.calcular_respuesta(self.operacion_actual)
        self.casillas_practicadas.add(self.operacion_actual)
        es_correcta = (respuesta_usuario == respuesta_correcta)
        self._actualizar_celda(es_correcta)

        if es_correcta:
            self.aciertos += 1
            if self.modo_competicion:
                self._actualizar_puntos_jugador()
            messagebox.showinfo("¡Correcto! ✨",
                                f"¡Respuesta mágica!{' Turno del Jugador ' + str(3 - self.jugador_actual) if self.modo_competicion else ''}")
        else:
            self.fallos += 1
            # Si la respuesta es incorrecta, se vuelve a insertar la operación en la lista de disponibles.
            self.operaciones_disponibles.append(self.operacion_actual)
            messagebox.showinfo("¡Ups! 🌟", f"La respuesta correcta es {respuesta_correcta}. ¡Sigue intentándolo!")

        if self.modo_competicion:
            self._cambiar_jugador()

        self.actualizar_estadisticas()
        self.generar_nueva_pregunta()

    def _actualizar_celda(self, es_correcta):
        """Actualiza el color de la celda según la respuesta."""
        if self.operacion_actual in self.celdas:
            color = Configuracion.COLOR_CORRECTO if es_correcta else Configuracion.COLOR_INCORRECTO
            self.celdas[self.operacion_actual].config(bg=color)

    def _actualizar_puntos_jugador(self):
        """Actualiza los puntos en modo competición."""
        if self.jugador_actual == 1:
            self.puntos_jugador1 += 1
        else:
            self.puntos_jugador2 += 1

    def _cambiar_jugador(self):
        """Alterna el turno entre jugadoras."""
        self.jugador_actual = 3 - self.jugador_actual

    def reiniciar_juego(self):
        """Reinicia el juego tras confirmación."""
        if messagebox.askyesno("Reiniciar", "¿Deseas reiniciar el juego?"):
            for celda in self.celdas.values():
                celda.config(bg=Configuracion.COLOR_NEUTRO)
            self.casillas_practicadas.clear()
            self.operaciones_disponibles = self.lista_operaciones.copy()
            self.aciertos = 0
            self.fallos = 0
            self.jugador_actual = 1
            self.puntos_jugador1 = 0
            self.puntos_jugador2 = 0
            self.iniciar_juego()

    def generar_informe(self):
        """Genera un informe en una ventana secundaria."""
        ventana = tk.Toplevel(self.root)
        ventana.title("✨ Informe Mágico ✨")
        ventana.geometry("550x450")
        ventana.configure(bg=Configuracion.COLOR_FONDO)
        self._crear_contenido_informe(ventana)

    def _crear_contenido_informe(self, ventana):
        """Crea el contenido del informe."""
        total = len(self.casillas_practicadas)
        porcentaje = (self.aciertos / (self.aciertos + self.fallos)) * 100 if (self.aciertos + self.fallos) else 0

        titulos = {
            "suma": "SUMA",
            "resta": "RESTA",
            "multiplicacion": "MULTIPLICACIÓN",
            "division": "DIVISIÓN"
        }

        titulo_frame = tk.Frame(ventana, bg=Configuracion.COLOR_FONDO)
        titulo_frame.pack(fill=tk.X, pady=10)
        self._crear_etiqueta(titulo_frame, "✨", font=("Arial", 24), fg=Configuracion.COLOR_ROSA)\
            .pack(side=tk.LEFT, padx=10)
        self._crear_etiqueta(titulo_frame, f"TU AVENTURA MATEMÁTICA DE {titulos[self.tipo_operacion]}",
                             font=Configuracion.FUENTE_TITULO, fg=Configuracion.COLOR_TITULO)\
            .pack(side=tk.LEFT)
        self._crear_etiqueta(titulo_frame, "✨", font=("Arial", 24), fg=Configuracion.COLOR_ROSA)\
            .pack(side=tk.LEFT, padx=10)

        contenido_frame = tk.Frame(ventana, bg=Configuracion.COLOR_FONDO, padx=20, pady=10)
        contenido_frame.pack(fill=tk.BOTH, expand=True)

        estilo = {"font": Configuracion.FUENTE_NORMAL,
                  "bg": Configuracion.COLOR_FONDO,
                  "fg": Configuracion.COLOR_TEXTO,
                  "anchor": "w"}
        self._crear_etiqueta(contenido_frame, f"🧁 Total de operaciones: {total}", **estilo)\
            .pack(fill=tk.X, pady=5)
        self._crear_etiqueta(contenido_frame, f"✅ Aciertos: {self.aciertos}", **estilo)\
            .pack(fill=tk.X, pady=5)
        self._crear_etiqueta(contenido_frame, f"❌ Fallos: {self.fallos}", **estilo)\
            .pack(fill=tk.X, pady=5)

        self._crear_barra_progreso(contenido_frame, porcentaje)

        if self.modo_competicion:
            self._mostrar_resultados_competicion(contenido_frame, estilo)

        boton_frame = tk.Frame(ventana, bg=Configuracion.COLOR_FONDO)
        boton_frame.pack(pady=10)
        tk.Button(boton_frame, text="✨ Cerrar ✨", command=ventana.destroy,
                  font=Configuracion.FUENTE_NORMAL, bg="#FFB6C1", fg=Configuracion.COLOR_TEXTO,
                  padx=10, pady=5).pack()

    def _crear_barra_progreso(self, contenedor, porcentaje):
        """Crea una barra visual de progreso en el informe."""
        barra_frame = tk.Frame(contenedor, bg=Configuracion.COLOR_FONDO)
        barra_frame.pack(fill=tk.X, pady=10)
        self._crear_etiqueta(barra_frame, f"Nivel de magia: {porcentaje:.1f}%",
                             font=(Configuracion.FUENTE_NORMAL[0], Configuracion.FUENTE_NORMAL[1], "bold"),
                             fg=Configuracion.COLOR_TITULO).pack(anchor="w")
        barra_bg = tk.Frame(barra_frame, bg="#FFD3E0", height=30, width=400)
        barra_bg.pack(pady=5)
        ancho_valor = max(5, int(4 * porcentaje))
        tk.Frame(barra_bg, bg=Configuracion.COLOR_ROSA, height=30, width=ancho_valor)\
            .place(x=0, y=0)

    def _mostrar_resultados_competicion(self, contenedor, estilo):
        """Muestra los resultados del modo competición en el informe."""
        self._crear_etiqueta(contenedor, "🏆 DUELO DE HECHIZOS MATEMÁGICOS 🏆",
                             font=(Configuracion.FUENTE_SUBTITULO[0], Configuracion.FUENTE_SUBTITULO[1], "bold"),
                             fg=Configuracion.COLOR_TITULO).pack(fill=tk.X, pady=5)
        self._crear_etiqueta(contenedor, f"👑 Princesa 1: {self.puntos_jugador1} pts", **estilo)\
            .pack(fill=tk.X, pady=5)
        self._crear_etiqueta(contenido_frame, f"👑 Princesa 2: {self.puntos_jugador2} pts", **estilo)\
            .pack(fill=tk.X, pady=5)
        if self.puntos_jugador1 > self.puntos_jugador2:
            ganador = "Princesa 1"
        elif self.puntos_jugador2 > self.puntos_jugador1:
            ganador = "Princesa 2"
        else:
            ganador = "Empate Real"
        resultado = f"Ganadora del duelo: {ganador}" if ganador != "Empate Real" else "Resultado: Empate Real"
        self._crear_etiqueta(contenedor, resultado,
                             font=(Configuracion.FUENTE_SUBTITULO[0], Configuracion.FUENTE_SUBTITULO[1], "bold"),
                             fg=Configuracion.COLOR_TITULO).pack(fill=tk.X, pady=10)

    def activar_modo_competicion(self):
        """Activa el modo competición para 2 jugadoras."""
        if messagebox.askyesno("Modo Duelo Mágico", "¿Activar modo duelo para 2 princesas matemáticas?"):
            self.modo_competicion = True
            self.jugador_actual = 1
            self.puntos_jugador1 = 0
            self.puntos_jugador2 = 0
            messagebox.showinfo("Duelo Mágico", "¡Duelo activado! Comienza la Princesa 1.")
            self.reiniciar_juego()

    def desactivar_modo_competicion(self):
        """Desactiva el modo competición y vuelve al modo individual."""
        if self.modo_competicion and messagebox.askyesno("Desactivar Duelo", "¿Volver al modo individual?"):
            self.modo_competicion = False
            self.reiniciar_juego()
            messagebox.showinfo("Modo Princesa", "¡Volviste al modo individual!")

    def volver_menu(self):
        """Vuelve al menú principal tras confirmar la acción."""
        if messagebox.askyesno("Volver al Castillo", "¿Volver al castillo principal? Se perderá tu progreso."):
            self.frame_principal.destroy()
            self.frame_stats.destroy()
            self.frame_preguntas.destroy()
            self.callback_menu()
