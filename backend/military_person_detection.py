import tensorflow as tf
import numpy as np
import cv2

MODEL_PATH = "/Users/hammaad/EdgeAI-1/backend/models/military_person_identification/military_classifier_50_epoch.keras"  
IMAGE_PATH = "/Users/hammaad/EdgeAI-1/demonstration_data/images/military.jpg"                   
IMG_SIZE = 224                                   


model = tf.keras.models.load_model(MODEL_PATH)

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img / 255.0  
    img = img.astype(np.float32)
    return np.expand_dims(img, axis=0)

input_image = preprocess_image(IMAGE_PATH)
output = model.predict(input_image)

label = "Military Person" if output[0][0] > 0.5 else "Person"
confidence = output[0][0]
print(f"Prediction: {label} (Confidence: {confidence:.2f})")
