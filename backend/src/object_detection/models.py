import os
import sys
from ultralytics import YOLO

def get_models():
    """
    Load YOLO models for weapon and bag detection.
    """
    yolov11n_model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'models', 'weapons_n_bags', 'yolo11n.pt')

    custom_weapon_model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'models', 'weapons_n_bags', 'weapon_11m.pt')


    if not os.path.exists(custom_weapon_model_path) or not os.path.exists(yolov11n_model_path):
        print('❌ One or both model paths are invalid.')
        sys.exit(1)

    model1 = YOLO(custom_weapon_model_path)
    model2 = YOLO(yolov11n_model_path)

    labels1 = model1.names
    labels2 = model2.names

    return model1, model2, labels1, labels2
