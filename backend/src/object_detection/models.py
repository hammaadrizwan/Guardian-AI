import os
import sys
from ultralytics import YOLO

def get_models():
    custom_weapon_model_path = '/Users/hammaad/EdgeAI-1/backend/models/weapons_n_bags/weapon_11s.pt'
    yolov8n_model_path = '/Users/hammaad/EdgeAI-1/backend/models/weapons_n_bags/yolo11n.pt'

    if not os.path.exists(custom_weapon_model_path) or not os.path.exists(yolov8n_model_path):
        print('❌ One or both model paths are invalid.')
        sys.exit(1)

    model1 = YOLO(custom_weapon_model_path)
    model2 = YOLO(yolov8n_model_path)

    labels1 = model1.names
    labels2 = model2.names

    return model1, model2, labels1, labels2
