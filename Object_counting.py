import cv2
import argparse

from ultralytics import YOLO

def parse_arguments():
    parser = argparse.ArgumentParser(description='YOLOv live')
    parser.add_argument('--web-resolution', default=[1200,720],nargs=2, type=int)

    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()
    frame_width,frame_height = args.web_resolution
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,frame_height)
    
    model = YOLO('yolov8l.pt')
    while True:
        ret, frame = cap.read()
        result = model(frame)
        cv2.imshow('yolov8', frame)

        if (cv2.waitKey(0) == 27):
            break



if __name__ == '__main__':
    main()
