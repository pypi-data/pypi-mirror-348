from importlib.metadata import version
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  # Desactiva los warnings de TensorFlow

__version__ = version("data-augmentation-app")   # ← lo leerá setuptools

from .augmentation_core import augment
from .layers_personalizadas import (
    RandomFlip, RandomRotation, RandomZoom,
    RandomChannelShift, RandomColorDistorsion,
    GaussianNoise, SaltPepperNoise,
)

__all__ = [
    "augment",
    "RandomFlip", "RandomRotation", "RandomZoom",
    "RandomChannelShift", "RandomColorDistorsion",
    "GaussianNoise", "SaltPepperNoise",
]
