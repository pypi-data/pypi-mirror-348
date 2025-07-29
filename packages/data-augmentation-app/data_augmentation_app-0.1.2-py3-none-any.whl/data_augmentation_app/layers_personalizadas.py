import tensorflow as tf

class RandomFlip(tf.keras.layers.Layer): # Aplica una rotación horizontal y/o vertical aleatoria a la imagen
    def __init__(self, horizontal_flip=True, vertical_flip=True, seed=None, **kwargs):
        super().__init__(**kwargs)
        self.horizontal_flip = horizontal_flip
        self.vertical_flip = vertical_flip
        self.seed = seed
        self.params = {}

    def call(self, inputs, training = None):
        if training: 
            x = inputs
            horizontal=False
            vertical=False

            # Aplica flip horizontal aleatorio
            if self.horizontal_flip and tf.random.uniform([], 0, 1) > 0.5:
                horizontal = True
                x = tf.image.flip_left_right(x)

            # Aplica flip vertical aleatorio
            if self.vertical_flip and tf.random.uniform([], 0, 1) > 0.5:
                x = tf.image.flip_up_down(x)
                vertical = True

            self.params = {
                "horizontal_flip": horizontal,
                "vertical_flip": vertical
            }
            return x
        else:
            return inputs

class RandomZoom(tf.keras.layers.Layer): # Aplica zoom aleatorio a la imagen
    def __init__(self, zoom_delta = 0.2, seed=None, **kwargs):
        super().__init__(**kwargs)
        self.zoom_delta = zoom_delta
        self.seed = seed
        self.params = {}

    def call(self, inputs, training=None):
        if training:

            # Genera un zoom aleatorio (Numero negativo significa zoom in y numero positivo significa zoom out)
            zoom_factor = tf.random.uniform([], -self.zoom_delta, self.zoom_delta, seed=self.seed) 

            # Aplica el zoom a la imagen
            zoom_layer = tf.keras.layers.RandomZoom(height_factor=(zoom_factor, zoom_factor), fill_mode='nearest')
            x = zoom_layer(inputs)

            zoom_factor = zoom_factor.numpy()
            zoom_factor = 1.0 - zoom_factor

            self.params = {
                "zoom_factor": float(zoom_factor)
            }

            return x
        else:
            return inputs


class RandomRotation(tf.keras.layers.Layer): # Aplica una rotación a la imagen en un rango de ±rotation_delta
    def __init__(self, rotation_delta=0.2, seed=None, **kwargs):
        super().__init__(**kwargs)
        self.rotation_delta = rotation_delta
        self.seed = seed
        self.params = {}
    
    def call(self, inputs, training=None):
        if training:

            # Genera un grado de rotación aleatorio
            rotation_factor = tf.random.uniform([], -self.rotation_delta, self.rotation_delta)
            
            rotation_layer = tf.keras.layers.RandomRotation(factor=(rotation_factor,rotation_factor), fill_mode='nearest')

            # Aplica la rotación a la imagen
            x = rotation_layer(inputs)

            self.params = {
                "rotation_factor": float(rotation_factor.numpy())
            }
            return x
        else:
            return inputs

class RandomColorDistorsion(tf.keras.layers.Layer): # Aplica cambio de hue, saturación, brillo y contraste
    def __init__(self,
                 hue_delta=0.08,
                 saturation_lower=0.5,
                 saturation_upper=1.5,
                 brightness_delta=0.1,
                 contrast_lower=0.8,
                 contrast_upper=1.2,
                 seed=None,
                 **kwargs): 
        super().__init__(**kwargs)
        self.hue_delta = hue_delta
        self.saturation_lower = saturation_lower
        self.saturation_upper = saturation_upper
        self.brightness_delta = brightness_delta
        self.contrast_lower = contrast_lower
        self.contrast_upper = contrast_upper
        self.seed = seed
        self.params = {}

    def call(self, inputs, training=None):
        if training:
            # Genera el factor de hue aleatorio
            hue_factor = tf.random.uniform([], -self.hue_delta, self.hue_delta, seed=self.seed)
            # Aplica el hue con el factor generado a la imagen
            x = tf.image.adjust_hue(inputs, hue_factor)

            # Saturación
            saturation_factor = tf.random.uniform([], self.saturation_lower, self.saturation_upper, seed=self.seed)
            x = tf.image.adjust_saturation(x, saturation_factor)

            # Brillo
            brightness_factor = tf.random.uniform([], -self.brightness_delta, self.brightness_delta, seed=self.seed)
            x = tf.image.adjust_brightness(x, brightness_factor)

            # Contraste
            contrast_factor = tf.random.uniform([], self.contrast_lower, self.contrast_upper, seed=self.seed)
            x = tf.image.adjust_contrast(x, contrast_factor)

            # Almacena todo en un diccionario de parámetros
            self.params = {
                "hue_factor": float(hue_factor.numpy()),
                "saturation_factor": float(saturation_factor.numpy()),
                "brightness_factor": float(brightness_factor.numpy()),
                "contrast_factor": float(contrast_factor.numpy())
            }
            return x
        else:
            return inputs

class RandomChannelShift(tf.keras.layers.Layer): # Desplazamiento de ±shift_delta % en cada canal de color (rojo, verde, azul)
    def __init__(self, shift_delta=0.2, seed=None, **kwargs):
        super().__init__(**kwargs)
        self.shift_delta = shift_delta
        self.seed = seed
        self.params = {}

    def call(self, inputs, training=None):
        if training:

            # Genera un tensor aleatorio a aplicar a cada canal
            shift = tf.random.uniform(
                shape=[1, 1, 1, 3],
                minval=-self.shift_delta,
                maxval=self.shift_delta,
                seed=self.seed,
            )

            # Convierte a float32 para evitar overflow y sumamos el desplazamiento de cada canal
            x = tf.cast(inputs, tf.float32) + shift
            
            # Clampea al rango válido [0,1]
            x = tf.clip_by_value(x, 0.0, 1.0)

            self.params = {
                "shift_r": float(shift[0, 0, 0, 0].numpy()),
                "shift_g": float(shift[0, 0, 0, 1].numpy()),
                "shift_b": float(shift[0, 0, 0, 2].numpy())
            }
            return x
        else:
            return inputs
        
class GaussianNoise(tf.keras.layers.Layer): # Añade ruido gaussiano a la imagen
    def __init__(self, mean_delta=0.0, stddev_delta=0.1, seed=None, **kwargs):
        super().__init__(**kwargs)
        self.mean_delta = mean_delta # Media del ruido gaussiano (se suele establecer en 0.0)
        self.stddev_delta = stddev_delta # Desviación estandar
        self.seed = seed
        self.params = {}

    def call(self, inputs, training=None):
        if training:

            mean = tf.random.uniform([], minval=-self.mean_delta, maxval=self.mean_delta, seed=self.seed)
            stddev = tf.random.uniform([], minval=0.0, maxval=self.stddev_delta, seed=self.seed)

            # Genera un tensor con distribución normal para el ruido gaussiano
            noise = tf.random.normal(shape=tf.shape(inputs), mean=mean, stddev=stddev, seed=self.seed)

            # Suma el ruido a la imagen
            x = inputs + noise
            
            # Clampea al rango válido [0,1]
            x = tf.clip_by_value(x, 0.0, 1.0)

            self.params = {
                "mean": float(mean.numpy()),
                "stddev": float(stddev.numpy())
            }
            return x
        else:
            return inputs


class SaltPepperNoise(tf.keras.layers.Layer): # Añade ruido sal y pimienta a la imagen
    def __init__(self, amount_delta=0.05, salt_vs_pepper=0.5, seed=None, **kwargs):
        super().__init__(**kwargs)
        self.amount_delta = amount_delta
        self.salt_vs_pepper = salt_vs_pepper
        self.seed = seed
        self.params = {}

    def call(self, inputs, training=None):
        if  training:

            # Genera un porcentaje de cantidad de ruido aleatorio
            amount = tf.random.uniform([], 0.0, self.amount_delta, seed=self.seed)

            # Obtiene la forma de la imagen: [batch, height, width, channels] ([1,height, width, 3])
            input_shape = tf.shape(inputs)
            batch_size, height, width, channels = input_shape[0], input_shape[1], input_shape[2], input_shape[3]

            # Genera una máscara por píxel (sin canal): [batch, height, width, 1]
            rnd = tf.random.uniform(shape=[batch_size, height, width, 1], seed=self.seed)

            salt_mask = tf.cast(rnd < (amount * self.salt_vs_pepper), tf.float32)
            pepper_mask = tf.cast(rnd > 1 - (amount * (1 - self.salt_vs_pepper)), tf.float32)
            clean_mask = 1.0 - salt_mask - pepper_mask

            # Expande las máscaras a todos los canales
            salt_mask = tf.repeat(salt_mask, repeats=channels, axis=-1)
            pepper_mask = tf.repeat(pepper_mask, repeats=channels, axis=-1)
            clean_mask = tf.repeat(clean_mask, repeats=channels, axis=-1)

            # Aplica el ruido: sal = 1.0 (blanco), pimienta = 0.0 (negro)
            x = inputs * clean_mask + salt_mask * 1.0 + pepper_mask * 0.0

            self.params = {
                "amount": float(amount),
                "salt_vs_pepper": float(self.salt_vs_pepper)
            }

            return x
        else:
            return inputs
