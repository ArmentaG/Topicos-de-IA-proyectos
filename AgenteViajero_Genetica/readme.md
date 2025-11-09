# Algoritmo Genético para el Problema del Viajante (TSP)

## Descripción general

Este proyecto implementa un algoritmo genético para resolver el Problema del Viajante (Traveling Salesman Problem, TSP). Dado un conjunto de ciudades con sus coordenadas geográficas (latitud y longitud), el objetivo es encontrar la ruta más corta que visite todas las ciudades exactamente una vez y regrese al punto de partida.

El algoritmo genético simula la evolución natural: crea una población inicial de rutas aleatorias, evalúa su "aptitud" (inversamente proporcional a la distancia total), selecciona los mejores individuos, los cruza para generar descendencia y aplica mutaciones para mantener la diversidad genética. El proceso se repite durante un número determinado de generaciones hasta converger a una solución aproximadamente óptima.

## Características del Proyecto

*   **Implementación:** Python 3.8+
*   **Paradigma:** Algoritmo Genético (Metaheurística).
*   **Problema Resuelto:** Problema del Viajante (TSP).
*   **Optimización:** El código ha sido optimizado para mejorar el rendimiento:
    *   **Caché de Distancia:** Se almacena la distancia calculada de una ruta para evitar recálculos innecesarios si la ruta no cambia.
    *   **Eliminación de Pandas en Selección:** Se reemplazó el uso de Pandas en la función de selección por operaciones puras de Python, lo que aumenta la velocidad de ejecución.
*   **Documentación:** Código completamente comentado y modularizado.
*   **Validación:** Se incluyen pruebas formales para verificar la funcionalidad de componentes clave.

## Instrucciones de Ejecución

1.  **Instalar dependencias:**
    Asegúrate de tener Python instalado. Luego, instala las bibliotecas necesarias usando pip:
    ```bash
    pip install numpy
    ```
    > *Nota:* Pandas ya no es estrictamente necesario para la lógica principal, pero puede estar instalado si lo usas en otros proyectos.

2.  **Crear y Activar un Entorno Virtual (Opcional pero recomendado):**
    ```bash
    # Crear el entorno virtual
    python -m venv venv

    # Activar el entorno virtual
    # En Windows:
    venv\Scripts\activate
    # En Linux/macOS:
    source venv/bin/activate
    ```

3.  **Guardar el Código:**
    Guarda el código Python optimizado en un archivo, por ejemplo, `AG.py`.

4.  **Ejecutar el Script:**
    Desde la terminal o consola, navega al directorio donde guardaste `AG.py` y ejecútalo:
    ```bash
    python AG.py
    ```

5.  **Salida Esperada:**
    *   El programa imprimirá mensajes de progreso, mostrando la distancia inicial y la mejor distancia encontrada cada 50 generaciones.
    *   Al finalizar, imprimirá la **distancia final** y la **mejor ruta encontrada**, listando las ciudades en el orden en que deben visitarse.

## Estructura del Código

*   `class Municipio`: Representa una ciudad con nombre y coordenadas (x, y). Contiene un método para calcular la distancia euclidiana a otra ciudad.
*   `class Aptitud`: Calcula la distancia total y la aptitud de una ruta específica. Utiliza caché para mejorar el rendimiento.
*   `crear_ruta`, `poblacion_inicial`: Funciones para generar la población inicial de rutas aleatorias.
*   `clasificacion_rutas`: Clasifica las rutas de la población según su aptitud.
*   `seleccion_rutas`: Implementa la selección por ruleta (roulette wheel selection) y elitismo.
*   `grupo_apareamiento`: Selecciona las rutas que servirán como padres para la siguiente generación.
*   `reproduccion`: Cruza dos rutas padres para producir una nueva ruta hijo (Order Crossover).
*   `reproduccion_poblacion`: Genera una nueva población completa a partir del grupo de apareamiento.
*   `mutacion`, `mutacion_poblacion`: Aplican mutaciones por intercambio (swap mutation) a los individuos.
*   `nueva_generacion`: Coordina los pasos de selección, apareamiento, reproducción y mutación para crear una nueva generación.
*   `algoritmo_genetico`: Función principal que ejecuta el ciclo del algoritmo genético por un número determinado de generaciones.
*   `if __name__ == "__main__":`: Bloque principal que define las ciudades y ejecuta el algoritmo con parámetros específicos.

## Pruebas Formales

Se realizaron pruebas para validar la implementación:

*   **Pruebas Unitarias (Ejemplo):**
    *   `test_distancia_municipio`: Verifica que el cálculo de distancia entre dos municipios sea correcto.
    *   `test_ruta_aptitud`: Verifica que la aptitud se calcule como el inverso de la distancia.
*   **Pruebas de Integración (Ejemplo):**
    *   `test_nueva_generacion`: Verifica que la función `nueva_generacion` produzca una población válida (mismo tamaño, rutas sin duplicados).
*   **Prueba de Ejecución Completa:**
    *   Se ejecutó el algoritmo completo con 10 ciudades, 200 individuos, 1000 generaciones y una tasa de mutación del 2%. El programa finalizó exitosamente, produciendo una ruta final lógica y mejor que la inicial, demostrando su correcto funcionamiento.

## Parámetros del Algoritmo

Los parámetros del algoritmo pueden ajustarse en la llamada a `algoritmo_genetico`:

*   `poblacion`: Lista de objetos `Municipio` que representan las ciudades a visitar.
*   `tamano_poblacion`: Número de rutas candidatas en cada generación (por defecto 200).
*   `indiv_seleccionados`: Número de individuos que pasan directamente a la siguiente generación por elitismo (por defecto 40).
*   `razon_mutacion`: Probabilidad de que un gen (posición de una ciudad en la ruta) mute (por defecto 0.02).
*   `generaciones`: Número de iteraciones del algoritmo (por defecto 1000).

## Notas

*   El algoritmo encuentra una **aproximación** a la solución óptima, no necesariamente la solución exacta. Es común que converja a un "óptimo local".
*   El tiempo de ejecución depende de `tamano_poblacion`, `generaciones` y el número de `ciudades`.
*   El código está listo para probar con diferentes conjuntos de ciudades simplemente modificando la lista `ciudades`.
