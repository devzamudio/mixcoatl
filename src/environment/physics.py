# src/environment/physics.py
import numpy as np
from dataclasses import dataclass
import random

@dataclass
class Star:
    x: float
    y: float
    z: float
    mass: float  # Determina la fuerza de la resistencia espacial

@dataclass
class Nebula:
    x: float
    y: float
    z: float
    density: float
    radius: float

def calculate_spatial_resistance(x, y, z, stars, nebulas):
    """
    Calcula la resistencia espacial proxy en un punto (x,y,z).
    Retorna un valor float. 0.0 es vacío profundo, >0 es resistencia.
    """
    resistance = 0.0
    
    # Influencia de las estrellas (Campo gravitacional proxy: 1/r^2)
    for star in stars:
        dx = x - star.x
        dy = y - star.y
        dz = z - star.z
        dist_sq = dx**2 + dy**2 + dz**2
        
        # Evitar división por cero si la nave está exactamente en el centro
        dist_sq = max(dist_sq, 0.1) 
        
        # La resistencia disminuye con el cuadrado de la distancia
        resistance += star.mass / dist_sq
        
    # Influencia de las nebulosas (Densidad de polvo proxy: Gaussiana)
    for nebula in nebulas:
        dx = x - nebula.x
        dy = y - nebula.y
        dz = z - nebula.z
        dist = np.sqrt(dx**2 + dy**2 + dz**2)
        
        # Si está fuera del radio de la nebulosa, no aporta resistencia
        if dist <= nebula.radius:
            # Modelo gaussiano: máxima densidad en el centro, decae hacia los bordes
            sigma = nebula.radius / 2.0
            resistance += nebula.density * np.exp(-(dist**2) / (2 * sigma**2))
            
    return resistance