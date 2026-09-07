# tests/test_phase1.py (Ejecutar desde la carpeta /src)
import sys
import os
# Añadir la carpeta src al path para que los imports funcionen
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

import numpy as np
from environment.space import Space
from utils.metrics import calculate_step_cost

def run_test():
    print("--- INICIANDO PRUEBA DE FASE 1 ---")
    
    # 1. Inicializar el espacio
    space = Space()
    
    print(f"Punto A (Inicio): {space.point_a}")
    print(f"Punto B (Destino): {space.point_b}")
    print(f"Estrellas generadas: {len(space.stars)}")
    print(f"Nebulosas generadas: {len(space.nebulas)}")
    
    # 2. Calcular resistencia en el Punto A
    res_A = space.get_resistance(space.point_a[0], space.point_a[1], space.point_a[2])
    print(f"Resistencia espacial en Punto A: {res_A:.4f} (Debería ser baja, cerca del vacío)")
    
    # 3. Simular dos rutas hacia el punto B
    
    # Ruta 1: Línea recta
    print("\nCalculando Ruta 1 (Línea Recta)...")
    cost_straight = 0.0
    steps = 10
    for i in range(1, steps + 1):
        t = i / steps
        current_pos = space.point_a * (1 - t) + space.point_b * t
        prev_pos = space.point_a * (1 - (t - 1/steps)) + space.point_b * (t - 1/steps)
        cost_straight += calculate_step_cost(prev_pos, current_pos, space)
    print(f"Costo total Ruta 1: {cost_straight:.2f}")
    
    # Ruta 2: Desvío arbitrario por el centro de la caja (para ver si cambian los costos)
    print("\nCalculando Ruta 2 (Desvío)...")
    waypoint = np.array([50.0, 50.0, 50.0])
    cost_detour = 0.0
    
    # Tramo A -> Waypoint
    for i in range(1, steps + 1):
        t = i / steps
        current_pos = space.point_a * (1 - t) + waypoint * t
        prev_pos = space.point_a * (1 - (t - 1/steps)) + waypoint * (t - 1/steps)
        cost_detour += calculate_step_cost(prev_pos, current_pos, space)
        
    # Tramo Waypoint -> B
    for i in range(1, steps + 1):
        t = i / steps
        current_pos = waypoint * (1 - t) + space.point_b * t
        prev_pos = waypoint * (1 - (t - 1/steps)) + space.point_b * (t - 1/steps)
        cost_detour += calculate_step_cost(prev_pos, current_pos, space)
        
    print(f"Costo total Ruta 2: {cost_detour:.2f}")
    
    print("\n--- PRUEBA FINALIZADA ---")
    print("Si los costos varían y la resistencia funciona, la Fase 1 es un éxito.")

if __name__ == "__main__":
    run_test()