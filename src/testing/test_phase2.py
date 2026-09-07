# tests/test_phase2.py
import sys
import os
# Añadir la carpeta src al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

import numpy as np
from environment.space import Space
from agents.path_planner import PathPlanner

def run_test():
    print("--- INICIANDO PRUEBA DE FASE 2: PATH PLANNER (A*) ---")
    
    # 1. Inicializar el espacio
    space = Space()
    print(f"Punto A: {space.point_a}")
    print(f"Punto B: {space.point_b}")
    
    # Mostrar dónde están las estrellas para entender el entorno
    for i, star in enumerate(space.stars):
        print(f"Estrella {i+1} en: ({star.x:.1f}, {star.y:.1f}, {star.z:.1f}) con masa {star.mass:.1f}")
        
    # 2. Inicializar y ejecutar el Path Planner
    planner = PathPlanner(space, step_size=2.0)
    path = planner.plan()
    
    if path is None:
        print("El algoritmo no logró encontrar una ruta.")
        return

    # 3. Analizar la ruta resultante
    print(f"\nRuta encontrada con {len(path)} nodos.")
    print("Primeros 3 nodos de la ruta:")
    for p in path[:3]:
        print(f"  - [{p[0]:.2f}, {p[1]:.2f}, {p[2]:.2f}]")
    print("Últimos 3 nodos de la ruta:")
    for p in path[-3:]:
        print(f"  - [{p[0]:.2f}, {p[1]:.2f}, {p[2]:.2f}]")
        
    # 4. Validación de seguridad: ¿La ruta atraviesa alguna estrella?
    print("\nValidando seguridad de la ruta...")
    invalid_nodes = 0
    max_resistance_on_path = 0.0
    
    for pos in path:
        if not space.is_valid_position(pos[0], pos[1], pos[2]):
            invalid_nodes += 1
        res = space.get_resistance(pos[0], pos[1], pos[2])
        if res > max_resistance_on_path:
            max_resistance_on_path = res
            
    print(f" - Nodos de la ruta dentro de una zona crítica (estrella): {invalid_nodes}")
    print(f" - Resistencia espacial máxima en la ruta: {max_resistance_on_path:.4f}")
    
    if invalid_nodes == 0:
        print("¡ÉXITO! La IA esquivó las estrellas correctamente.")
    else:
        print("ALERTA: La ruta atraviesa zonas donde la burbuja se rompería.")

if __name__ == "__main__":
    run_test()