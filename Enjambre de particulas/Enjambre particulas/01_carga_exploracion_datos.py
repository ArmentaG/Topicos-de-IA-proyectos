import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Cargar los datos desde el archivo CSV
print("Cargando datos desde 'datos_cultivos.csv'...")
try:
    # Usar skiprows=1 para saltar la primera fila (0,1,2,3,4,5,6)
    # y usar la siguiente fila (la real) como encabezado.
    # Además, especificamos header=0 para indicar que el encabezado está en la nueva primera fila.
    df = pd.read_csv('dataset_combinado.csv', skiprows=1)
    print("Datos cargados exitosamente.")
    print(f"Encabezado real detectado: {list(df.columns)}") # Mostrar los encabezados
except FileNotFoundError:
    print("Error: No se encontró el archivo 'datos_cultivos.csv'. Asegúrate de que esté en la misma carpeta que este script.")
    exit() # Termina el script si no encuentra el archivo

# 2. Explorar los datos
print("\n--- Información del Dataset ---")
print(df.info())

print("\n--- Primeras filas del Dataset ---")
print(df.head())

print("\n--- Estadísticas descriptivas ---")
print(df.describe())

print("\n--- Valores únicos por columna ---")
for col in df.columns:
    print(f"{col}: {df[col].unique()}")

print("\n--- Conteo de cultivos ---")
print(df['Cultivo'].value_counts())

# 3. Visualización
print("\nGenerando visualización...")
plt.figure(figsize=(10, 8))

# Graficar puntos de muestreo coloreados por Cultivo
scatter = plt.scatter(df['Longitud'], df['Latitud'], c=pd.Categorical(df['Cultivo']).codes, cmap='viridis', alpha=0.7, edgecolors='w', s=50)
plt.xlabel('Longitud')
plt.ylabel('Latitud')
plt.title('Distribución de Puntos de Muestreo por Cultivo en Guasave')

# Crear una leyenda basada en los cultivos
handles, _ = scatter.legend_elements()
labels = pd.Categorical(df['Cultivo']).categories
legend1 = plt.legend(handles, labels, title="Cultivo", loc="best", bbox_to_anchor=(1, 1))
plt.gca().add_artist(legend1) # Para que la leyenda de cultivo no se sobreescriba con la de humedad si se agrega

# Opcional: colorear por Humedad
# plt.figure(figsize=(10, 8))
# scatter2 = plt.scatter(df['Longitud'], df['Latitud'], c=df['Humedad (%)'], cmap='Blues', alpha=0.7, edgecolors='w', s=50)
# plt.colorbar(scatter2, label='Humedad (%)')
# plt.xlabel('Longitud')
# plt.ylabel('Latitud')
# plt.title('Distribución de Humedad en el Campo')

plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

print("\nVisualización completada.")