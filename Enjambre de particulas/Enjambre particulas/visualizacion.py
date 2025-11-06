# visualizacion.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Cargar el dataset original ---
# Usamos skiprows=1 porque la primera fila del CSV no es el encabezado real
df_datos = pd.read_csv('dataset_combinado.csv', skiprows=1)

# Extraemos las coordenadas del dataset
coordenadas_dataset = df_datos[['Latitud', 'Longitud']].values
cultivos_dataset = df_datos['Cultivo']

# --- Datos de ejemplo: Reemplaza estos valores con la salida de main_pso.py ---
# Supongamos que después de correr main_pso.py, obtuviste algo como esto:
# cost: 0.025432
# pos: [ 25.551234 -108.498765  25.598765 -108.451234  25.532109 -108.465432
#        25.610987 -108.501234  25.575432 -108.439876]
# Copia y pega aquí el vector 'pos' real que obtuviste.
# Asegúrate de que sea un array de NumPy de 10 elementos.
# Si copias la salida directamente de la consola, puede incluir 'array([...])'.
# En ese caso, copia solo los números dentro de los corchetes.
# Ejemplo de cómo debería ser:
mejor_configuracion_pos = np.array([
25.54158755, -108.50214587,   25.54344773, -108.45333497,   25.56144224,
 -108.46127455,   25.61390248, -108.47067501,   25.59272325, -108.50153785
])

# Verificar que la configuración tenga la forma correcta (10,)
if mejor_configuracion_pos.shape != (10,):
    print(f"Error: mejor_configuracion_pos tiene forma {mejor_configuracion_pos.shape}, se esperaba (10,)")
    exit()

# Convertir la configuración de 1D (10,) a 2D (5, 2) para los sensores
sensores_optimos = mejor_configuracion_pos.reshape((5, 2))

print("Configuración de sensores óptimos cargada:")
print(sensores_optimos)

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
scatter_sensores = plt.scatter(sensores_optimos[:, 1], sensores_optimos[:, 0], # [lon, lat]
                               marker='*', s=200, c='red', edgecolors='black', 
                               linewidth=1.5, label='Sensores Optimizados (PSO)')

plt.xlabel('Longitud')
plt.ylabel('Latitud')
plt.title('Optimización de Ubicación de Sensores (N=5) - PSO\n'
          'Puntos de Muestreo (Coloreados por Cultivo) y Sensores Optimizados')

# Opcional: Añadir etiquetas a los sensores
for i, (lat, lon) in enumerate(sensores_optimos):
    plt.annotate(f'S{i+1}', (lon, lat), textcoords="offset points", 
                 xytext=(5,-10), ha='center', fontsize=10, color='red', weight='bold')

plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

print("\nVisualización completada.")