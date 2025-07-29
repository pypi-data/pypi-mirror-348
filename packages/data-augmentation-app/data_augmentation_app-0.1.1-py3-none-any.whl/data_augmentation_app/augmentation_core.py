import sqlite3
import os, io, json
import numpy as np
from PIL import Image
import tensorflow as tf

###############################################
# Conexión y almacenamiento en la base de datos
###############################################

# Se concecta con la base de datos SQLite y crea la tabla si no existe
def conectar_base_datos(nombre_db: str):
    conn = sqlite3.connect(nombre_db)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS imagenes_aumentadas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            imagen BLOB NOT NULL,
            label TEXT
        )"""
    )
    conn.commit()
    return conn

# Almacena la imagen y el nombre del tipo de figura en la base de datos
def almacenar_imagen_base_datos(conn, img_bytes: bytes, label: str):
    conn.execute(
        "INSERT INTO imagenes_aumentadas (imagen, label) VALUES (?, ?)",
        (img_bytes, label),
    )
    conn.commit()



###############################################
# Función principal de Data Augmentation
###############################################

# Se ejecuta y hace todo el trabajo de Data Augmentation
def augment(cfg: dict, progress_cb=None, stop_flag=None):
    # Se conecta a la base de datos
    conn = conectar_base_datos(cfg["db_path"]) if cfg.get("db_path") else None
    try:
        # Obtiene la lista de archivos en la carpeta de entrada y calcula el total de transformaciones a implementar
        files = [f for f in os.listdir(cfg["in_dir"])
                if os.path.isfile(os.path.join(cfg["in_dir"], f))]
        total = len(files) * cfg["num_aug"]
        step = 0

        # Construcción del pipeline de transformaciones
        pipeline = tf.keras.Sequential([cls(**params) for cls, params in cfg["layers"]])

        # Carga la imagen y la pasa por el pipeline para aplicarle las transformaciones
        for file in files:

            img_path = os.path.join(cfg["in_dir"], file)
            label = os.path.splitext(file)[0].split("_")[0]

            # Carga la imagen en formato array float [0,1] y añade una dimensión para el batch size
            arr = tf.keras.utils.img_to_array(tf.keras.utils.load_img(img_path)) / 255.0
            arr = tf.expand_dims(arr, 0)  # Formato (1, H, W, C)

            for i in range(cfg["num_aug"]):

                # Si se recibe la señal de parada, se detiene el proceso
                if stop_flag and stop_flag():
                    raise KeyboardInterrupt("Proceso cancelado por el usuario")
                
                # Aplica las transformaciones a una imagen y almacena los parámetos utilizados
                if cfg.get("use_cpu"):
                    with tf.device('/CPU:0'):
                        aug = pipeline(arr, training=True)
                else:
                    aug = pipeline(arr, training=True)
                params = {f"layer_{l.name}": getattr(l, "params", {}) for l in pipeline.layers}

                # Cambia la imagen de tensor a formato PIL [0,255]
                aug = tf.clip_by_value(aug[0], 0, 1).numpy() * 255
                pil_img = Image.fromarray(aug.astype(np.uint8))

                # Guarda la imagen como PNG en disco
                base = os.path.splitext(file)[0]
                name = f"{base}_{i}.png"
                if cfg["out_dir"]:
                    pil_img.save(os.path.join(cfg["out_dir"], name))

                # Guarda los parámetros utilizados en las transfoprmaciones en un JSON
                if cfg["json_dir"]:
                    with open(os.path.join(cfg["json_dir"], f"{base}_{i}.json"), "w") as fp:
                        json.dump(params, fp, indent=2)

                # Guarda la imagen en formato PNG y el tipo de figura (label) en la base de datos SQLite
                if conn:
                    buf = io.BytesIO()
                    pil_img.save(buf, format="PNG")
                    almacenar_imagen_base_datos(conn, buf.getvalue(), label)

                # Actualiza la barra de carga de la GUI
                step += 1
                if progress_cb:
                    progress_cb(int(step * 100 / total))
    finally:
        # Cierra la conexión con la base de datos
        if conn:
            conn.close()
