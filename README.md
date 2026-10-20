# Proyecto de aula de Estadística para Ingeniería

Proyecto académico de **Estadística para Ingeniería (2026-2)**. El repositorio reúne
los notebooks y los programas usados para resolver las tres preguntas de la guía:

1. análisis descriptivo e inferencial de hornos de cocción a gas;
2. generación y comparación de tiempos de procesamiento para dos equipos;
3. experimento práctico de comparación del tiempo de ordenamiento en Python y Java.

## Integrantes

| Integrante | Nombre completo |
|---|---|
| 1 | **Luis Alejandro Correa Arrieta** |
| 2 | **[Nombre del integrante 2]** |
| 3 | **Samuel Romaña Acevedo** |

Reemplacen los textos entre corchetes por los nombres definitivos del equipo.

## Estructura del repositorio

```text
.
├── docs/
│   ├── PROYECTO ... DEF.md       # Consigna del proyecto
│   └── PROYECTO ... DEF.pdf
├── Pregunta1/
│   └── punto1.ipynb              # Análisis de marcas, emisiones y potencia
├── Pregunta2/
│   └── Punto2.ipynb               # Simulación y pruebas para equipos A y B
└── Pregunta3/
    ├── base_datos_pregunta_3.csv
    ├── tiempos_java.csv
    ├── tiempos_python.csv
    ├── java_prueba/Experimento.java
    └── python/experimento.py
```

## Requisitos

- Python 3.10 o superior.
- Jupyter Notebook o JupyterLab.
- Paquetes de Python: `pandas`, `numpy`, `scipy`, `matplotlib`, `seaborn` y
  `openpyxl`.
- JDK 11 o superior para ejecutar el experimento de Java.

El repositorio todavía no incluye un `requirements.txt`. Para preparar un entorno
local:

```bash
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
# .venv\Scripts\activate        # Windows
python -m pip install jupyter pandas numpy scipy matplotlib seaborn openpyxl
```

## Ejecución

### Pregunta 1

El notebook espera un archivo Excel llamado
`BD Proyecto de Aula DEF 2026-2.xlsx` en el directorio de trabajo del notebook. Ejecutar:

```bash
jupyter notebook Pregunta1/punto1.ipynb
```

El análisis genera el diagrama de cajas de `ppm`, porcentajes de cumplimiento de
potencia, intervalos de confianza, una comparación de varianzas y una prueba
binomial para la marca 5.

### Pregunta 2

```bash
jupyter notebook Pregunta2/Punto2.ipynb
```

El notebook fija la semilla `2026`, genera 60 observaciones por grupo para los
escenarios normal y gamma, muestra histogramas y aplica Shapiro-Wilk,
Welch/Student y Mann-Whitney.

### Pregunta 3: experimento de ordenamiento

Para ejecutar Java desde `Pregunta3/`:

```bash
cd Pregunta3
javac -d . java_prueba/Experimento.java
java java_prueba.Experimento
```

Para ejecutar Python desde `Pregunta3/`:

```bash
cd Pregunta3
python python/experimento.py
```

Ambos programas generan 100 mediciones del ordenamiento de un arreglo de un
millón de números y escriben los resultados en `tiempos_java.csv` y
`tiempos_python.csv`. Los archivos se escriben relativos al directorio actual;
por eso se recomienda ejecutar los comandos desde `Pregunta3/`.

## Resultados disponibles de la Pregunta 3

Las mediciones actualmente versionadas contienen 100 observaciones por lenguaje.
Su resumen descriptivo es:

| Lenguaje | Media (ms) | Desviación estándar (ms) |
|---|---:|---:|
| Java | 98.481 | 8.847 |
| Python | 367.162 | 35.182 |

Estos valores son resultados de una ejecución concreta y dependen del hardware,
la versión del runtime, la carga del sistema y la configuración de la máquina.
No deben interpretarse como una comparación universal entre lenguajes.


## Referencia académica

La consigna original está disponible en
[`docs/`](./docs/), en formato Markdown y PDF. El contenido del informe final
debe respetar las indicaciones de presentación, citación, interpretación y
extensión establecidas allí.
