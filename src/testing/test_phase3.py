# tests/test_phase3.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

import numpy as np
from environment.space import Space
from agents.path_planner import PathPlanner
from agents.bubble_optimizer import BubbleOptimizer

def run_test():
    print("--- INICIANDO PRUEBA DE FASE 3: BUBBLE OPTIMIZER ---")
    
    # 1. Inicializar espacio y trazar la ruta (Agente 1)
    space = Space()
    planner = PathPlanner(space, step_size=2.0)
    path = planner.plan()
    
    if path is None:
        print("No se pudo continuar, no hay ruta.")
        return

    # 2. Inicializar Agente 2 y optimizar la ruta
    try:
        optimizer = BubbleOptimizer()
    except FileNotFoundError as e:
        print(e)
        return
        
    print("\nOptimizando geometría de la burbuja para cada nodo de la ruta...")
    geometries = optimizer.optimize_path(path, space)
    
    # 3. Analizar resultados
    print(f"\nSe analizaron {len(geometries)} nodos de la ruta.")
    
    # Mostrar geometría en el inicio (Vacío)
    g_start = geometries[0]
    print("\n> Inicio de la ruta (Zona Vacía):")
    print(f"  Resistencia: {g_start['resistance']:.4f} | W: {g_start['W']:.4f} | D: {g_start['D']:.4f} | Energía: {g_start['energy']:.4f} | Estable: {g_start['stable']}")

    # Encontrar el nodo de mayor resistencia (Borde de Estrella)
    max_res_node = max(geometries, key=lambda x: x['resistance'])
    print("\n> Punto de mayor resistencia (Borde de Estrella):")
    print(f"  Resistencia: {max_res_node['resistance']:.4f} | W: {max_res_node['W']:.4f} | D: {max_res_node['D']:.4f} | Energía: {max_res_node['energy']:.4f} | Estable: {max_res_node['stable']}")

    # Mostrar geometría en el destino
    g_end = geometries[-1]
    print("\n> Destino:")
    print(f"  Resistencia: {g_end['resistance']:.4f} | W: {g_end['W']:.4f} | D: {g_end['D']:.4f} | Energía: {g_end['energy']:.4f} | Estable: {g_end['stable']}")

    # Validación
    unstable_count = sum(1 for g in geometries if not g['stable'])
    print(f"\nNodos inestables (la burbuja se rompería): {unstable_count}")
    
    if unstable_count == 0 and max_res_node['W'] > g_start['W']:
        print("¡ÉXITO! La IA adaptó la geometría: usó burbujas más gruesas en zonas de alta resistencia y delgadas en el vacío.")
    else:
        print("Alerta: Revisar la estabilidad de la burbuja.")

if __name__ == "__main__":
    run_test()