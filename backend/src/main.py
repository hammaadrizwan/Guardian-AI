
import argparse
import cv2
from object_detection.models import get_models
from object_detection.real_time_detection import run_detection
from utils.camera import get_cctv_footage_info
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
    camera = get_cctv_footage_info(2)#1 for CAM_01, 2 for CAM_02
    video_path = camera["info"]["video_path"]
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print('❌ Invalid video path.')
        exit()
    source_type = 'video'
    print(f'🎥 Live Camera Feed: {video_path}')

# Set resolution
resW, resH = 640, 480
cap.set(3, resW)
cap.set(4, resH)

# Optional video recorder
recorder = None
if args.record:
    recorder = cv2.VideoWriter('demo1.avi', cv2.VideoWriter_fourcc(*'MJPG'), 30, (resW, resH))

# Run the detection loop
run_detection(cap, weapon_model, yolo11n, weapon_model_labels, yolo11n_labels, resW, resH, args.thresh,camera,recorder,no_display=args.no_display)

# Cleanup
cap.release()
if recorder:
    recorder.release()
cv2.destroyAllWindows()
