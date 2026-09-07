# src/agents/path_planner.py
import heapq
import numpy as np
from utils.config import BOX_SIZE
from utils.metrics import calculate_step_cost

class PathPlanner:
    def __init__(self, space, step_size=2.0):
        """
        Inicializa el planificador de rutas.
        :param space: Instancia de la clase Space (el entorno).
        :param step_size: Resolución de la cuadrícula de búsqueda (ej. 2.0 unidades).
        """
        self.space = space
        self.step_size = step_size
        self.min_bound = 0.0
        self.max_bound = BOX_SIZE
        
        # Convertir puntos A y B a índices de la cuadrícula
        self.start_idx = self._to_grid_idx(space.point_a)
        self.goal_idx = self._to_grid_idx(space.point_b)
        self.goal_pos = space.point_b

    def _to_grid_idx(self, pos):
        """Convierte coordenadas continuas (x,y,z) a índices de la cuadrícula."""
        pos_clamped = np.clip(pos, self.min_bound, self.max_bound)
        return tuple((pos_clamped / self.step_size).astype(int))

    def _to_continuous_pos(self, idx):
        """Convierte índices de la cuadrícula de vuelta a coordenadas continuas."""
        return np.array(idx) * self.step_size

    def _get_neighbors(self, idx):
        """Obtiene los 26 vecinos en un espacio 3D (incluyendo diagonales)."""
        neighbors = []
        # Movimientos en 3D: -1, 0, 1 en cada eje
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    if dx == 0 and dy == 0 and dz == 0:
                        continue # Es el nodo actual
                    
                    new_idx = (idx[0] + dx, idx[1] + dy, idx[2] + dz)
                    new_pos = self._to_continuous_pos(new_idx)
                    
                    # 1. Verificar límites de la caja
                    if np.any(new_pos < self.min_bound) or np.any(new_pos > self.max_bound):
                        continue
                    
                    # 2. Verificar colisiones (si está dentro de una estrella, se descarta)
                    if not self.space.is_valid_position(new_pos[0], new_pos[1], new_pos[2]):
                        continue
                        
                    neighbors.append((new_idx, new_pos))
        return neighbors

    def _heuristic(self, pos):
        """
        Heurística para A*: Estima el costo restante al destino.
        Usamos distancia euclidiana. Es admisible porque la resistencia (>=0) 
        solo puede aumentar el costo real, nunca reducirlo por debajo de la distancia física.
        """
        return np.linalg.norm(pos - self.goal_pos)

    def plan(self):
        """Ejecuta el algoritmo A* y devuelve la ruta como una lista de coordenadas [x,y,z]."""
        open_set = []
        # Cola de prioridad: (f_score, contador, nodo_idx)
        # El contador evita errores si dos f_scores son iguales al comparar arrays.
        counter = 0 
        start_h = self._heuristic(self.space.point_a)
        heapq.heappush(open_set, (start_h, counter, self.start_idx))
        
        came_from = {}
        g_score = {self.start_idx: 0.0}
        
        print("Iniciando búsqueda A*...")
        
        while open_set:
            current_f, _, current_idx = heapq.heappop(open_set)
            current_pos = self._to_continuous_pos(current_idx)
            
            # Condición de llegada (si estamos a un paso del objetivo)
            if np.linalg.norm(current_pos - self.goal_pos) <= self.step_size * 1.5:
                print("¡Ruta encontrada!")
                return self._reconstruct_path(came_from, current_idx)
            
            for neighbor_idx, neighbor_pos in self._get_neighbors(current_idx):
                # Costo real de llegar al vecino desde el inicio
                step_cost = calculate_step_cost(current_pos, neighbor_pos, self.space)
                tentative_g = g_score[current_idx] + step_cost
                
                if tentative_g < g_score.get(neighbor_idx, float('inf')):
                    # Este camino es mejor que cualquier anterior
                    came_from[neighbor_idx] = current_idx
                    g_score[neighbor_idx] = tentative_g
                    f_score = tentative_g + self._heuristic(neighbor_pos)
                    counter += 1
                    heapq.heappush(open_set, (f_score, counter, neighbor_idx))
                    
        print("No se encontró una ruta válida.")
        return None

    def _reconstruct_path(self, came_from, current_idx):
        """Reconstruye la ruta desde el objetivo hasta el inicio."""
        path = [self._to_continuous_pos(current_idx)]
        while current_idx in came_from:
            current_idx = came_from[current_idx]
            path.append(self._to_continuous_pos(current_idx))
        path.reverse()
        
        # Forzar el último punto para que sea exactamente el Punto B definido
        path[-1] = self.goal_pos
        return path