# src/models/ann_model.py
from sklearn.neural_network import MLPRegressor

def create_ann_model():
    """
    Crea una Red Neuronal Artificial (ANN) simple.
    Entrada: 1 característica (Resistencia Espacial S)
    Salida: 2 características (Grosor W, Densidad D)
    """
    # Usamos 2 capas ocultas de 32 y 16 neuronas. Función de activación ReLU.
    model = MLPRegressor(
        hidden_layer_sizes=(32, 16),
        activation='relu',
        solver='adam',
        max_iter=2000,
        random_state=42
    )
    return model