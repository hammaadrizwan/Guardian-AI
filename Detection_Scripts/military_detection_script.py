import cv2
import torch
import numpy as np
from torchvision import transforms
from PIL import Image

# Load YOLO models
weapon_model = torch.hub.load('ultralytics/yolo11s', 'custom', path="weapon_model.pt") # load the trained weapon model
person_model = torch.hub.load('ultralytics/yolo11s', 'yolo11s') # load the pre- trained model for person detection

# load military uniform classifier (Assumes a Res-Net based classifier is trained)
uniform_classifier = torch.load('uniform_classifier.pth')
uniform_classifier.eval()

# Image Transform for uniform classification
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

def detect_objects(model, img):
    results = model(img)
    return results.pandas().xyxy[0]  # Get bounding boxes

def is_military_person(person_crop):
    img = Image.fromarray(cv2.cvtColor(person_crop, cv2.COLOR_BGR2RGB))
    img = transform(img).unsqueeze(0)
    with torch.no_grad():
        output = uniform_classifier(img)
        _, pred = torch.max(output, 1)
    return pred.item() == 1  # Assuming 1 represents military personnel

def process_frame(frame):
    weapon_detections = detect_objects(weapon_model, frame)
    person_detections = detect_objects(person_model, frame)
    
    for _, weapon in weapon_detections.iterrows():
        weapon_x1, weapon_y1, weapon_x2, weapon_y2 = map(int, [weapon['xmin'], weapon['ymin'], weapon['xmax'], weapon['ymax']])
        
        for _, person in person_detections.iterrows():
            person_x1, person_y1, person_x2, person_y2 = map(int, [person['xmin'], person['ymin'], person['xmax'], person['ymax']])
            
            # Check if weapon is within the person's bounding box
            if person_x1 < weapon_x1 < person_x2 and person_y1 < weapon_y1 < person_y2:
                person_crop = frame[person_y1:person_y2, person_x1:person_x2]
                if not is_military_person(person_crop):
                    print("ALERT: Non-military person with a weapon detected!")
                    cv2.rectangle(frame, (person_x1, person_y1), (person_x2, person_y2), (0, 0, 255), 2)  # Red box for alert
                else:
                    cv2.rectangle(frame, (person_x1, person_y1), (person_x2, person_y2), (0, 255, 0), 2)  # Green box for military
    return frame

# Video capture
cap = cv2.VideoCapture(0)  # Use webcam or video file
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    processed_frame = process_frame(frame)
    cv2.imshow('Weapon Detection', processed_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()