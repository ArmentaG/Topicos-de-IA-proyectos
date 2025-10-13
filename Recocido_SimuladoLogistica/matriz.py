import pandas as pd

# Cargar la matriz de distancias
distancias = pd.read_excel('matriz_distancias.xlsx', index_col=0)

print("Matriz de distancias:")
print(f"Forma: {distancias.shape}")
print("\nPrimeras 10 filas y columnas:")
print(distancias.iloc[:10, :10])  # Mostrar solo una parte para ver la estructura

print("\nÍndices (filas y columnas):")
print(distancias.index.tolist())

# Verificar si es simétrica (opcional, pero útil)
es_simetrica = distancias.equals(distancias.T)
print(f"\n¿La matriz es simétrica? {es_simetrica}")

# Cargar también el archivo de tiendas para comparar índices
tiendas_df = pd.read_excel('datos_distribucion_tiendas.xlsx')
print("\nNombres de tiendas/centros del archivo de datos:")
print(tiendas_df['Nombre'].tolist())

# Verificar si los índices de la matriz coinciden con los nombres del archivo
nombres_en_datos = set(tiendas_df['Nombre'])
nombres_en_distancias = set(distancias.index)

coinciden = nombres_en_datos == nombres_en_distancias
print(f"\n¿Los nombres en el archivo de datos coinciden con los índices de la matriz de distancias? {coinciden}")