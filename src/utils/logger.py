# src/utils/logger.py
import os
import json
import numpy as np

def save_flight_manifest(geometries, speed=5.0):
    """
    Toma las geometrías de la burbuja, calcula marcas de tiempo basadas en una velocidad constante,
    y guarda el manifiesto de vuelo en un archivo JSON.
    """
    manifest = []
    current_time = 0.0
    
    for i, geo in enumerate(geometries):
        if i > 0:
            # Calcular distancia desde el punto anterior
            dist = np.linalg.norm(geo['pos'] - geometries[i-1]['pos'])
            # Sumar el tiempo que toma recorrer esa distancia a la velocidad dada
            current_time += dist / speed
            
        # Formatear el registro para JSON (convertir tipos de numpy a tipos nativos de python)
        record = {
            "t": round(float(current_time), 2),
            "pos": [round(float(x), 2) for x in geo['pos']],
            "resistance": round(float(geo['resistance']), 4),
            "W": round(float(geo['W']), 4),
            "D": round(float(geo['D']), 4),
            "energy": round(float(geo['energy']), 4),
            "stable": bool(geo['stable'])
        }
        manifest.append(record)
        
    # Determinar ruta de guardado (src/data/outputs/)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, 'data', 'outputs')
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = os.path.join(output_dir, 'flight_manifest.json')
    
    with open(file_path, 'w') as f:
        json.dump(manifest, f, indent=4)
        
    return file_path, manifest