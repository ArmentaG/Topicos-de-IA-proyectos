# funciones_pso.py

import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist # Importamos la función para calcular distancias

# --- Carga del dataset (esto debe hacerse una vez) ---
# Usamos skiprows=1 porque la primera fila del CSV no es el encabezado real
# y la segunda fila sí contiene los nombres de las columnas.
df_datos = pd.read_csv('dataset_combinado.csv', skiprows=1)

# Extraemos las coordenadas del dataset como un array de NumPy
# Esto será más eficiente para cálculos posteriores
coordenadas_dataset = df_datos[['Latitud', 'Longitud']].values # Shape: (101, 2)

def funcion_objetivo(particulas_2d):
    """
    Función objetivo para el algoritmo PSO.
    Calcula la distancia promedio desde cada punto del dataset
    al sensor más cercano definido por cada partícula del enjambre.
    Esta función maneja un enjambre de partículas (matriz 2D).

    Args:
        particulas_2d (numpy.ndarray): Matriz 2D de shape (n_particles, 10)
                                       donde cada fila es [lat1, lon1, lat2, lon2, ..., lat5, lon5].

    Returns:
        numpy.ndarray: Vector 1D de shape (n_particles,) con los valores de fitness
                       (distancia promedio) para cada partícula. El PSO los minimiza.
    """
    n_particles = particulas_2d.shape[0]

    # Inicializar el array de fitness para todas las partículas
    fitness_values = np.zeros(n_particles)

    # Iterar sobre cada partícula individualmente
    # (Esta parte del cálculo podría vectorizarse más, pero este enfoque es más claro)
    for i in range(n_particles):
        # 1. Obtener la partícula individual (vector 1D de 10 elementos)
        particula_1d = particulas_2d[i, :] # Shape: (10,)

        # 2. Convertir la partícula 1D (10,) en una matriz de 5 pares de coordenadas (5, 2)
        sensores = particula_1d.reshape((5, 2)) # Shape: (5, 2)

        # 3. Calcular distancias entre todos los puntos del dataset y los sensores de esta partícula
        # coordenadas_dataset: (101, 2)
        # sensores: (5, 2)
        # distancias: (101, 5) -> distancia del punto i del dataset al sensor j
        distancias = cdist(coordenadas_dataset, sensores, metric='euclidean')

        # 4. Para cada punto del dataset, encontrar la distancia mínima al sensor más cercano
        # axis=1 significa que buscamos el mínimo a lo largo de las columnas (sensores)
        distancias_minimas = np.min(distancias, axis=1) # Shape: (101,)

        # 5. Calcular la distancia promedio (fitness) para esta partícula
        fitness_values[i] = np.mean(distancias_minimas)

    return fitness_values # Devolvemos un array con el fitness de cada partícula del enjambre

# --- Opcional: Función para verificar límites ---
# Es buena práctica verificar que las coordenadas generadas por PSO
# estén dentro de los límites del campo.
def verificar_limites(particula_1d, limites):
    """
    Verifica si una partícula (o un conjunto de partículas) está dentro de los límites definidos.

    Args:
        particula_1d (numpy.ndarray): Vector 1D o 2D de la(s) partícula(s).
        limites (tuple): Tupla de (minimos, maximos) para cada dimensión.

    Returns:
        numpy.ndarray: Boolean array indicando si cada dimensión está dentro de los límites.
    """
    min_pos, max_pos = limites
    dentro = np.logical_and(particula_1d >= min_pos, particula_1d <= max_pos)
    return dentro

# --- Definición de límites basados en el dataset ---
# Calculamos los límites del espacio de búsqueda a partir del dataset cargado
lat_min = df_datos['Latitud'].min()
lat_max = df_datos['Latitud'].max()
lon_min = df_datos['Longitud'].min()
lon_max = df_datos['Longitud'].max()

limites_inferiores = np.array([lat_min, lon_min] * 5) # [lat_min, lon_min, lat_min, lon_min, ...]
limites_superiores = np.array([lat_max, lon_max] * 5) # [lat_max, lon_max, lat_max, lon_max, ...]
limites = (limites_inferiores, limites_superiores)

print(f"Límites calculados del dataset:")
print(f"Latitud: [{lat_min:.6f}, {lat_max:.6f}]")
print(f"Longitud: [{lon_min:.6f}, {lon_max:.6f}]")
print(f"Límites inferiores para la partícula: {limites_inferiores}")
print(f"Límites superiores para la partícula: {limites_superiores}")

# --- Fin del archivo funciones_pso.py ---