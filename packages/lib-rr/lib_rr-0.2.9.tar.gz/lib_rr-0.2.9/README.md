![Portada: Import](https://i.imgur.com/7GTQnDw.png)

# lib_rr

**lib_rr** es una librería de Python 🐍 diseñada para facilitar la experimentación con algoritmos genéticos, especialmente aplicada a la **optimización del ángulo de inclinación de paneles solares** 🌞 y el cálculo de la **distancia mínima (DM)** entre ellos.

Esta herramienta está pensada para estudiantes, investigadores o desarrolladores interesados en la eficiencia energética y la aplicación de algoritmos evolutivos. 🏛️

A continuación encontraras la documentación de la libreria, y al final podras ver dos imagenes como ejemplos:

1. Ejemplo para utilizar la libreria desde Google Colab y acceder a los metodos de las Funciones.

2. Ejemplo para utilizar la libreria desde Google Colab y utilizar el algoritmo genetico.

---

## 👥 Autores

**Jorge Andrés Rodríguez Castaño**  
**Carlos Andrés Ramos García**  
Machine Learning y Algoritmos Genéticos – Universidad de Cundinamarca

---

## 🚀 Características principales

- 🧬 Implementación de un **algoritmo genético adaptativo**.
- 🌞 Optimización del ángulo óptimo de inclinación para paneles solares según latitud.
- 📏 Cálculo automático de la **distancia mínima (DM)** entre paneles solares para evitar sombras.
- 🔄 Funciones auxiliares para generación de individuos y poblaciones.
- 🧩 Código modular y reutilizable.


---

## 📦 Instalación

Instálala fácilmente desde PyPI:

```bash
pip install lib_rr

from lib_rr import Funciones, algoritmo_genetico

🔧 Funcionalidades del módulo Funciones.py
Este módulo contiene funciones auxiliares fundamentales para el algoritmo genético,
enfocadas en la creación de individuos, evaluación de aptitud y cálculos solares.

funcion_objetivo(x)
Calcula una función cuadrática simple 🧮

```

![Función objetivo](https://i.imgur.com/gc8Uooo.png)

```bash

  usada como ejemplo de optimización.

Parámetros:
x (float): valor de entrada.

Retorna:
(float) resultado de aplicar la función cuadrática.

crear_individuo(valor_min, valor_max)
Genera un valor aleatorio dentro de un rango dado. Representa un individuo de la población. 🧍

Parámetros:
valor_min (float): límite inferior.
valor_max (float): límite superior.

Retorna:
(float) individuo 🧍 aleatorio generado.

crear_poblacion(tamano, valor_min, valor_max)
Crea una lista de individuos aleatorios que conforman una población inicial. 🌍

Parámetros:
tamano (int): número de individuos.
valor_min (float): valor mínimo por individuo. 🔽
valor_max (float): valor máximo por individuo. 🔼

Retorna:
(list[float]) población generada aleatoriamente.

calcular_Hmin(latitud, invierno)
Calcula el ángulo mínimo de altura solar (Hmin) considerando la latitud 🧭 y condiciones
invernales. ⛄

Parámetros:
latitud (float): ubicación geográfica.
invierno (float): corrección por estación invernal (en grados).

Retorna:
(float) ángulo solar mínimo.

calcular_DM(B, beta_grados, latitud, invierno)
Calcula la distancia mínima entre paneles solares para evitar sombras. 

Parámetros:
B (float): longitud del panel (m).
beta_grados (float): ángulo de inclinación del panel (°).
latitud (float): ubicación (°).
invierno (float): corrección por invierno (°). ❄️

Retorna:
(float) distancia mínima entre paneles (m).

fitness(beta_array, B, latitud, invierno)
Evalúa qué tan buenos son los ángulos beta en función de la distancia mínima obtenida.

Parámetros:
beta_array (list[float]): lista de ángulos a evaluar.
B (float): longitud del panel (m).
latitud (float): ubicación (°).
invierno (float): corrección estacional (°).

Retorna:
np.ndarray con la aptitud negativa de cada ángulo beta.

🤖 Funcionalidades del módulo algoritmo_genetico.py
Este módulo implementa el núcleo del algoritmo genético adaptativo utilizado para
optimizar el ángulo de inclinación de los paneles solares. También incluye funciones
clave para cálculos solares y evaluación de aptitud.

calcular_Hmin(latitud, invierno)
Calcula el ángulo mínimo de altura solar (Hmin) durante el invierno, utilizado en el
cálculo de distancia mínima.

Parámetros:
latitud (float): latitud geográfica (°).
invierno (float): corrección por invierno (°).

Retorna:
(float) ángulo solar mínimo. 📐

calcular_DM(B, beta_grados, latitud, invierno)
Calcula la distancia mínima entre paneles solares, en función de la latitud y el ángulo
de inclinación (beta).

Parámetros:
B (float): longitud del panel solar (m).
beta_grados (float): ángulo de inclinación del panel (°).
latitud (float): latitud geográfica (°).
invierno (float): corrección estacional por invierno (°).

Retorna:
(float) distancia mínima (m) entre paneles. ☀️

fitness(beta_array, B, latitud, invierno)
Evalúa la aptitud de cada ángulo beta calculando la distancia mínima entre paneles.
Entre menor la distancia, mejor la aptitud (negativa para facilitar la maximización).

Parámetros:
beta_array (list[float] o np.ndarray): lista de ángulos a evaluar.
B (float): longitud del panel solar.
latitud (float): latitud geográfica.
invierno (float): corrección estacional.

Retorna:
np.ndarray con los valores de aptitud (negativos).

ejecutar_algoritmo_genetico(tam_poblacion, ngen, p_cruce, p_mutacion, B, latitud, invierno)
Ejecuta un algoritmo genético adaptativo para encontrar el mejor ángulo de inclinación
beta que minimiza la distancia entre paneles solares, dadas ciertas condiciones. 💻

Parámetros:
tam_poblacion (int): tamaño de la población.
ngen (int): número de generaciones.
p_cruce (float): probabilidad de cruce entre individuos.
p_mutacion (float): probabilidad de mutación.
B (float): longitud del panel solar.
latitud (float): latitud geográfica.
invierno (float): corrección por estación invernal.

Retorna:

mejor_beta (float): ángulo de inclinación óptimo (°).

mejor_DM (float): distancia mínima alcanzada (m).

mejores (list[float]): historial del mejor fitness por generación. 💪


```

---

## 🎬 Ejemplos de uso

A continuación, se presentan tres ejemplos visuales del uso de la librería en Google Colab:

Primer ejemplo: Uso de funciones auxiliares 🛠️

![Ejemplo 1: Uso de funciones auxiliares](https://i.imgur.com/E6tSdEE.png)

Segundo ejemplo: como usar el algoritmo genético 🧬

![Ejemplo 2: Ejecución del algoritmo genético](https://i.imgur.com/eYeWgUc.png)

![Ejemplo 3: Resultados visuales del proceso](https://i.imgur.com/N3GBCf9.png)


---