# Data Augmentation App

Aplicación en Python que permite aplicar **data augmentation** a colecciones de imágenes mediante capas personalizadas de *TensorFlow / Keras*. Se puede usar tanto con **interfaz gráfica** (PyQt 5) como desde la **línea de comandos** (CLI). Los resultados pueden almacenarse en disco y/o en una base de datos SQLite; además se genera un fichero JSON con los parámetros aplicados a cada imagen.

---

## Características principales

* **GUI** en PyQt 5 (incluida en `data_augmentation_main.py`).
* **CLI** con `argparse`, gestionado por el mismo archivo (`python -m data_augmentation_app …`).
* **Capas Keras personalizadas** (`layers_personalizadas.py`).
* **Funciones núcleo** (`augmentation_core.py`) para transformar y opcionalmente guardar en SQLite.
* Exportación opcional de **metadatos** a JSON.

---

## Requisitos

```bash
Python >= 3.9
TensorFlow >= 2.15
PyQt5
numpy
Pillow
```

Instalación rápida de dependencias:

```bash
pip install -r requirements.txt  # desarrollo rápido
# o, si usas pyproject.toml
pip install .                    # instala el paquete localmente
```

---

## Estructura del proyecto

```
├── data_augmentation_app/        # paquete instalable
│   ├── __init__.py               # marca el paquete y expone la API pública
│   ├── data_augmentation_main.py # GUI + CLI en un mismo ‘main’
│   ├── augmentation_core.py      # lógica de data‑augmentation
│   ├── layers_personalizadas.py  # capas Keras custom
│   └── cli_helpers.py            # (opcional) extras para argparse
├── README.md
├── LICENSE
├── requirements.txt              # dependencias mínimas
└── pyproject.toml                # configuración de empaquetado
```

> **Sobre `__init__.py`**
> Este archivo convierte la carpeta en un *paquete* Python tradicional. Eso permite:
>
> 1. Instalar con `pip install .` y usar `import data_augmentation_app` en cualquier parte.
> 2. Definir un “API pública” reexportando, por ejemplo, `augment` o las capas personalizadas.
> 3. Evitar problemas de rutas con herramientas y tests.

---

## Uso

### Sin instalar (modo desarrollo)

```bash
# GUI (por defecto si no hay flags)
python -m data_augmentation_app

# Ayuda de la CLI
a python -m data_augmentation_app --help

# Ejemplo CLI
python -m data_augmentation_app \
  --input_dir ./dataset/original \
  --output_dir ./dataset/augmented \
  --rotation 20 --flip_horizontal --zoom 0.2 \
  --save_json --db_path ./augmentations.db
```

### Instalado con pip (recomendado)

Tras instalar con `pip install .` (o `pipx install --editable .`):

```bash
data-augmentation            # GUI

data-augmentation --help     # CLI

data-augmentation --input_dir ./imgs --output_dir ./out --rotation 15
```

La *entry‑point* `data-augmentation` se define en la sección `[project.scripts]` de `pyproject.toml`.

---

## Contribuir

1. **Fork** y rama feature:

   ```bash
   git checkout -b feature/mi-mejora
   ```
2. Ejecuta linters y tests:

   ```bash
   pre-commit run --all-files && pytest
   ```
3. Abre un **pull request**.
