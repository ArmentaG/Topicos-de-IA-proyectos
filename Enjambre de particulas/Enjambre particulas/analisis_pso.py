# analisis_pso.py

# 1. Importar librerías y funciones definidas
import numpy as np
import pyswarms as ps
import matplotlib.pyplot as plt
# Importamos la función objetivo y los límites desde el otro archivo
from funciones_pso import funcion_objetivo, limites

# 2. Definir parámetros del PSO
n_particles = 30
dimensions = 10
iters = 200 # Puedes usar el mismo número que en main_pso.py

options = {'c1': 0.5, 'c2': 0.3, 'w':0.9}

# 3. Crear instancia del optimizador
optimizer = ps.single.GlobalBestPSO(
    n_particles=n_particles,
    dimensions=dimensions,
    options=options,
    bounds=limites
)

# 4. Ejecutar la optimización y capturar historial
print("Iniciando optimización PSO...")
print(f"Configuración: Partículas={n_particles}, Iteraciones={iters}")

# La función optimize devuelve el mejor costo y la mejor posición
# También captura internamente el historial en el objeto optimizer
best_cost, best_pos = optimizer.optimize(funcion_objetivo, iters=iters, verbose=True)

# 5. Mostrar resultados finales
print("\n--- Resultados del PSO ---")
# Usamos best_cost en lugar de optimizer.best_cost
print(f"Mejor valor de la función objetivo (distancia promedio mínima): {best_cost:.6f}")
# Usamos best_pos en lugar de optimizer.pos_history[-1]
print(f"Mejor configuración de sensores (lat1, lon1, lat2, lon2, ..., lat5, lon5):")
print(best_pos)
pos_final = best_pos # Renombramos para consistencia

# Formatear la salida de la mejor configuración
mejores_sensores = pos_final.reshape((5, 2))
print("\nMejor configuración de sensores (Latitud, Longitud):")
for i, (lat, lon) in enumerate(mejores_sensores):
    print(f"  Sensor {i+1}: ({lat:.6f}, {lon:.6f})")

print("\nOptimización completada.")

# 6. Visualización del historial de fitness
plt.figure(figsize=(10, 6))
plt.plot(optimizer.cost_history, label='Mejor Fitness Global por Iteración')
plt.xlabel('Iteración')
plt.ylabel('Valor de la Función Objetivo (Distancia Promedio)')
plt.title('Evolución del Fitness durante la Optimización PSO')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

# Opcional: Visualización de la evolución promedio del fitness del enjambre
# (Puede ser menos informativa que el mejor global, pero da otra perspectiva)
plt.figure(figsize=(10, 6))
plt.plot(optimizer.mean_pbest_history, label='Fitness Promedio del Enjambre', alpha=0.7)
plt.xlabel('Iteración')
plt.ylabel('Valor Promedio de la Función Objetivo')
plt.title('Evolución del Fitness Promedio del Enjambre PSO')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

print("\nAnálisis de evolución completado.")

# --- Opcional: Llamar a la visualización de resultados ---
# Este bloque intenta importar y usar el código de visualizacion.py
# para mostrar la ubicación final de los sensores.
# Asegúrate de que visualizacion.py esté en la misma carpeta.
# Este bloque puede fallar si visualizacion.py no está bien formateado
# o si no se puede importar correctamente.

try:
    import sys
    # Asegura que Python busque en el directorio actual
    sys.path.append('.')

    # Importar las librerías necesarias en este contexto
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    # Cargar el dataset original
    df_datos = pd.read_csv('dataset_combinado.csv', skiprows=1)

    print("\nGenerando visualización de resultados...")

    # --- Visualización ---
    plt.figure(figsize=(12, 10))

    # Graficar puntos de muestreo coloreados por Cultivo
    scatter_datos = plt.scatter(df_datos['Longitud'], df_datos['Latitud'],
                                c=pd.Categorical(df_datos['Cultivo']).codes,
                                cmap='viridis', alpha=0.6, edgecolors='w', s=50,
                                label='Puntos de Muestreo')

    # Crear una leyenda basada en los cultivos
    handles_datos, _ = scatter_datos.legend_elements()
    labels_datos = pd.Categorical(df_datos['Cultivo']).categories
    legend_datos = plt.legend(handles_datos, labels_datos, title="Cultivo",
                              loc="upper left", bbox_to_anchor=(0.02, 0.98))
    plt.gca().add_artist(legend_datos) # Para que la leyenda de cultivo no se sobreescriba

    # Graficar sensores optimizados
    # Usamos una estrella grande y de color distinto
    scatter_sensores = plt.scatter(mejores_sensores[:, 1], mejores_sensores[:, 0], # [lon, lat]
                                   marker='*', s=200, c='red', edgecolors='black',
                                   linewidth=1.5, label='Sensores Optimizados (PSO)')

    plt.xlabel('Longitud')
    plt.ylabel('Latitud')
    plt.title('Optimización de Ubicación de Sensores (N=5) - PSO\n'
              'Puntos de Muestreo (Coloreados por Cultivo) y Sensores Optimizados')

    # Opcional: Añadir etiquetas a los sensores
    for i, (lat, lon) in enumerate(mejores_sensores):
        plt.annotate(f'S{i+1}', (lon, lat), textcoords="offset points",
                     xytext=(5,-10), ha='center', fontsize=10, color='red', weight='bold')

    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

    print("\nVisualización de resultados completada.")
except ImportError as e:
    print(f"\nAdvertencia: No se pudo importar visualizacion.py o sus dependencias: {e}")
    print("Puedes ejecutar 'visualizacion.py' manualmente con el siguiente vector 'pos':")
    print(f"pos = {pos_final.tolist()}")
except Exception as e:
    print(f"\nError inesperado al generar la visualización: {e}")
    print("Puedes ejecutar 'visualizacion.py' manualmente con el siguiente vector 'pos':")
    print(f"pos = {pos_final.tolist()}")


# --- Fin del archivo analisis_pso.py ---