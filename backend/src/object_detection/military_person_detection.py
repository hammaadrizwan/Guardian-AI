#!/usr/bin/env python3

import tensorflow as tf
import numpy as np
import cv2
import os


def load_model(model_path):
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
    model = tf.keras.models.load_model(model_path)
    return model

# Preprocess an image for inference
def preprocess_image(image_path, IMG_SIZE):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found at {image_path}")
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Failed to load image at {image_path}")
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img / 255.0  # Normalize to [0, 1]
    img = img.astype(np.float32)  # Ensure float32
    return np.expand_dims(img, axis=0)  # Add batch dimension


def is_military_person(image_path,model_path,IMG_SIZE=32):
    """
    Function to determine if the image contains a military person.
    :param image_path: Path to the image file
    :return: True if military person, False otherwise
    """

    try:
        model = load_model(model_path)
        
        test_image = preprocess_image(image_path, IMG_SIZE)
        
        output = model.predict(test_image)
        
        prediction = True if output[0][0] > 0.5 else False

        return prediction

    except Exception as e:
        print(f"Error: {e}")

        return False



