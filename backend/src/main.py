from object_detection.military_person_detection import is_military_person
import argparse
import cv2
from object_detection.models import get_models
from object_detection.real_time_detection import run_detection

# Argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--thresh', default=0.6, type=float, help='Minimum confidence threshold for displaying detected objects')
parser.add_argument('--record', action='store_true', help='Record results from video or webcam')
parser.add_argument('--webcam', action='store_true', help='Use webcam as input source')
parser.add_argument('--no-display', action='store_true', help='Disable display window')

args = parser.parse_args()


# Load models
weapon_model, yolo11n, weapon_model_labels, yolo11n_labels = get_models()

# Input source
if args.webcam:
    cap = cv2.VideoCapture(0)
    source_type = 'webcam'
    print('📷 Using webcam...')
else:
    video_path = '../../demonstration_data/videos/Unattended_Bag.mp4'
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print('❌ Invalid video path.')
        exit()
    source_type = 'video'
    print(f'🎥 Using video file: {video_path}')

# Set resolution
resW, resH = 640, 480
cap.set(3, resW)
cap.set(4, resH)

# Optional video recorder
recorder = None
if args.record:
    recorder = cv2.VideoWriter('demo1.avi', cv2.VideoWriter_fourcc(*'MJPG'), 30, (resW, resH))

# Run the detection loop
run_detection(cap, weapon_model, yolo11n, weapon_model_labels, yolo11n_labels, resW, resH, args.thresh, recorder,no_display=args.no_display)

# Cleanup
cap.release()
if recorder:
    recorder.release()
cv2.destroyAllWindows()



# # this is activated only if a weapon is detected

# IMG_SIZE = 32  

# MODEL_PATH = "/Users/hammaad/EdgeAI-1/backend/models/military_person_identification/military_classifier_50_epoch.keras"
# TEST_IMAGE_PATH = "/Users/hammaad/EdgeAI-1/demonstration_data/images/military.jpg"

# result = is_military_person(TEST_IMAGE_PATH, MODEL_PATH, IMG_SIZE)
# if result:
#     print("The image contains a military person.")
# else:
#     print("The image does not contain a military person.")