import tkinter as tk
from config import Configuracion
from juego import JuegoOperacionesMatematicas

class MenuPrincipal:
    """Clase para la pantalla del menú principal"""
    
    def __init__(self, root):
        """Inicializa el menú principal"""
        self.root = root
        self.root.title("Matemáticas Mágicas")
        self.root.geometry("900x650")
        self.root.configure(bg=Configuracion.COLOR_FONDO)
        
        # Frame principal
        self.frame_principal = tk.Frame(root, bg=Configuracion.COLOR_FONDO)
        self.frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self._crear_interfaz()
    
    def _crear_interfaz(self):
        """Crea todos los elementos de la interfaz del menú principal"""
        self._crear_titulo()
        self._crear_descripcion()
        self._crear_botones()
        self._agregar_decoraciones()
        self._crear_boton_salir()
    
    def _crear_titulo(self):
        """Crea el título decorado"""
        titulo_frame = tk.Frame(self.frame_principal, bg=Configuracion.COLOR_FONDO)
        titulo_frame.pack(pady=10)
        
        # Estrella izquierda
        estrella_izq = tk.Label(titulo_frame, text="✦", font=("Arial", 30), 
                               fg=Configuracion.COLOR_ROSA, bg=Configuracion.COLOR_FONDO)
        estrella_izq.pack(side=tk.LEFT, padx=10)
        
        # Título central
        titulo = tk.Label(titulo_frame, text="MATEMÁTICAS MÁGICAS", 
                         font=Configuracion.FUENTE_GRANDE, 
                         fg=Configuracion.COLOR_TITULO, bg=Configuracion.COLOR_FONDO)
        titulo.pack(side=tk.LEFT, padx=10)
        
        # Estrella derecha
        estrella_der = tk.Label(titulo_frame, text="✦", font=("Arial", 30), 
                               fg=Configuracion.COLOR_ROSA, bg=Configuracion.COLOR_FONDO)
        estrella_der.pack(side=tk.LEFT, padx=10)
    
    def _crear_descripcion(self):
        """Crea el subtítulo de la pantalla"""
        descripcion = tk.Label(self.frame_principal, 
                             text="✨ Elige la aventura matemática que quieres comenzar ✨", 
                             font=Configuracion.FUENTE_SUBTITULO, 
                             fg=Configuracion.COLOR_LILA, 
                             bg=Configuracion.COLOR_FONDO)
        descripcion.pack(pady=20)
    
    def _crear_botones(self):
        """Crea los botones para cada operación matemática"""
        botones_frame = tk.Frame(self.frame_principal, bg=Configuracion.COLOR_FONDO)
        botones_frame.pack(pady=30)
        
        # Configuración común para botones
        estilo_botones = {
            "font": Configuracion.FUENTE_BOTONES,
            "width": 15,
            "height": 2,
            "borderwidth": 3,
            "relief": "raised"
        }
        
        # Botón de suma
        btn_sumar = tk.Button(botones_frame, text="Sumar", 
                             bg="#FFD1DC",  # Rosa pálido
                             fg=Configuracion.COLOR_TEXTO,
                             command=lambda: self.iniciar_juego("suma"), 
                             **estilo_botones)
        btn_sumar.grid(row=0, column=0, padx=15, pady=15)
        
        # Botón de resta
        btn_restar = tk.Button(botones_frame, text="Restar", 
                              bg="#E0B0FF",  # Lila pálido
                              fg="#4B0082",  # Índigo
                              command=lambda: self.iniciar_juego("resta"), 
                              **estilo_botones)
        btn_restar.grid(row=0, column=1, padx=15, pady=15)
        
        # Botón de multiplicación
        btn_multiplicar = tk.Button(botones_frame, text="Multiplicar", 
                                   bg="#FFB6C1",  # Rosa claro
                                   fg=Configuracion.COLOR_TEXTO,
                                   command=lambda: self.iniciar_juego("multiplicacion"), 
                                   **estilo_botones)
        btn_multiplicar.grid(row=1, column=0, padx=15, pady=15)
        
        # Botón de división
        btn_dividir = tk.Button(botones_frame, text="Dividir", 
                               bg="#D8BFD8",  # Cardo (violeta claro)
                               fg="#4B0082",  # Índigo
                               command=lambda: self.iniciar_juego("division"), 
                               **estilo_botones)
        btn_dividir.grid(row=1, column=1, padx=15, pady=15)
    
    def _agregar_decoraciones(self):
        """Agrega decoraciones estéticas a la interfaz"""
        decoracion_frame = tk.Frame(self.frame_principal, bg=Configuracion.COLOR_FONDO)
        decoracion_frame.pack(pady=10, fill=tk.X)
        
        for deco in Configuracion.DECORACIONES:
            lbl = tk.Label(decoracion_frame, 
                          text=deco, 
                          font=("Arial", 24), 
                          bg=Configuracion.COLOR_FONDO)
            lbl.pack(side=tk.LEFT, expand=True)
    
    def _crear_boton_salir(self):
        """Crea el botón para salir de la aplicación"""
        btn_salir = tk.Button(self.frame_principal, 
                             text="Salir", 
                             command=self.root.quit, 
                             font=Configuracion.FUENTE_NORMAL, 
                             bg="#FFB6C1",
                             fg=Configuracion.COLOR_TEXTO,
                             width=8)
        btn_salir.pack(pady=10)
    
    def iniciar_juego(self, operacion):
        """Inicia un juego para la operación seleccionada"""
        self.frame_principal.pack_forget()
        # Iniciar el juego correspondiente pasando el callback para volver al menú
        JuegoOperacionesMatematicas(self.root, operacion, self.volver_menu)
    
    def volver_menu(self):
        """Muestra de nuevo el menú principal"""
        self.frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)