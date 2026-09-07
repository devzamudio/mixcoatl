# src/utils/metrics.py
import numpy as np
from utils.config import RESISTANCE_WEIGHT, BUBBLE_W_MIN, BUBBLE_W_MAX, BUBBLE_D_MIN, BUBBLE_D_MAX

def calculate_step_cost(pos1, pos2, space):
    """
    Calcula el costo energético de moverse de pos1 a pos2.
    pos1, pos2: Arrays numpy [x, y, z]
    space: Instancia de la clase Space
    """
    # 1. Distancia euclidiana (costo base de moverse)
    distance = np.linalg.norm(pos2 - pos1)
    
    # 2. Resistencia espacial promedio en el segmento
    # Para simplificar, tomamos la resistencia en el punto de destino.
    # (En una versión más avanzada se podría promediar varios puntos a lo largo del vector)
    resistance = space.get_resistance(pos2[0], pos2[1], pos2[2])
    
    # 3. Cálculo del Costo Total
    # Si la resistencia es alta, el costo se dispara. 
    # Fórmula: Distancia * (1 + Peso * Resistencia)
    cost = distance * (1.0 + (RESISTANCE_WEIGHT * resistance))
    
    return cost

def is_bubble_stable(W, D, S):
    """
    Determina si la burbuja sobrevive a la resistencia espacial.
    Regla proxy: La estabilidad requiere que el producto de Grosor (W) y Densidad (D) 
    sea mayor o igual a la Resistencia (S) dividida por un factor de escala.
    """
    # Factor de escala para que los rangos de S (0-50) encajen con W (0.1-2.0) y D (0.1-10.0)
    stability_threshold = S / 5.0 
    return (W * D) >= stability_threshold

def calculate_bubble_energy(W, D, S):
    """
    Calcula el costo energético de mantener una burbuja con parámetros [W, D] 
    en un entorno con resistencia S.
    """
    # Energía proporcional al Grosor (W) y la Densidad (D).
    # A mayor resistencia (S), más energía se necesita solo para mantenerla estable.
    energy = (W * 10.0) + (D * 10.0) + (S * 2.0)
    return energy