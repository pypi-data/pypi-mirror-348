import sys, os, warnings
import threading

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  # Desactiva los warnings de TensorFlow
import tensorflow

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPalette, QColor, QFont, QIcon
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFileDialog,
    QLabel, QLineEdit, QPushButton, QSpinBox, QDoubleSpinBox,
    QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox,
    QCheckBox, QProgressBar, QMessageBox, QScrollArea, QStyle
)

from .layers_personalizadas import (
    RandomColorDistorsion, RandomChannelShift,
    GaussianNoise, RandomFlip, RandomRotation,
    RandomZoom, SaltPepperNoise
)

from .augmentation_core import augment
from .cli import parse_args

###############################################
# Worker en hilo aparte para no congelar la GUI
###############################################

class AugmentWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    # Constructor del worker, guarda la configuración generada en la ventana y un flag self._stop para detener el proceso si es necesario.
    # cfg contiene todos los atributos necesarios (ruta de entrada, salida, json, base de datos, número de aumentos y capas de transformación).
    def __init__(self, cfg, parent=None):
        super().__init__(parent)
        self.cfg = cfg
        self._stop = threading.Event()

    def stop(self):
        """Marca la bandera de parada para que el sub‑hilo finalice lo antes posible."""
        self._stop.set()

    # Método que se ejecuta en segundo plano y hace todo el trabajo pesado para que la interfaz no se congele
    def run(self):
        try:
            # Llama a la función augment encargada de aplicar las transformaciones a las imágenes
            augment(cfg=self.cfg, progress_cb=self.progress.emit, stop_flag=self._stop.is_set)
            # Construye un texto según dónde se guardaron las imágenes
            destinos = []
            if self.cfg["out_dir"]:
                destinos.append("la carpeta de salida")
            if self.cfg["db_path"]:
                destinos.append("la base de datos")
            txt = f"¡Proceso de Data Augmentation finalizado!\nLas imágenes se han guardado en {' y '.join(destinos)}."

            self.finished.emit(txt)
        except KeyboardInterrupt:
            self.finished.emit("Proceso cancelado por el usuario.")
        except Exception as e:
            self.finished.emit(f"Error: {e}")


###############################################
# Widgets auxiliares
###############################################

# Barra reutilizable de selección de directorio o base de datos
class PathRow(QWidget):

    # Configura el layout de la barra de selección de directorio o base de datos con el icono adecuado
    def __init__(self, text, mode="dir", parent=None):
        super().__init__(parent)
        self.mode = mode
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(QLabel(text))
        self.le = QLineEdit()
        lay.addWidget(self.le, 1)
        btn = QPushButton()
        icon = self.style().standardIcon(
            QStyle.SP_DirOpenIcon if mode == "dir" else QStyle.SP_FileIcon
        )
        btn.setIcon(icon)
        btn.clicked.connect(self.browse)
        lay.addWidget(btn)

    # Abre el explorador de archivos para seleccionar el directorio o base de datos
    def browse(self):
        if self.mode == "dir":
            path = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta")
        else:
            path, _ = QFileDialog.getOpenFileName(
                self,
                "Seleccionar base de datos (.db)",
                filter="Bases de datos (*.db)"
            )
        if path:
            self.le.setText(path)

    # Devuelve el texto de la barra de selección (la ruta)
    def text(self):
        return self.le.text()

# Grupo de widgets reutilizables con checkbox y parámetros auto-desactivables para las transformaciones
class TransformBox(QGroupBox):

    def __init__(self, title, params_def: dict, parent=None):
        super().__init__(title, parent)
        self.setCheckable(True)
        self.setChecked(False)
        grid = QGridLayout(self)
        self.widgets = {}
        for row, (name, meta) in enumerate(params_def.items()):
            typ, default, minimum, maximum, step = meta
            lab = QLabel(name.replace("_", " "))
            if typ == "bool":
                w = QCheckBox()
                w.setChecked(bool(default))
            elif typ == "int":
                w = QSpinBox()
                w.setRange(minimum, maximum)
                w.setSingleStep(step)
                w.setValue(default)
            else:  # float
                w = QDoubleSpinBox()
                w.setDecimals(3)
                w.setRange(minimum, maximum)
                w.setSingleStep(step)
                w.setValue(default)
            self.widgets[name] = w
            grid.addWidget(lab, row, 0)
            grid.addWidget(w, row, 1)
        self.toggled.connect(lambda s: [w.setEnabled(s) for w in self.widgets.values()])

    # Si el grupo esta desactivado, devuelve None, si no devuelve un diccionario con los parámetros de la transformación
    def get_cfg(self):
        if not self.isChecked():
            return None
        cfg = {}
        for k, w in self.widgets.items():
            # Si es un checkbox devolvemos True/False (o int, como se prefiera)
            cfg[k] = w.isChecked() if isinstance(w, QCheckBox) else w.value()
        return cfg


###############################################
# Ventana principal
###############################################

# Ventana principal de la aplicación, contiene todos los widgets y el worker para el procesamiento en segundo plano
class MainWindow(QMainWindow):

    # Configura el título, tamaño y estilo de la ventana principal
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Augmentation")
        self.resize(880, 640)
        self.setWindowIcon(QIcon.fromTheme("applications-graphics"))
        self._set_dark_palette()
        self.worker = None  # Se inicializa antes de construir la interfaz por si se necesita en callbacks
        self._build_ui()

    # Aplica una paleta de colores en modo oscuro para la aplicación, usando el estilo "Fusion"
    def _set_dark_palette(self):
        QApplication.setStyle("Fusion")
        pal = QPalette()
        pal.setColor(QPalette.Window, QColor(45, 45, 45))
        pal.setColor(QPalette.WindowText, Qt.white)
        pal.setColor(QPalette.Base, QColor(30, 30, 30))
        pal.setColor(QPalette.AlternateBase, QColor(45, 45, 45))
        pal.setColor(QPalette.ToolTipBase, Qt.white)
        pal.setColor(QPalette.ToolTipText, Qt.white)
        pal.setColor(QPalette.Text, Qt.white)
        pal.setColor(QPalette.Button, QColor(45, 45, 45))
        pal.setColor(QPalette.ButtonText, Qt.white)
        pal.setColor(QPalette.Link, QColor(100, 150, 255))
        pal.setColor(QPalette.Highlight, QColor(100, 150, 255))
        pal.setColor(QPalette.HighlightedText, Qt.black)
        QApplication.setPalette(pal)

    # Construye toda la GUI de la aplicación, incluyendo los widgets y su disposición
    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        v = QVBoxLayout(central)
        v.setContentsMargins(15, 15, 15, 15)
        v.setSpacing(12)

        # Título
        lbl_title = QLabel("<b>Image Augmentation</b>")
        lbl_title.setFont(QFont("Arial", 22))
        lbl_title.setAlignment(Qt.AlignCenter)
        v.addWidget(lbl_title)

        # Rutas de directorios y base de datos
        grp_paths = QGroupBox("Rutas")
        l_paths = QVBoxLayout(grp_paths)
        self.row_in = PathRow("Imágenes de entrada: ")
        self.row_out = PathRow("Carpeta de salida: ")
        self.row_json = PathRow("Carpeta parámetros JSON: ")
        self.row_db = PathRow("Base de datos (.db): ", mode="file")
        for r in (self.row_in, self.row_out, self.row_json, self.row_db):
            l_paths.addWidget(r)
        v.addWidget(grp_paths)

        # Parámetros generales
        h_param = QHBoxLayout()
        h_param.addWidget(QLabel("Aumentos por imagen:"))
        self.spn_aug = QSpinBox()
        self.spn_aug.setRange(1, 100)
        self.spn_aug.setValue(20)
        h_param.addWidget(self.spn_aug)
        self.chk_cpu = QCheckBox("Forzar uso de CPU")
        h_param.addWidget(self.chk_cpu)
        h_param.addStretch()
        v.addLayout(h_param)

        # Cuadro de transformaciones
        grp_tf = QGroupBox("Transformaciones disponibles")
        v_tf = QVBoxLayout(grp_tf)
        scr = QScrollArea()
        scr.setWidgetResizable(True)
        inner = QWidget()
        self.v_tf_inner = QVBoxLayout(inner)
        self.v_tf_inner.setAlignment(Qt.AlignTop)
        scr.setWidget(inner)
        v_tf.addWidget(scr)
        v.addWidget(grp_tf, 1)

        self._populate_transforms()

        # Barra de progreso y botones de control
        self.bar = QProgressBar()
        self.lbl_status = QLabel("Listo para comenzar...")

        # Botón Iniciar
        self.btn_start = QPushButton("Iniciar")
        self.btn_start.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.btn_start.clicked.connect(self._start)

        # Botón Detener
        self.btn_stop = QPushButton("Detener")
        self.btn_stop.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.btn_stop.clicked.connect(self._stop_worker)
        self.btn_stop.hide()  # Oculto por defecto

        v.addWidget(self.bar)
        v.addWidget(self.lbl_status)
        v.addWidget(self.btn_start)
        v.addWidget(self.btn_stop)

    # Lista de transformaciones disponibles, cada una con su respectivo grupo de parámetros
    def _populate_transforms(self):
        self.t_boxes = []
        # Formato: (tipo de parámetro, default, min, max, step)
        defs = [
            (
                "Random Flip",
                RandomFlip,
                {
                    "horizontal_flip": ("bool", True, None, None, None),
                    "vertical_flip": ("bool", True, None, None, None),
                },
            ),
            (
                "Random Rotation",
                RandomRotation,
                {"rotation_delta": ("float", 0.2, 0.0, 1.0, 0.01)},
            ),
            (
                "Random Zoom",
                RandomZoom,
                {"zoom_delta": ("float", 0.2, 0.0, 1.0, 0.01)},
            ),
            (
                "Channel Shift",
                RandomChannelShift,
                {"shift_delta": ("float", 0.2, 0.0, 1.0, 0.01)},
            ),
            (
                "Color Distortion",
                RandomColorDistorsion,
                {
                    "hue_delta": ("float", 0.5, 0.0, 0.5, 0.01),
                    "saturation_lower": ("float", 0.5, 0.0, 1.0, 0.05),
                    "saturation_upper": ("float", 1.5, 1.0, 3.0, 0.05),
                    "brightness_delta": ("float", 0.2, 0.0, 1.0, 0.01),
                    "contrast_lower": ("float", 0.8, 0.0, 1.0, 0.05),
                    "contrast_upper": ("float", 1.2, 1.0, 3.0, 0.05),
                },
            ),
            (
                "Gaussian Noise",
                GaussianNoise,
                {
                    "mean_delta": ("float", 0.0, -1.0, 1.0, 0.01),
                    "stddev_delta": ("float", 0.1, 0.0, 1.0, 0.01),
                },
            ),
            (
                "Salt and Pepper Noise",
                SaltPepperNoise,
                {
                    "amount_delta": ("float", 0.05, 0.0, 0.5, 0.01),
                    "salt_vs_pepper": ("float", 0.5, 0.0, 1.0, 0.01),
                },
            ),
        ]
        for title, cls, pdef in defs:
            box = TransformBox(title, pdef)
            self.t_boxes.append((box, cls))
            self.v_tf_inner.addWidget(box)
        self.v_tf_inner.addStretch()

    # Validación de los campos de entrada, comprueba que los directorios y la base de datos estén seleccionados y que al menos una transformación esté activada
    def _validate(self):
        if not self.row_in.text():
            return "Selecciona la carpeta de imágenes de entrada."
        if not (self.row_out.text() or self.row_db.text()):
            return "Selecciona al menos la carpeta de salida o la base de datos (.db)."
        if not any(b.get_cfg() for b, _ in self.t_boxes):
            return "Selecciona al menos una transformación."
        return None

    # Inicia el proceso de data augmentation
    def _start(self):
        err = self._validate()
        if err:
            QMessageBox.warning(self, "Campos incompletos", err)
            return

        # Lanza un aviso en caso de no querer almacenar los parámetros de las transformaciones en archivos JSON
        if not self.row_json.text():
            QMessageBox.information(
                self,
                "Aviso",
                "No se ha seleccionado carpeta para los parámetros JSON.\n"
                "Los parámetros de las transformaciones NO se guardarán."
            )

        if self.chk_cpu.isChecked():
            QMessageBox.information(
                self,
                "Aviso",
                "Las transformaciones se aplicarán en CPU."
            )

        # Crea carpetas si no existen
        if self.row_out.text():
            os.makedirs(self.row_out.text(), exist_ok=True)
        if self.row_json.text():
            os.makedirs(self.row_json.text(), exist_ok=True)

        # Guarda la configuración de la GUI en un diccionario
        cfg = {
            "in_dir": self.row_in.text(),
            "out_dir": self.row_out.text(),
            "json_dir": self.row_json.text(),
            "db_path": self.row_db.text(),
            "num_aug": self.spn_aug.value(),
            "use_cpu": self.chk_cpu.isChecked(),
            "layers": [
                (cls, box.get_cfg())
                for box, cls in self.t_boxes
                if box.get_cfg() is not None
            ],
        }

        self.lbl_status.setText("Procesando...")
        self.bar.setValue(0)

        # Inicia el worker en un hilo aparte para no congelar la GUI y aplica las transformaciones
        self.worker = AugmentWorker(cfg)
        self.worker.progress.connect(self.bar.setValue)
        self.worker.finished.connect(self._done)
        self.worker.start()

        # Cambia los botones
        self.btn_start.hide()
        self.btn_stop.show()
        self.btn_stop.setEnabled(True)

    def _stop_worker(self):
        """Callback del botón Detener."""
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.lbl_status.setText("Deteniendo...")
            self.btn_stop.setEnabled(False)  # Impide múltiples pulsaciones

    # Actualiza la etiqueta de la barra de estado al finalizar el proceso de data augmentation
    def _done(self, txt):
        self.lbl_status.setText(txt)
        self.bar.setValue(0)

        # Restaura los botones
        self.btn_stop.hide()
        self.btn_stop.setEnabled(True)
        self.btn_start.show()
        self.worker = None


###############################################
# Main
###############################################

def main() -> None:
    if len(sys.argv) > 1:
        args = parse_args()
        augment(args)
    else:
        app = QApplication(sys.argv)  # Crea la aplicación
        w = MainWindow()  # Crea la ventana principal
        w.show()  # Muestra la ventana en pantalla
        sys.exit(app.exec_())  # Ejecuta el bucle de eventos


if __name__ == "__main__":
    main()
