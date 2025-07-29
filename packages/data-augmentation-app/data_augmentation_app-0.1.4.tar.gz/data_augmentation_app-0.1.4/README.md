# Data Augmentation App

Aplicación en Python que permite aplicar **data augmentation** a colecciones de imágenes mediante capas personalizadas de *TensorFlow / Keras*. Se puede usar tanto con **interfaz gráfica** (PyQt 5) como desde la **línea de comandos** (CLI). Los resultados pueden almacenarse en disco y/o en una base de datos SQLite; además se genera un fichero JSON con los parámetros aplicados a cada imagen. Permite forzar el uso de CPU en vez de GPU o TPU,
en caso de no contar con los drivers necesarios instalados.

---

## Índice

1. [Características](#características)
2. [Instalación](#instalación)
3. [Requisitos](#requisitos)
4. [Uso rápido](#uso-rápido)
   1. [GUI](#interfaz-gráfica-gui)
   2. [CLI](#línea-de-comandos-cli)
5. [Ejemplos](#ejemplos)
6. [Arquitectura del proyecto](#arquitectura-del-proyecto)
7. [Contribuir](#contribuir)
8. [Licencia](#licencia)

---

## Características

* **Transformaciones de imagen** basadas en capas personalizadas de Keras:

  * Volteo aleatorio horizontal/vertical
  * Rotación aleatoria
  * Zoom aleatorio
  * Desplazamiento de canales (*channel shift*)
  * Distorsión de color (hue, saturación, brillo, contraste)
  * Ruido gaussiano
  * Ruido *Salt & Pepper*
* **Modo GUI** (PyQt5) con barra de progreso y cancelación.
* **Modo CLI** con `argparse`, ideal para automatización y *pipelines*.
* **Salida flexible**:

  * Carpeta en disco (PNG)
  * Base de datos SQLite (blob + etiqueta)
  * Ficheros JSON con los parámetros aplicados a cada transformación.
* Opción de forzar ejecución en **CPU**.

## Instalación

```bash
pip install data-augmentation-app
```

> ⚠️ Asegúrate de usar un *virtual environment* para evitar conflictos de dependencias.

## Requisitos

* Python ≥ 3.8
* TensorFlow ≥ 2.8
* PyQt5 ≥ 5.15
* Pillow
* NumPy

Las dependencias principales se instalan automáticamente desde *PyPI*.

> **Nota en sistemas Unix**
> TensorFlow puede mostrar algunos *warnings* (p. ej. sobre extensiones AVX, variables de entorno o aceleradores no detectados) al arrancar.
> Estos mensajes son solo informativos y **no afectan al funcionamiento ni a los resultados de la aplicación**.

## Uso rápido

### Interfaz gráfica (GUI)

```bash
data-augmentation
```

1. Selecciona la carpeta de imágenes de entrada.
2. Indica al menos uno de los destinos: carpeta de salida y/o archivo `.db` de SQLite.
3. En caso de considerarlo oportuno, activa el uso de CPU para las transformaciones.
4. Activa las transformaciones deseadas y ajusta sus parámetros.
5. Pulsa **Iniciar** y sigue la barra de progreso. Puedes detener el proceso en cualquier momento.

### Línea de comandos (CLI)

```bash
data-augmentation --help
```

Los parámetros más importantes son:

| Parámetro                                                                                     | Descripción                                              |
| --------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| `--in-dir`                                                                                    | Carpeta de imágenes de entrada (obligatorio)             |
| `--out-dir`                                                                                   | Carpeta para guardar las imágenes aumentadas             |
| `--db-path`                                                                                   | Ruta a la base de datos SQLite donde almacenar los blobs |
| `--json-dir`                                                                                  | Carpeta donde guardar los ficheros JSON de parámetros    |
| `--num-aug`                                                                                   | Nº de augmentos por imagen *(por defecto 20)*            |
| `--use-cpu`                                                                                   | Fuerza la ejecución en CPU                               |
| `--random-flip` `--flip-horizontal/--no-flip-horizontal` `--flip-vertical/--no-flip-vertical` | Activa el volteo aleatorio y sus opciones                |
| `--random-rotation` `--rotation-delta 0.3`                                                    | Rotación aleatoria ±0.3                                  |
| `--random-zoom` `--zoom-delta 0.25`                                                           | Zoom aleatorio ±0.25                                     |
| `--random-channel-shift` `--channel-shift 0.2`                                                | Desplazamiento de canales                                |
| `--color-distortion` …                                                                        | Distorsiones de color (hue, brillo, etc.)                |
| `--gaussian-noise` …                                                                          | Ruido gaussiano                                          |
| `--salt-pepper-noise` …                                                                       | Ruido sal y pimienta                                     |

#### Ejemplo mínimo

```bash
data-augmentation \
    --in-dir ./imgs \
    --out-dir ./augmented \
    --num-aug 30 \
    --random-flip --random-rotation --rotation-delta 0.25
```

---

## Ejemplos

Al finalizar se generarán archivos `*.png` y, si lo indicas, sus correspondientes `*.json` con esta estructura:

```
augmented/
├── imagen_0.png
├── imagen_0.json
├── imagen_1.png
├── imagen_1.json
└── …
```

La base de datos SQLite contendrá una tabla `imagenes_aumentadas` con los blobs de imagen y su etiqueta.

---

## Arquitectura del proyecto

```
data_augmentation_app/
├── __init__.py            # Metadata del paquete y exportación de API pública
├── data_augmentation_main.py  # Lanza la GUI / dispatcher principal
├── cli.py                 # Parsing de argumentos y creación de la config CLI
├── augmentation_core.py   # Núcleo de procesamiento: aplica el pipeline y gestiona la E/S
└── layers_personalizadas.py # Capas Keras para cada transformación
```

Cada transformación es una subclase de `tf.keras.layers.Layer`, de modo que el *pipeline* se construye como un `tf.keras.Sequential`, aprovechando la API funcional de TensorFlow y la ejecución en GPU/CPU.

---

## Contribuir

1. Haz un *fork* del repositorio y crea tu rama: `git checkout -b feature/nueva-funcion`.
2. Envía un *pull request* describiendo tus cambios.

¡Se agradecen nuevas transformaciones y mejoras en la interfaz!

---

## Licencia

Este proyecto se distribuye bajo la licencia **MIT**.

## Autoría

Desarrollado con ❤️ por Javier García.
