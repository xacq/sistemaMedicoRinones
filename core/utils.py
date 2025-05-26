# ssmedico/utils.py
import pickle
from PIL import Image
import numpy as np
import os

def cargar_modelo():
    ruta_modelo = os.path.join('model', 'modelo_entrenado.pkl')
    with open(ruta_modelo, 'rb') as archivo:
        modelo = pickle.load(archivo)
    return modelo

def procesar_imagen(imagen):
    # Convertir la imagen a escala de grises y redimensionar
    imagen = imagen.convert('L')
    imagen = imagen.resize((128, 128))
    # Convertir la imagen a un array de numpy
    imagen_array = np.array(imagen).flatten()
    return imagen_array
