# algoritmo_genetico.py

import numpy as np
import random

# Ángulo de altura solar mínima
def calcular_Hmin(latitud, invierno):
    return (90 - latitud) - invierno

# Distancia mínima entre paneles
def calcular_DM(B, beta_grados, latitud, invierno):
    beta = np.radians(beta_grados)
    Hmin = np.radians(calcular_Hmin(latitud, invierno))
    return B * np.cos(beta) + (B * np.sin(beta)) / np.tan(Hmin)

# Función de aptitud para una población de betas
def fitness(beta_array, B, latitud, invierno):
    return -np.array([calcular_DM(B, beta, latitud, invierno) for beta in beta_array])

# Algoritmo genético adaptativo
def ejecutar_algoritmo_genetico(tam_poblacion, ngen, p_cruce, p_mutacion, B, latitud, invierno):
    poblacion = np.random.uniform(0, 90, tam_poblacion)
    mejores = []

    for _ in range(ngen):
        aptitudes = fitness(poblacion, B, latitud, invierno)
        mejores.append(max(aptitudes))

        # Selección por torneo
        seleccionados = []
        for _ in range(tam_poblacion):
            a, b = random.sample(range(tam_poblacion), 2)
            seleccionados.append(poblacion[a] if aptitudes[a] > aptitudes[b] else poblacion[b])

        # Cruce adaptativo
        nueva_poblacion = []
        for i in range(0, tam_poblacion, 2):
            if random.random() < p_cruce:
                punto = random.uniform(0, 1)
                hijo1 = punto * seleccionados[i] + (1 - punto) * seleccionados[i + 1]
                hijo2 = (1 - punto) * seleccionados[i] + punto * seleccionados[i + 1]
                nueva_poblacion.extend([hijo1, hijo2])
            else:
                nueva_poblacion.extend([seleccionados[i], seleccionados[i + 1]])

        # Mutación adaptativa
        for i in range(tam_poblacion):
            if random.random() < p_mutacion:
                nueva_poblacion[i] += np.random.uniform(-0.1, 0.1)
                nueva_poblacion[i] = np.clip(nueva_poblacion[i], 0, 90)

        poblacion = np.array(nueva_poblacion)

    mejor_beta = poblacion[np.argmax(fitness(poblacion, B, latitud, invierno))]
    mejor_DM = calcular_DM(B, mejor_beta, latitud, invierno)
    return mejor_beta, mejor_DM, mejores
