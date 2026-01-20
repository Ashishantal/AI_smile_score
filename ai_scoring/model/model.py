import tensorflow as tf
import numpy as np
from PIL import Image
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "smile_cnn_model.keras")

# IMPORTANT: do NOT load model here
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
model = None


def get_model():
    global model
    if model is None:
        print("🔄 Loading ML model...")
        model = tf.keras.models.load_model(MODEL_PATH)
        print("✅ Model loaded successfully")
    return model


def predict_score(image_path):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((64, 64))

    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    model = get_model()   # load once
    prediction = model.predict(img_array)

    print("Raw model output:", prediction)

    score = round(float(prediction[0][0] * 100), 2)
    return score
