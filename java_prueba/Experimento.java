package java_prueba;

import java.util.Arrays;
import java.util.Random;
import java.io.FileWriter;
import java.io.IOException;

public class Experimento {
    public static void main(String[] args) {
        int iteraciones = 100;
        int tamano_arreglo = 1_000_000;
        Random random = new Random();
        double[] arreglo_base = new double[tamano_arreglo];

        System.out.println("Generando arreglo original de 1 millón de numeros...");
        for (int i = 0; i < arreglo_base.length; i++){
            arreglo_base[i] = random.nextDouble();
        }

        System.out.println("Fase de calentamiento...");
        for (int i = 0; i < 3; i++){
            double[] copia_calentamiento = Arrays.copyOf(arreglo_base, tamano_arreglo);
            Arrays.sort(copia_calentamiento);
        }

        System.out.println("Iniciando medición oficial...");
        try (FileWriter writer = new FileWriter("tiempos_java.csv")) {
            writer.append("lenguaje,Tiempo_ms\n");

            for (int i = 0; i < iteraciones; i++){
                // Clonamos el arreglo
                double[] arregloPrueba = Arrays.copyOf(arreglo_base, tamano_arreglo);

                // Iniciamos cronómetro
                long inicio = System.nanoTime();
                Arrays.sort(arregloPrueba);
                long fin = System.nanoTime();

                // Convertimos nanosegundos a milisegundos
                double tiempoMs = (fin - inicio) / 1_000_000.0;
                writer.append("Java," + tiempoMs + "\n");

                // Sugerir recolección de basura para evitar picos de latencia
                System.gc();

                if ((i + 1) % 10 == 0){
                    System.out.println("Iteración " + (i + 1) + "/100 completada.");
                }


            }
            System.out.println("Experimento Java finalizado. Datos guardados en tiempos_java.csv");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}