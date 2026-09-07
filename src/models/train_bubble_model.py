# src/models/train_bubble_model.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
import joblib
from utils.config import BUBBLE_W_MIN, BUBBLE_W_MAX, BUBBLE_D_MIN, BUBBLE_D_MAX
from utils.metrics import is_bubble_stable, calculate_bubble_energy
from models.ann_model import create_ann_model

def generate_optimal_dataset():
    """
    Genera un dataset lineal perfecto para que la ANN aprenda sin errores.
    """
    # Simulamos 500 niveles de resistencia espacial entre 0 y 50
    S_values = np.linspace(0, 50, 500)
    
    X = [] # Entradas: Resistencia (S)
    y = [] # Salidas: [Grosor (W), Densidad (D)]
    
    print("Generando dataset de optimización lineal...")
    for S in S_values:
        # Relación lineal directa:
        # Si S=0, W=0.1, D=0.1 (Mínimo absoluto)
        # Si S=50, W=2.0, D=10.0 (Máximo absoluto)
        W = 0.1 + (S / 50.0) * 1.9
        D = 0.1 + (S / 50.0) * 9.9
            
        X.append([S])
        y.append([W, D])
        
    return np.array(X), np.array(y)

def train_and_save():
    X, y = generate_optimal_dataset()
    print(f"Dataset generado: {len(X)} muestras.")
    
    print("Entrenando la Red Neuronal...")
    model = create_ann_model()
    model.fit(X, y)
    print("Entrenamiento completado. Score R^2:", model.score(X, y))
    
    # Guardar el modelo
    save_dir = os.path.join(os.path.dirname(__file__), 'saved_models')
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, 'bubble_ann.pkl')
    joblib.dump(model, save_path)
    print(f"Modelo guardado en: {save_path}")

if __name__ == "__main__":
    train_and_save()