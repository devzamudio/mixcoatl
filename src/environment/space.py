# src/environment/space.py
import random
import numpy as np
from environment.physics import Star, Nebula, calculate_spatial_resistance
from utils.config import (BOX_SIZE, NUM_STARS, NUM_NEBULAS, 
                          STAR_MASS_RANGE, NEBULA_DENSITY_RANGE, NEBULA_RADIUS_RANGE)

class Space:
    def __init__(self):
        self.bounds = (0, BOX_SIZE)
        self.stars = []
        self.nebulas = []
        self.point_a = None  # Inicio
        self.point_b = None  # Destino
        
        self._generate_environment()

    def _generate_environment(self):
        """Genera estrellas, nebulosas y los puntos A y B de forma aleatoria."""
        min_b, max_b = self.bounds
        
        # Generar Estrellas
        for _ in range(NUM_STARS):
            # Mantener un margen de los bordes
            pos = [random.uniform(min_b + 10, max_b - 10) for _ in range(3)]
            mass = random.uniform(*STAR_MASS_RANGE)
            self.stars.append(Star(pos[0], pos[1], pos[2], mass))
            
        # Generar Nebulosas
        for _ in range(NUM_NEBULAS):
            pos = [random.uniform(min_b + 10, max_b - 10) for _ in range(3)]
            density = random.uniform(*NEBULA_DENSITY_RANGE)
            radius = random.uniform(*NEBULA_RADIUS_RANGE)
            self.nebulas.append(Nebula(pos[0], pos[1], pos[2], density, radius))
            
        # Generar Punto A y B (en extremos opuestos de la caja para asegurar un viaje largo)
        self.point_a = np.array([0.0, random.uniform(min_b, max_b), random.uniform(min_b, max_b)])
        self.point_b = np.array([float(max_b), random.uniform(min_b, max_b), random.uniform(min_b, max_b)])

    def get_resistance(self, x, y, z):
        """Wrapper para consultar la resistencia en un punto específico."""
        return calculate_spatial_resistance(x, y, z, self.stars, self.nebulas)

    def is_valid_position(self, x, y, z):
        """Verifica si una posición no está dentro del radio crítico de una estrella (burbuja rota)."""
        for star in self.stars:
            dist = np.sqrt((x - star.x)**2 + (y - star.y)**2 + (z - star.z)**2)
            # Radio crítico arbitrario: la masa indica cuánto "espacio" deforma gravitacionalmente
            critical_radius = np.cbrt(star.mass) / 2.0 
            if dist < critical_radius:
                return False # La burbuja se rompería instantáneamente
        return True