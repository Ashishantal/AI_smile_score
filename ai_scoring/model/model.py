import tensorflow as tf
import numpy as np
from PIL import Image
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "smile_cnn_model.keras")

model = tf.keras.models.load_model(MODEL_PATH)

def predict_score(image_path):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((64, 64))

    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)

    print("Raw model output:", prediction)
    score = round(float(prediction[0][0] * 100), 2)
    return score
