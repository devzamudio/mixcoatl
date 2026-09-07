# src/utils/config.py

# --- Parámetros del Espacio ---
BOX_SIZE = 100.0          # Tamaño de la caja 3D (100x100x100 unidades)
GRID_RESOLUTION = 2.0     # Distancia entre nodos de la cuadrícula (para discretizar el espacio)

# --- Parámetros de Obstáculos ---
NUM_STARS = 3             # Número de estrellas
NUM_NEBULAS = 2           # Número de nebulosas
STAR_MASS_RANGE = (50.0, 100.0)   # Masa proxy de las estrellas (determina su radio de influencia)
NEBULA_DENSITY_RANGE = (10.0, 30.0) # Densidad proxy de las nebulosas
NEBULA_RADIUS_RANGE = (15.0, 25.0) # Radio físico de las nebulosas

# --- Parámetros de la Burbuja de Warp (Agentes futuros) ---
BUBBLE_R_MIN = 1.0
BUBBLE_R_MAX = 5.0
BUBBLE_W_MIN = 0.1
BUBBLE_W_MAX = 2.0
BUBBLE_D_MIN = 0.1
BUBBLE_D_MAX = 10.0

# --- Hiperparámetros de Costos ---
# Ponderación de la resistencia espacial vs la distancia en el cálculo de energía
RESISTANCE_WEIGHT = 0.1