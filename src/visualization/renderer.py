# src/visualization/renderer.py
import numpy as np
import pyvista as pv

class Renderer:
    def __init__(self, space, manifest):
        self.space = space
        self.manifest = manifest
        
        # 1. Inicializar la ventana de PyVista
        self.plotter = pv.Plotter(window_size=(1000, 800))
        self.plotter.set_background('black')
        self.plotter.add_axes()
        
        self.plotter.camera.position = (150, 150, 150)
        self.plotter.camera.focal_point = (50, 50, 50)
        
        # Variables de estado
        self.frame_index = 0
        self.is_playing = True
        
        # Calcular mínimos y máximos para escalar colores y tamaños de forma exagerada
        energies = [d['energy'] for d in self.manifest]
        Ws = [d['W'] for d in self.manifest]
        self.min_energy = min(energies)
        self.max_energy = max(energies) or 1.0
        self.min_W = min(Ws)
        self.max_W = max(Ws) or 1.0
        
        # 2. Construir el entorno estático
        self._draw_environment()
        self._draw_route()
        
        # 3. Crear la burbuja de warp (Elemento dinámico)
        # Usamos un radio base pequeño y la creamos en el origen
        self.bubble_mesh = pv.Sphere(radius=2, center=(0, 0, 0))
        # IMPORTANTE: No le damos color aquí, lo controlaremos por código
        self.bubble_actor = self.plotter.add_mesh(self.bubble_mesh, opacity=0.8, smooth_shading=True)
        # Forzar el color inicial usando la API de PyVista
        self.bubble_actor.prop.color = (0, 1, 0) # Verde inicial
        self.bubble_actor.position = manifest[0]['pos']
        
        # 4. Interfaz de usuario (Texto y Botón)
        self.text_actor = self.plotter.add_text("Iniciando...", position=(0.02, 0.85), 
                                                font_size=12, color='white')
        
        self.plotter.add_checkbox_button_widget(self._restart_animation, 
                                               position=(10, 10), size=30, 
                                               color_on='grey', color_off='white')
        self.plotter.add_text("Reiniciar", position=(0.02, 0.05), font_size=10, color='white')

        # 5. Configurar el bucle de actualización
        self.plotter.iren
        vtk_iren = self.plotter.render_window.GetInteractor()
        vtk_iren.AddObserver("TimerEvent", self._update_animation)
        vtk_iren.CreateRepeatingTimer(100)

    def _draw_environment(self):
        self.plotter.add_mesh(pv.Sphere(radius=2, center=self.space.point_a), color='blue')
        self.plotter.add_mesh(pv.Sphere(radius=2, center=self.space.point_b), color='red')
        
        for star in self.space.stars:
            self.plotter.add_mesh(pv.Sphere(radius=star.mass/20, center=(star.x, star.y, star.z)), 
                                  color='gold', smooth_shading=True)
            
        for neb in self.space.nebulas:
            self.plotter.add_mesh(pv.Sphere(radius=neb.radius, center=(neb.x, neb.y, neb.z)), 
                                  color='purple', opacity=0.2)

    def _draw_route(self):
        points = np.array([p['pos'] for p in self.manifest])
        poly = pv.MultipleLines(points=points)
        self.plotter.add_mesh(poly, color='white', line_width=3, opacity=0.5)

    def _restart_animation(self, flag):
        self.frame_index = 0
        self.is_playing = True

    def _update_animation(self, caller, event):
        if not self.is_playing:
            return
            
        if self.frame_index < len(self.manifest):
            data = self.manifest[self.frame_index]
            
            # 1. Posición 
            self.bubble_actor.position = (data['pos'][0], data['pos'][1], data['pos'][2])
            
            # 2. Escala (API PyVista) - EXAGERADA
            # Normalizamos W entre 0 y 1 usando el mínimo y máximo de la ruta
            range_W = self.max_W - self.min_W
            norm_W = (data['W'] - self.min_W) / range_W if range_W > 0 else 0
            # Multiplicador exagerado: pasa de tamaño 1x a 10x
            scale = 1.0 + (norm_W * 10.0) 
            self.bubble_actor.scale = (scale, scale, scale)
            
            # 3. Color (API PyVista) - PUROS
            range_energy = self.max_energy - self.min_energy
            norm_energy = (data['energy'] - self.min_energy) / range_energy if range_energy > 0 else 0
            # Verde puro (0, 1, 0) a Rojo puro (1, 0, 0)
            r = norm_energy
            g = 1.0 - norm_energy
            b = 0.0
            self.bubble_actor.prop.color = (r, g, b)
            
            # Depuración: Imprimir exactamente qué valores se le están dando a PyVista
            print(f"Frame {self.frame_index}: Scale={scale:.2f}, Color=({r:.2f}, {g:.2f}, {b:.2f})")
            
            # 4. Texto
            status = "ESTABLE" if data['stable'] else "INESTABLE"
            self.text_actor.SetInput(
                f"Tiempo: {data['t']:.1f}s | Resistencia: {data['resistance']:.2f}\n"
                f"Grosor (W): {data['W']:.2f} | Densidad (D): {data['D']:.2f}\n"
                f"Energía: {data['energy']:.2f} [{status}]"
            )
            
            self.frame_index += 1
            self.plotter.render()
        else:
            self.is_playing = False
            self.text_actor.SetInput("Viaje completado. \nHaz clic en 'Reiniciar' para repetir.")
            self.plotter.render()

    def animate(self):
        self.plotter.show()