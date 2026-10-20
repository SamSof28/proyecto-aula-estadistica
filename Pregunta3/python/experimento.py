import time
import random
import csv
from typing import List

def ejecutar_experimento():
    iteraciones: int = 100
    tamano_arreglo: int = 1_000_000
    resultados: List[int] = []

    print("Generando arreglo original de  millón de números...")
    arreglo_base: List[int] = [random.random() for _ in range(tamano_arreglo)]

    print("Fase de calentamiento...")
    for _ in range(3):
        copia_calentamiento: List[int] = arreglo_base.copy()
        copia_calentamiento.sort()

    print("Iniciando medición oficial...")
    for i in range(iteraciones):
        # Clonamos el arreglo para ordenar siempre los mismos datos desordenados
        arreglo_prueba: List[int] = arreglo_base.copy()

        # Iniciamos cronometro justo antes de la acción
        inicio: time = time.perf_counter_ns()
        arreglo_prueba.sort()
        fin: time = time.perf_counter_ns()

        tiempo_ms: float = (fin - inicio) / 1_000_000.0
        resultados.append(["Python", tiempo_ms])

        if (i + 1) % 10 == 0:
            print(f"Iteración {i + 1}/100 completada.")

    with open('tiempos_python.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Lenguaje", "Tiempo_ms"])
        writer.writerows(resultados)

    print("Experimento Python finalizado. Datos guardados en tiempos_python.csv")

if __name__ == "__main__":
    ejecutar_experimento()