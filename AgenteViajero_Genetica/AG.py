import random
import numpy as np
import operator # Solo se usa aquí, está bien

# --- CLASES PRINCIPALES ---

class Municipio:
    """
    Representa un municipio con coordenadas geográficas (x, y).
    Se utiliza para calcular distancias entre puntos.
    """
    def __init__(self, nombre, x, y):
        self.nombre = nombre  # Nombre del municipio (opcional, útil para debug)
        self.x = x
        self.y = y

    def distancia(self, otro_municipio):
        """
        Calcula la distancia euclidiana entre este municipio y otro usando el teorema de Pitágoras.
        :param otro_municipio: Objeto Municipio
        :return: Distancia flotante
        """
        xDis = abs(self.x - otro_municipio.x)
        yDis = abs(self.y - otro_municipio.y)
        return np.sqrt((xDis ** 2) + (yDis ** 2))

    def __repr__(self):
        """Representación textual del municipio."""
        return f"{self.nombre} ({self.x}, {self.y})"


class Aptitud: 
    """
    Calcula la aptitud de una ruta (solución candidata) en el problema del viajante.
    La aptitud es inversamente proporcional a la distancia total de la ruta.
    OPTIMIZACIÓN: Cachear la distancia para evitar recálculos.
    """
    def __init__(self, ruta):
        self.ruta = ruta
        self.distancia = 0
        self.f_aptitud = 0.0

    def distanciaRuta(self):
        """
        Calcula la distancia total de la ruta, incluyendo el retorno al punto inicial.
        OPTIMIZACIÓN: Solo calcula si no está cacheada.
        :return: Distancia total (float)
        """
        if self.distancia == 0:
            distancia_total = 0
            for i in range(len(self.ruta)):
                punto_inicial = self.ruta[i]
                punto_final = self.ruta[(i + 1) % len(self.ruta)]  # Vuelve al inicio si es el último
                distancia_total += punto_inicial.distancia(punto_final)
            self.distancia = distancia_total
        return self.distancia

    def rutaApta(self):
        """
        Calcula la aptitud de la ruta. Cuanto menor sea la distancia, mayor será la aptitud.
        OPTIMIZACIÓN: Solo calcula si no está cacheada.
        :return: Valor de aptitud (float)
        """
        if self.f_aptitud == 0:
            self.f_aptitud = 1 / float(self.distanciaRuta())
        return self.f_aptitud


# --- FUNCIONES DE ALGORITMO GENÉTICO ---

def crear_ruta(lista_municipios):
    """
    Genera una ruta aleatoria (permutación) de los municipios.
    :param lista_municipios: Lista de objetos Municipio
    :return: Lista aleatoria de Municipios
    """
    return random.sample(lista_municipios, len(lista_municipios))


def poblacion_inicial(tamano_pob, lista_municipios):
    """
    Crea la población inicial de rutas aleatorias.
    :param tamano_pob: Tamaño de la población
    :param lista_municipios: Lista de objetos Municipio
    :return: Lista de rutas (cada ruta es una lista de Municipios)
    """
    poblacion = []
    for _ in range(tamano_pob):
        poblacion.append(crear_ruta(lista_municipios))
    return poblacion


def clasificacion_rutas(poblacion):
    """
    Clasifica la población según su aptitud (de mayor a menor).
    OPTIMIZACIÓN: Uso directo de la función de aptitud sin Pandas.
    :param poblacion: Lista de rutas
    :return: Lista ordenada de tuplas (índice, aptitud)
    """
    fitness_results = {}
    for i, ruta in enumerate(poblacion):
        # Crear objeto Aptitud solo para obtener la aptitud
        # Si la ruta cambia, la distancia se recalcula. Si no, se usa la cacheada.
        fitness_results[i] = Aptitud(ruta).rutaApta()
    # Ordenar por aptitud descendente
    return sorted(fitness_results.items(), key=operator.itemgetter(1), reverse=True)


def seleccion_rutas(pop_ranked, indiv_seleccionados):
    """
    Implementa la selección por ruleta (roulette wheel selection).
    OPTIMIZACIÓN: Se eliminó el uso de Pandas y se calculó la suma total de aptitudes una sola vez.
    :param pop_ranked: Lista ordenada de (índice, aptitud)
    :param indiv_seleccionados: Número de individuos a seleccionar directamente (elitismo)
    :return: Lista de índices seleccionados
    """
    resultados_seleccion = []
    # Selección elitista: los mejores 'indiv_seleccionados'
    for i in range(indiv_seleccionados):
        resultados_seleccion.append(pop_ranked[i][0])

    # Calcular la aptitud total una sola vez
    aptitud_total = sum(aptitud for _, aptitud in pop_ranked)

    # Selección por ruleta para el resto
    for _ in range(len(pop_ranked) - indiv_seleccionados):
        seleccion = aptitud_total * random.random() # Selecciona un valor entre 0 y aptitud_total
        aptitud_acumulada = 0
        for i in range(len(pop_ranked)):
            aptitud_acumulada += pop_ranked[i][1] # Agrega la aptitud actual
            if seleccion <= aptitud_acumulada:
                resultados_seleccion.append(pop_ranked[i][0])
                break # Sale del bucle interno si encuentra el individuo
    return resultados_seleccion
 

def grupo_apareamiento(poblacion, resultados_seleccion):
    """
    Construye el grupo de apareamiento a partir de los índices seleccionados.
    :param poblacion: Lista de rutas
    :param resultados_seleccion: Lista de índices seleccionados
    :return: Lista de rutas seleccionadas para apareamiento
    """
    grupo_apareamiento = []
    for idx in resultados_seleccion:
        grupo_apareamiento.append(poblacion[idx])
    return grupo_apareamiento


def reproduccion(progenitor1, progenitor2):
    """
    Operador de cruce (crossover) tipo Order Crossover (OX).
    :param progenitor1: Ruta padre 1
    :param progenitor2: Ruta padre 2
    :return: Hijo (nueva ruta)
    """
    hijo_p1 = []
    hijo_p2 = []

    # Seleccionar dos puntos de corte aleatorios
    gen_x = int(random.random() * len(progenitor1))
    gen_y = int(random.random() * len(progenitor2))
    gen_inicial = min(gen_x, gen_y)
    gen_final = max(gen_x, gen_y)

    # Copiar segmento del primer padre
    hijo_p1 = progenitor1[gen_inicial:gen_final]

    # Completar con genes del segundo padre, sin repetir
    hijo_p2 = [item for item in progenitor2 if item not in hijo_p1]

    # Concatenar
    hijo = hijo_p1 + hijo_p2
    return hijo


def reproduccion_poblacion(grupo_apareamiento, indiv_seleccionados):
    """
    Genera una nueva población mediante reproducción.
    :param grupo_apareamiento: Grupo de padres seleccionados
    :param indiv_seleccionados: Número de individuos elitistas
    :return: Nueva población de hijos
    """
    hijos = []
    tamano = len(grupo_apareamiento) - indiv_seleccionados
    espacio = random.sample(grupo_apareamiento, len(grupo_apareamiento))

    # Mantener los individuos elitistas
    for i in range(indiv_seleccionados):
        hijos.append(grupo_apareamiento[i])

    # Crear nuevos hijos mediante cruce
    for i in range(tamano):
        hijo = reproduccion(espacio[i], espacio[len(grupo_apareamiento) - i - 1])
        hijos.append(hijo)
    return hijos


def mutacion(individuo, razon_mutacion):
    """
    Aplica mutación por intercambio (swap mutation) a un individuo.
    :param individuo: Ruta (lista de Municipios)
    :param razon_mutacion: Probabilidad de mutación por gen
    :return: Individuo mutado
    """
    for i in range(len(individuo)):
        if random.random() < razon_mutacion:
            j = int(random.random() * len(individuo))
            # Intercambiar posiciones
            individuo[i], individuo[j] = individuo[j], individuo[i]
    return individuo


def mutacion_poblacion(poblacion, razon_mutacion):
    """
    Aplica mutación a toda la población.
    :param poblacion: Lista de rutas
    :param razon_mutacion: Probabilidad de mutación
    :return: Población mutada
    """
    pob_mutada = []
    for individuo in poblacion:
        individuo_mutado = mutacion(individuo, razon_mutacion)
        pob_mutada.append(individuo_mutado)
    return pob_mutada


def nueva_generacion(generacion_actual, indiv_seleccionados, razon_mutacion):
    """
    Genera la siguiente generación a partir de la actual.
    :param generacion_actual: Población actual
    :param indiv_seleccionados: Número de individuos elitistas
    :param razon_mutacion: Probabilidad de mutación
    :return: Nueva generación
    """
    # 1. Clasificar rutas
    pop_ranked = clasificacion_rutas(generacion_actual)

    # 2. Seleccionar candidatos
    selection_results = seleccion_rutas(pop_ranked, indiv_seleccionados)

    # 3. Formar grupo de apareamiento
    # CORREGIDO: Renombrada la variable local para evitar conflicto de nombres
    grupo_apareamiento_local = grupo_apareamiento(generacion_actual, selection_results)

    # 4. Reproducir
    hijos = reproduccion_poblacion(grupo_apareamiento_local, indiv_seleccionados)

    # 5. Mutar
    nueva_generacion = mutacion_poblacion(hijos, razon_mutacion)

    return nueva_generacion


def algoritmo_genetico(poblacion, tamano_poblacion, indiv_seleccionados, razon_mutacion, generaciones):
    """
    Ejecuta el algoritmo genético para encontrar la mejor ruta.
    :param poblacion: Lista de objetos Municipio
    :param tamano_poblacion: Tamaño de la población inicial
    :param indiv_seleccionados: Número de individuos elitistas
    :param razon_mutacion: Probabilidad de mutación
    :param generaciones: Número de generaciones
    :return: Mejor ruta encontrada
    """
    print("Iniciando algoritmo genético...")
    pop = poblacion_inicial(tamano_poblacion, poblacion)
    mejor_distancia_inicial = 1 / clasificacion_rutas(pop)[0][1]
    print(f"Distancia Inicial: {mejor_distancia_inicial:.2f}")

    for i in range(generaciones):
        pop = nueva_generacion(pop, indiv_seleccionados, razon_mutacion)
        # Imprimir progreso cada 50 generaciones en lugar de cada 100
        if (i + 1) % 50 == 0:
            mejor_distancia_actual = 1 / clasificacion_rutas(pop)[0][1]
            print(f"Generación {i + 1}: Mejor distancia = {mejor_distancia_actual:.2f}")

    mejor_distancia_final = 1 / clasificacion_rutas(pop)[0][1]
    print(f"\nDistancia Final: {mejor_distancia_final:.2f}")

    best_route_index = clasificacion_rutas(pop)[0][0]
    mejor_ruta = pop[best_route_index]
    return mejor_ruta


# --- DATOS DE ENTRADA CORREGIDOS ---
# Definimos los municipios como objetos Municipio, no como sets.

ciudades = [
    Municipio("Madrid", 40.4168, -3.7038),
    Municipio("Barcelona", 41.3784, 2.1925),
    Municipio("Valencia", 39.4699, -0.3763),
    Municipio("Sevilla", 37.3891, -5.9845),
    Municipio("Zaragoza", 41.6488, -0.8891),
    Municipio("Málaga", 36.7213, -4.4214),
    Municipio("Murcia", 37.9833, -1.1333),
    Municipio("Palma de Mallorca", 39.5696, 2.6502),
    Municipio("Las Palmas de Gran Canaria", 28.0997, -15.4157),
    Municipio("Bilbao", 43.2630, -2.9350)
]

# --- EJECUCIÓN DEL ALGORITMO ---
if __name__ == "__main__":
    mejor_ruta = algoritmo_genetico(
        poblacion=ciudades,
        tamano_poblacion=200,      # Aumentado
        indiv_seleccionados=40,    # Ajustado proporcionalmente
        razon_mutacion=0.02,       # Aumentado ligeramente
        generaciones=1000          # Aumentado
    )

    print("\n--- MEJOR RUTA ENCONTRADA ---")
    for i, municipio in enumerate(mejor_ruta):
        print(f"{i + 1}. {municipio}")
