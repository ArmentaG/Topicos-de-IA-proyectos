import pandas as pd
import folium

# --- 1. Cargar los datos desde el archivo Excel ---
df = pd.read_excel('datos_distribucion_tiendas.xlsx')

# --- 2. Verificar que las columnas necesarias existan ---
print("Columnas disponibles:", df.columns.tolist())

# --- 3. Crear el mapa centrado en Culiacán, Sinaloa ---
# Coordenadas de Culiacán: 24.8070° N, 107.3900° W
mapa = folium.Map(location=[24.8070, -107.3900], zoom_start=12, tiles='OpenStreetMap')

# --- 4. Agregar marcadores al mapa ---
for index, row in df.iterrows():
    lat = row['Latitud_WGS84']
    lon = row['Longitud_WGS84']
    nombre = row['Nombre']
    tipo = row['Tipo']

    # Elegir color según el tipo
    if tipo == 'Centro de Distribución':
        color = 'red'
        icono = 'info-sign'
    else:  # 'Tienda'
        color = 'blue'
        icono = 'shopping-cart'

    # Crear el marcador
    folium.Marker(
        location=[lat, lon],
        popup=f"<b>{nombre}</b><br>Tipo: {tipo}",
        icon=folium.Icon(color=color, icon=icono)
    ).add_to(mapa)

# --- 5. Guardar el mapa como archivo HTML ---
mapa.save('mapa_culiacan_tienda.html')

print("✅ Mapa generado con éxito. Abre el archivo 'mapa_culiacan_tienda.html' en tu navegador.")