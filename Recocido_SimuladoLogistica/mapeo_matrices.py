import pandas as pd
import numpy as np

# --- 1. Cargar los datos de las tiendas ---
tiendas_df = pd.read_excel('datos_distribucion_tiendas.xlsx')
nombres_nodos = tiendas_df['Nombre'].tolist()
latitudes = tiendas_df['Latitud_WGS84'].values
longitudes = tiendas_df['Longitud_WGS84'].values

print(f"Total de nodos (centros + tiendas): {len(nombres_nodos)}")
print("Primeros 5 nombres:", nombres_nodos[:5])

# --- 2. Función para calcular la distancia de Haversine (en kilómetros) ---
def haversine(lat1, lon1, lat2, lon2):
    # Convertir grados a radianes
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    # Fórmula de Haversine
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371  # Radio de la Tierra en km
    return c * r

# --- 3. Calcular la matriz de distancias ---
n = len(nombres_nodos)
distancias = np.zeros((n, n))

for i in range(n):
    for j in range(n):
        distancias[i, j] = haversine(latitudes[i], longitudes[i], latitudes[j], longitudes[j])

# --- 4. Convertir a DataFrame y asignar nombres ---
distancias_df = pd.DataFrame(distancias, index=nombres_nodos, columns=nombres_nodos)

# --- 5. Guardar la matriz de distancias ---
distancias_df.to_excel('matriz_distancias_calculada.xlsx')
print("\n✅ Matriz de distancias calculada y guardada como 'matriz_distancias_calculada.xlsx'.")

# --- 6. Imprimir una parte de la matriz para verificar ---
print("\nMatriz de distancias (primeras 5 filas y columnas):")
print(distancias_df.head())