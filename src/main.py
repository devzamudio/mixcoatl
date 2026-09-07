# src/main.py
import os
import sys
# Añadir la carpeta actual al path por si se ejecuta directamente
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from environment.space import Space
from agents.path_planner import PathPlanner
from agents.bubble_optimizer import BubbleOptimizer
import utils.logger as logger
from visualization.renderer import Renderer

def main():
    print("======================================================")
    print(" SISTEMA MULTIAGENTE MIXCÓATL - INICIANDO SECUENCIA ")
    print("======================================================\n")
    
    # 1. Inicializar entorno estelar
    print("[1/4] Generando entorno estelar...")
    space = Space()
    print(f"      Punto A: {space.point_a}")
    print(f"      Punto B: {space.point_b}\n")
    
    # 2. Agente 1: Planificación de ruta (A*)
    print("[2/4] Agente 1: Trazando ruta de mínima energía...")
    planner = PathPlanner(space, step_size=2.0)
    path = planner.plan()
    
    if path is None:
        print("Error: No se encontró una ruta viable. Abortando misión.")
        return
        
    print(f"      Ruta trazada con {len(path)} nodos.\n")
    
    # 3. Agente 2: Optimización de burbuja (ANN)
    print("[3/4] Agente 2: Optimizando geometría de burbuja de warp...")
    try:
        optimizer = BubbleOptimizer()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
        
    geometries = optimizer.optimize_path(path, space)
    print("      Geometrías calculadas para cada segmento.\n")
    
    # 4. Orquestación: Generar manifiesto
    print("[4/4] Generando manifiesto de vuelo temporal...")
    json_path, manifest = logger.save_flight_manifest(geometries, speed=5.0)
    
    # Resumen final
    total_energy = sum(g['energy'] for g in geometries)
    unstable_nodes = sum(1 for g in geometries if not g['stable'])
    total_time = manifest[-1]['t']
    
    print("\n======================================================")
    print(" RESUMEN DEL VUELO ")
    print("======================================================")
    print(f"Tiempo total de viaje: {total_time:.2f} segundos simulados")
    print(f"Energía total consumida: {total_energy:.2f} unidades")
    print(f"Nodos inestables (burbuja rota): {unstable_nodes} / {len(geometries)}")
    print(f"Manifiesto completo guardado en: {json_path}")
    print("======================================================")
    
    # 5. Visualización 3D
    print("\nIniciando visualización 3D...")
    print("(Cierra la ventana de Matplotlib para terminar el programa)")
    renderer = Renderer(space, manifest)
    renderer.animate()

if __name__ == "__main__":
    main()