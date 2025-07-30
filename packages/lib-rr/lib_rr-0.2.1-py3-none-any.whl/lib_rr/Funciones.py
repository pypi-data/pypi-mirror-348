#Funciones.py
import random   # Importar random para generar numeros aleatorios
import numpy as np

# Funcion objetivo a minimizar
def funcion_objetivo(x):
    # """ calcula el cuadrado del valor de x. """
    return x ** 2

# Crear un individuo aleatorio
def crear_individuo(valor_min, valor_max):
    # """ Genera un numero aleatorio dentro de un rango especifico """
    return random.uniform(valor_min, valor_max)
print (crear_individuo)   

# crear una poblacion inicial
def crear_poblacion(tamano, valor_min, valor_max):
    # Genera una lista de individuos aleatorios
    return [crear_individuo(valor_min, valor_max) for _ in range(tamano)]

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