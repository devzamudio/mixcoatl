# src/agents/bubble_optimizer.py
import os
import numpy as np
import joblib
from utils.config import BUBBLE_W_MIN, BUBBLE_W_MAX, BUBBLE_D_MIN, BUBBLE_D_MAX
from utils.metrics import is_bubble_stable, calculate_bubble_energy

class BubbleOptimizer:
    def __init__(self):
        model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'saved_models', 'bubble_ann.pkl')
        if not os.path.exists(model_path):
            raise FileNotFoundError("Modelo ANN no encontrado. Ejecuta 'python models/train_bubble_model.py' primero.")
        self.model = joblib.load(model_path)
        print("Agente 2 (Optimizador de Burbuja) inicializado y ANN cargada.")
        
    def optimize_path(self, path, space):
        """
        Recibe la ruta del Agente 1 y devuelve la secuencia de geometrías de la burbuja.
        """
        geometries = []
        
        for pos in path:
            # 1. Consultar resistencia en el punto actual
            S = space.get_resistance(pos[0], pos[1], pos[2])
            
            # 2. Predecir parámetros óptimos con la ANN
            W_pred, D_pred = self.model.predict(np.array([[S]]))[0]
            
            # 3. Recortar a los límites físicos por seguridad (las ANN pueden extrapolar mal)
            W = np.clip(W_pred, BUBBLE_W_MIN, BUBBLE_W_MAX)
            D = np.clip(D_pred, BUBBLE_D_MIN, BUBBLE_D_MAX)
            
            # 4. Calcular métricas reales para el reporte
            energy = calculate_bubble_energy(W, D, S)
            stable = is_bubble_stable(W, D, S)
            
            geometries.append({
                'pos': pos,
                'resistance': float(S),
                'W': float(W),
                'D': float(D),
                'energy': float(energy),
                'stable': bool(stable)
            })
            
        return geometries