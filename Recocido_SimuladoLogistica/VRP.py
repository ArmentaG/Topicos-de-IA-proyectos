import pandas as pd
import numpy as np
import random
import math
import folium

# --- 1. FUNCIONES AUXILIARES ---

def haversine(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia entre dos puntos en kilómetros usando la fórmula de Haversine.
    """
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371  # Radio de la Tierra en km
    return c * r

# --- 2. CLASE VRP (PARA DISTANCIAS) ---

class VRP:
    def __init__(self, distancias_df):
        """
        Inicializa el problema VRP.
        :param distancias_df: DataFrame de pandas con la matriz de distancias.
        """
        self.distancias_df = distancias_df
        self.nodos = distancias_df.index.tolist()
        self.nombre_a_indice = {nombre: i for i, nombre in enumerate(self.nodos)}
        self.centros = [nombre for nombre in self.nodos if "Centro de Distribución" in nombre]
        self.tiendas = [nombre for nombre in self.nodos if "Tienda" in nombre]
        self.dist_matrix = distancias_df.values

    def calcular_costo_ruta(self, ruta):
        """
        Calcula la distancia total de una ruta dada.
        """
        costo_total = 0
        for i in range(len(ruta) - 1):
            nodo_origen = ruta[i]
            nodo_destino = ruta[i+1]
            indice_origen = self.nombre_a_indice[nodo_origen]
            indice_destino = self.nombre_a_indice[nodo_destino]
            costo_total += self.dist_matrix[indice_origen][indice_destino]
        return costo_total

    def calcular_costo_solucion(self, solucion):
        """
        Calcula el costo total de una solución completa (lista de rutas).
        """
        costo_total = 0
        for ruta in solucion:
            costo_total += self.calcular_costo_ruta(ruta)
        return costo_total

    def generar_solucion_inicial(self, centro_inicio):
        """
        Genera una solución inicial factible usando Nearest Neighbor.
        """
        tiendas_no_visitadas = self.tiendas.copy()
        rutas = []

        while tiendas_no_visitadas:
            ruta_actual = [centro_inicio]
            nodo_actual = centro_inicio

            while tiendas_no_visitadas:
                nodo_actual_indice = self.nombre_a_indice[nodo_actual]
                distancias_desde_actual = self.dist_matrix[nodo_actual_indice]

                tienda_mas_cercana = None
                distancia_minima = float('inf')

                for tienda in tiendas_no_visitadas:
                    tienda_indice = self.nombre_a_indice[tienda]
                    distancia = distancias_desde_actual[tienda_indice]
                    if distancia < distancia_minima:
                        distancia_minima = distancia
                        tienda_mas_cercana = tienda

                if tienda_mas_cercana:
                    ruta_actual.append(tienda_mas_cercana)
                    tiendas_no_visitadas.remove(tienda_mas_cercana)
                    nodo_actual = tienda_mas_cercana
                else:
                    break

            ruta_actual.append(centro_inicio)
            rutas.append(ruta_actual)

        return rutas

    def generar_solucion_aleatoria(self, centro_inicio):
        """
        Genera una solución inicial aleatoria.
        :param centro_inicio: Nombre del centro de distribución para iniciar la ruta.
        :return: Lista de rutas (cada ruta es una lista de nombres de nodos).
        """
        tiendas_no_visitadas = self.tiendas.copy()
        random.shuffle(tiendas_no_visitadas)

        ruta_actual = [centro_inicio] + tiendas_no_visitadas + [centro_inicio]
        return [ruta_actual]

    def generar_vecino(self, solucion_actual):
        """
        Genera una solución vecina usando varios tipos de movimientos.
        """
        nueva_solucion = [ruta[:] for ruta in solucion_actual]

        ruta1_idx = random.randint(0, len(nueva_solucion) - 1)
        ruta1 = nueva_solucion[ruta1_idx]

        if len(ruta1) > 3:
            tienda1_idx = random.randint(1, len(ruta1) - 2)
            tienda2_idx = random.randint(1, len(ruta1) - 2)
            if tienda1_idx != tienda2_idx:
                nueva_solucion[ruta1_idx][tienda1_idx], nueva_solucion[ruta1_idx][tienda2_idx] = \
                    nueva_solucion[ruta1_idx][tienda2_idx], nueva_solucion[ruta1_idx][tienda1_idx]
                return nueva_solucion

        if len(nueva_solucion) > 1:
            ruta2_idx = random.randint(0, len(nueva_solucion) - 1)
            while ruta2_idx == ruta1_idx:
                ruta2_idx = random.randint(0, len(nueva_solucion) - 1)
            ruta2 = nueva_solucion[ruta2_idx]

            if len(ruta1) > 2 and len(ruta2) > 2:
                tienda1_idx = random.randint(1, len(ruta1) - 2)
                tienda2_idx = random.randint(1, len(ruta2) - 2)

                tienda_a_mover = nueva_solucion[ruta1_idx].pop(tienda1_idx)
                nueva_solucion[ruta2_idx].insert(tienda2_idx, tienda_a_mover)
                return nueva_solucion

        if len(ruta1) > 4:
            start_idx = random.randint(1, len(ruta1) - 3)
            end_idx = random.randint(start_idx + 1, len(ruta1) - 2)
            nueva_solucion[ruta1_idx][start_idx:end_idx+1] = reversed(nueva_solucion[ruta1_idx][start_idx:end_idx+1])
            return nueva_solucion

        return nueva_solucion

# --- 3. ALGORITMO DE RECOCIDO SIMULADO (PARA DISTANCIAS) ---

def simulated_annealing(vrp_instance, solucion_inicial, T_inicial=50000, T_final=0.00001, enfriamiento=0.99995, max_iter_sin_mejora=10000):
    """
    Algoritmo de Recocido Simulado para resolver el VRP.
    Minimiza la DISTANCIA total.
    """
    mejor_solucion = solucion_inicial[:]
    mejor_costo = vrp_instance.calcular_costo_solucion(mejor_solucion)

    solucion_actual = solucion_inicial[:]
    costo_actual = vrp_instance.calcular_costo_solucion(solucion_actual)

    T = T_inicial
    iter_sin_mejora = 0
    iteracion = 0
    historial_costos = []

    print(f"Iteración {iteracion}: Mejor DISTANCIA actual: {mejor_costo:.2f}, Temperatura: {T:.4f}")

    while T > T_final and iter_sin_mejora < max_iter_sin_mejora:
        iteracion += 1

        solucion_vecina = vrp_instance.generar_vecino(solucion_actual)
        costo_vecina = vrp_instance.calcular_costo_solucion(solucion_vecina)
        historial_costos.append(costo_vecina)

        delta_E = costo_vecina - costo_actual

        if delta_E < 0 or random.random() < math.exp(-delta_E / T):
            solucion_actual = solucion_vecina
            costo_actual = costo_vecina

            if costo_actual < mejor_costo:
                mejor_solucion = solucion_actual[:]
                mejor_costo = costo_actual
                iter_sin_mejora = 0
                print(f"Iteración {iteracion}: NUEVA MEJOR SOLUCIÓN ENCONTRADA (DISTANCIA): {mejor_costo:.2f}")
            else:
                iter_sin_mejora += 1
        else:
            iter_sin_mejora += 1

        T *= enfriamiento

        print(f"Iteración {iteracion}: Mejor DISTANCIA actual: {mejor_costo:.2f}, Temperatura: {T:.6f}, Iteraciones sin mejora: {iter_sin_mejora}")

    print(f"Finalizado en Iteración {iteracion}.")
    return mejor_solucion, mejor_costo, historial_costos, iteracion

# --- 4. FUNCIÓN PARA VISUALIZAR LAS RUTAS OPTIMIZADAS EN EL MAPA ---

def visualizar_rutas_en_mapa(vrp_instance, solucion_optimizada, nombre_archivo_html="mapa_rutas_optimizadas.html"):
    """
    Visualiza las rutas optimizadas en un mapa interactivo de Culiacán.
    Incluye marcadores para *todos* los Centros de Distribución y las Tiendas visitadas en la solución.
    """
    mapa = folium.Map(location=[24.8070, -107.3900], zoom_start=12, tiles='OpenStreetMap')

    colores = [
        'red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige',
        'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue',
        'lightgreen', 'gray', 'black', 'lightgray'
    ]

    tiendas_df = pd.read_excel('datos_distribucion_tiendas.xlsx')
    coordenadas = dict(zip(tiendas_df['Nombre'], zip(tiendas_df['Latitud_WGS84'], tiendas_df['Longitud_WGS84'])))

    for nombre_centro in vrp_instance.centros:
        if nombre_centro in coordenadas:
            lat, lon = coordenadas[nombre_centro]
            folium.Marker(
                location=[lat, lon],
                popup=f"<b>{nombre_centro}</b>",
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(mapa)

    for i, ruta in enumerate(solucion_optimizada):
        color_ruta = colores[i % len(colores)]

        puntos_ruta = []
        for nodo in ruta:
            if nodo in coordenadas:
                lat, lon = coordenadas[nodo]
                puntos_ruta.append([lat, lon])
                if "Tienda" in nodo:
                    folium.Marker(
                        location=[lat, lon],
                        popup=f"<b>{nodo}</b>",
                        icon=folium.Icon(color='blue', icon='shopping-cart')
                    ).add_to(mapa)

        if len(puntos_ruta) > 1:
            folium.PolyLine(
                puntos_ruta,
                color=color_ruta,
                weight=5,
                opacity=0.7,
                tooltip=f'Ruta {i+1}'
            ).add_to(mapa)

    mapa.save(nombre_archivo_html)
    print(f"✅ Mapa de rutas optimizadas guardado como '{nombre_archivo_html}'. Ábrelo en tu navegador.")

# --- 5. CÓDIGO PRINCIPAL ---

if __name__ == "__main__":
    print("Cargando datos y calculando matriz de distancias...")
    # Cargar los datos de las tiendas
    tiendas_df = pd.read_excel('datos_distribucion_tiendas.xlsx')
    nombres_nodos = tiendas_df['Nombre'].tolist()
    latitudes = tiendas_df['Latitud_WGS84'].values
    longitudes = tiendas_df['Longitud_WGS84'].values

    # Calcular la matriz de distancias desde las coordenadas
    n = len(nombres_nodos)
    distancias = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            distancias[i, j] = haversine(latitudes[i], longitudes[i], latitudes[j], longitudes[j])

    # Convertir a DataFrame
    distancias_df = pd.DataFrame(distancias, index=nombres_nodos, columns=nombres_nodos)
    # Opcional: Guardar la matriz calculada
    # distancias_df.to_excel('matriz_distancias_calculada.xlsx')

    print("Inicializando el problema VRP...")
    # Crear instancia del problema VRP
    vrp = VRP(distancias_df)

    # --- Ejemplo de uso ---
    centro_inicio_nombre = vrp.centros[0]  # Usar el primer centro
    print(f"Generando solución inicial aleatoria desde: {centro_inicio_nombre}")
    solucion_inicial = vrp.generar_solucion_aleatoria(centro_inicio_nombre)

    print("\nSolución Inicial Aleatoria (ejemplo):")
    for i, ruta in enumerate(solucion_inicial):
        print(f"  Ruta {i+1}: {ruta[:5]}... (y {len(ruta)-2} tiendas más, termina en {ruta[-1]})") # Mostrar solo inicio y fin
    costo_inicial = vrp.calcular_costo_solucion(solucion_inicial)
    print(f"Distancia total de la solución inicial aleatoria: {costo_inicial:.2f}")

    # --- EJECUTAR EL ALGORITMO ---
    print("\nEjecutando Recocido Simulado (minimizando DISTANCIA)...")
    mejor_solucion_sa, mejor_costo_sa, historial_costos, iteraciones_totales = simulated_annealing(vrp, solucion_inicial)

    print("\nMejor solución encontrada por SA (minimizando distancia):")
    for i, ruta in enumerate(mejor_solucion_sa):
        print(f"  Ruta {i+1}: {ruta[:5]}... (y {len(ruta)-2} tiendas más, termina en {ruta[-1]})") # Mostrar solo inicio y fin
    print(f"Distancia total de la mejor solución: {mejor_costo_sa:.2f}")

    # Comparar con la solución inicial
    print(f"\nComparación:")
    print(f"Distancia inicial: {costo_inicial:.2f}")
    print(f"Distancia con SA:  {mejor_costo_sa:.2f}")
    if costo_inicial > 0:
        mejora_porcentaje = ((costo_inicial - mejor_costo_sa) / costo_inicial) * 100
        print(f"Mejora de DISTANCIA: {mejora_porcentaje:.2f}%")
    else:
        print("No se puede calcular mejora por distancia inicial 0.")

    print(f"Iteraciones totales del algoritmo: {iteraciones_totales}")

    # --- VISUALIZAR LAS RUTAS OPTIMIZADAS EN EL MAPA ---
    print("\nVisualizando las rutas optimizadas en el mapa...")
    visualizar_rutas_en_mapa(vrp, mejor_solucion_sa)

    print("\n🎉 ¡Todo listo! Abre el archivo 'mapa_rutas_optimizadas.html' en tu navegador para ver las rutas.")