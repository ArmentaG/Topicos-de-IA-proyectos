# main_pso.py

# 1. Importar librerías y funciones definidas
import numpy as np
import pyswarms as ps
# Importamos la función objetivo y los límites desde el otro archivo
from funciones_pso import funcion_objetivo, limites

# 2. Definir parámetros del PSO
# Número de partículas en el enjambre
n_particles = 30 # <-- Parámetro original
# Dimensiones de cada partícula (5 sensores * 2 coordenadas cada uno)
dimensions = 10
# Número de iteraciones
iters = 200 # <-- Parámetro original

# Parámetros del PSO (Opcional: ajustar para mejorar la búsqueda)
options = {'c1': 0.5, 'c2': 0.3, 'w':0.9} # c1: coeficiente cognitivo, c2: coeficiente social, w: inercia

# 3. Crear instancia del optimizador
# Usamos GlobalBestPSO (mejor enjambre global)
optimizer = ps.single.GlobalBestPSO(
    n_particles=n_particles,
    dimensions=dimensions,
    options=options,
    bounds=limites # Pasamos los límites calculados en funciones_pso.py
)

# 4. Ejecutar la optimización
print("Iniciando optimización PSO...")
print(f"Configuración: Partículas={n_particles}, Iteraciones={iters}")
cost, pos = optimizer.optimize(funcion_objetivo, iters=iters, verbose=True) # <-- verbose=True

# 5. Mostrar resultados
print("\n--- Resultados del PSO ---")
print(f"Mejor valor de la función objetivo (distancia promedio mínima): {cost:.6f}")
print(f"Mejor configuración de sensores (lat1, lon1, lat2, lon2, ..., lat5, lon5):")
print(pos) # Este es el vector 1D de 10 posiciones

# Opcional: Formatear la salida de la mejor configuración
mejores_sensores = pos.reshape((5, 2)) # Convertimos a matriz 5x2
print("\nMejor configuración de sensores (Latitud, Longitud):")
for i, (lat, lon) in enumerate(mejores_sensores):
    print(f"  Sensor {i+1}: ({lat:.6f}, {lon:.6f})")

print("\nOptimización completada.")
# --- Fin del archivo main_pso.py ---