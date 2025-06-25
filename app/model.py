# app/model.py

import tensorflow as tf
import numpy as np
from PIL import Image
import io

#nombres de las clases
CLASS_NAMES = ['Hazardous', 'Organic', 'Recyclable', 'Non-Recyclable']


def load_model():
    """
    Carga el modelo guardado en models/greenvision_saved_model
    """
    return tf.keras.models.load_model("models/greenvision.h5", compile=False)


def preprocess_image(contents: bytes) -> np.ndarray:
    """
    Recibe el contenido bytes de la imagen, la convierte a RGB,
    la resizea y normaliza para que el modelo la procese.
    Devuelve un array con shape (1, 224, 224, 3).
    """
    img = Image.open(io.BytesIO(contents)).convert("RGB")
    img = img.resize((224, 224))            
    arr = np.array(img).astype(np.float32) / 255.0
    return np.expand_dims(arr, axis=0)
