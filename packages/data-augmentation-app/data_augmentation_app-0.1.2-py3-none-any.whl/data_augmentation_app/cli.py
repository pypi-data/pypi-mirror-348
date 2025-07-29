import argparse
from .layers_personalizadas import (
        RandomColorDistorsion, RandomChannelShift,
        GaussianNoise, RandomFlip, RandomRotation,
        RandomZoom, SaltPepperNoise
    )

#  Devuelve la misma estructura de configuración que genera la GUI, alimentada desde la línea de comandos con argparse
def parse_args(argv=None):

###############################################
# Argumentos de confirguración inicial
# (carpetas de entrada y salida, base de datos, número de aumentos)
###############################################
    p = argparse.ArgumentParser(
        prog="ImageAugCLI",
        description="Aplicar data-augmentation desde CLI."
    )
    p.add_argument("--in-dir", help="Carpeta de imágenes de entrada")
    p.add_argument("--out-dir", help="Carpeta donde guardar las imágenes aumentadas")
    p.add_argument("--json-dir", help="Carpeta donde guardar los parámetros en JSON")
    p.add_argument("--db-path", help="Ruta a la base de datos SQLite (.db)")
    p.add_argument("--num-aug", type=int, default=20, help="Aumentos que se generarán por cada imagen (default: 20)")
    p.add_argument("--use-cpu", action="store_true", help="Usar CPU para el procesamiento")

###############################################
# Argumentos de las transformaciones
###############################################

    # Random Flip
    g = p.add_argument_group("Random Flip")
    g.add_argument("--random-flip", action="store_true",
                   help="Activa la capa RandomFlip")
    g.add_argument("--flip-horizontal", dest="flip_horizontal",
                   action=argparse.BooleanOptionalAction, default=True,
                   help="Permitir volteo horizontal (default: True)")
    g.add_argument("--flip-vertical", dest="flip_vertical",
                   action=argparse.BooleanOptionalAction, default=True,
                   help="Permitir volteo vertical (default: True)")

    # Random Rotation
    g = p.add_argument_group("Random Rotation")
    g.add_argument("--random-rotation", action="store_true",
                   help="Activa la capa RandomRotation")
    g.add_argument("--rotation-delta", type=float, default=0.2, help="(default: 0.2)")

    # Random Zoom
    g = p.add_argument_group("Random Zoom")
    g.add_argument("--random-zoom", action="store_true",
                   help="Activa la capa RandomZoom")
    g.add_argument("--zoom-delta", type=float, default=0.2, help="(default: 0.2)")

    # Random Channel Shift
    g = p.add_argument_group("Channel Shift")
    g.add_argument("--random-channel-shift", action="store_true",
                   help="Activa la capa RandomChannelShift")
    g.add_argument("--channel-shift", type=float, default=0.2, help="(default: 0.2)")

    # Color Distortion
    g = p.add_argument_group("Color Distortion")
    g.add_argument("--color-distortion", action="store_true",
                   help="Activa la capa RandomColorDistorsion")
    g.add_argument("--hue-delta", type=float, default=0.5)
    g.add_argument("--saturation-lower", type=float, default=0.5)
    g.add_argument("--saturation-upper", type=float, default=1.5)
    g.add_argument("--brightness-delta", type=float, default=0.2)
    g.add_argument("--contrast-lower", type=float, default=0.8)
    g.add_argument("--contrast-upper", type=float, default=1.2)

    # Gaussian Noise
    g = p.add_argument_group("Gaussian Noise")
    g.add_argument("--gaussian-noise", action="store_true",
                   help="Activa la capa GaussianNoise")
    g.add_argument("--mean-delta", type=float, default=0.0)
    g.add_argument("--stddev-delta", type=float, default=0.1)

    # Salt and Pepper Noise 
    g = p.add_argument_group("Salt and Pepper Noise")
    g.add_argument("--salt-pepper-noise", action="store_true",
                   help="Activa la capa SaltPepperNoise")
    g.add_argument("--amount-delta", type=float, default=0.05)
    g.add_argument("--salt-vs-pepper", type=float, default=0.5)

    # Parseo de argumentos y validación
    args = p.parse_args(argv)

    if not args.in_dir:
        p.error("Debes indicar --in-dir como origen de las imágenes")

    if not (args.out_dir or args.db_path):
        p.error("Debes indicar --out-dir y/o --db-path como destino de las imágenes")

    # Lista de capas seleccionadas
    layers = []

    if args.random_flip:
        layers.append((RandomFlip, {
            "horizontal_flip": args.flip_horizontal,
            "vertical_flip": args.flip_vertical,
        }))

    if args.random_rotation:
        layers.append((RandomRotation, {
            "rotation_delta": args.rotation_delta,
        }))

    if args.random_zoom:
        layers.append((RandomZoom, {
            "zoom_delta": args.zoom_delta,
        }))

    if args.random_channel_shift:
        layers.append((RandomChannelShift, {
            "shift_delta": args.channel_shift,
        }))

    if args.color_distortion:
        layers.append((RandomColorDistorsion, {
            "hue_delta": args.hue_delta,
            "saturation_lower": args.saturation_lower,
            "saturation_upper": args.saturation_upper,
            "brightness_delta": args.brightness_delta,
            "contrast_lower": args.contrast_lower,
            "contrast_upper": args.contrast_upper,
        }))

    if args.gaussian_noise:
        layers.append((GaussianNoise, {
            "mean_delta": args.mean_delta,
            "stddev_delta": args.stddev_delta,
        }))

    if args.salt_pepper_noise:
        layers.append((SaltPepperNoise, {
            "amount_delta": args.amount_delta,
            "salt_vs_pepper": args.salt_vs_pepper,
        }))

    if not layers:
        p.error("Debe activarse al menos una capa de transformación")

    # Diccionario de configuración idéntico al de la GUI
    cfg = {
        "in_dir":  args.in_dir,
        "out_dir": args.out_dir,
        "json_dir": args.json_dir,
        "db_path": args.db_path,
        "num_aug": args.num_aug,
        "use_cpu": args.use_cpu,
        "layers":  layers,
    }
    return cfg
