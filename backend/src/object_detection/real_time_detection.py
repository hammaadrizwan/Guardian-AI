import time
import cv2
import os
import numpy as np
from logger.log import upload_to_s3
from object_detection.military_person_detection import is_military_person
# Allowed labels to draw
ALLOWED_LABELS = {'person', 'gun', 'heavy-gun', 'suitcase', 'handbag','bag'}

def is_bag_unattended(bag, people_locations, min_distance=150):
    bag_x, bag_y, bag_w, bag_h = bag
    bag_center = (bag_x + bag_w // 2, bag_y + bag_h // 2)

    min_dist = float('inf')
    nearest_person = None

    for person in people_locations:
        distance = np.linalg.norm(np.array(bag_center) - np.array(person))
        if distance < min_dist:
            min_dist = distance
            nearest_person = person

    return min_dist, nearest_person

def run_detection(cap, model1, model2, labels1, labels2, resW, resH, min_thresh, recorder=None,no_display=False):
    bbox_colors1 = (0, 255, 0)  # Green
    bbox_colors2 = (0, 0, 255)  # Red
    frame_rate_buffer = []
    fps_avg_len = 100

    unattended_bag_time = {}  # Dictionary to track time when a bag was unattended
    weapon_time = False  # Track if weapon is detected for 4 seconds

    while True:
        t_start = time.perf_counter()
        ret, frame = cap.read()
        if not ret:
            print('⚠️ No more frames or failed to capture from source.')
            break

        frame_resized = cv2.resize(frame, (resW, resH))
        results1 = model1(frame_resized, verbose=False)
        results2 = model2(frame_resized, verbose=False)

        detections1 = results1[0].boxes
        detections2 = results2[0].boxes

        object_count = 0
        people_locations = []
        bags_locations = []

        # Process model1 detections
        for det in detections1:
            xyxy = det.xyxy.cpu().numpy().squeeze().astype(int)
            conf = det.conf.item()
            classidx = int(det.cls.item())
            label = labels1[classidx]

            if conf > min_thresh and label in ALLOWED_LABELS:
                xmin, ymin, xmax, ymax = xyxy
                cv2.rectangle(frame_resized, (xmin, ymin), (xmax, ymax), bbox_colors1, 2)
                cv2.putText(frame_resized, f'{label}: {int(conf * 100)}%', (xmin, ymin - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, bbox_colors1, 2)
                object_count += 1

                # # cv2.circle(frame_resized, (center_x, center_y), 5, (0, 255, 0), -1)

                if label in ['gun', 'heavy-gun'] and conf >= 0.56:
                    cv2.putText(frame_resized, f'{label}: {int(conf * 100)}%', (xmin, ymin - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    
                    #save the frame
                    cv2.imwrite('detected_frame.jpg', frame_resized)
                    IMG_SIZE = 32  

                    MODEL_PATH = "/Users/hammaad/EdgeAI-1/backend/models/military_person_identification/military_classifier_50_epoch.keras"

                    result = is_military_person('detected_frame.jpg', MODEL_PATH, IMG_SIZE)
                    if result:
                        print("The image contains a military person.")
                    else:
                        upload_to_s3('detected_frame.jpg')
                        print("Image Uploaded")
                    #delete the image after uploading
                    os.remove('detected_frame.jpg')


        # Process model2 detections
        for det in detections2:
            xyxy = det.xyxy.cpu().numpy().squeeze().astype(int)
            conf = det.conf.item()
            classidx = int(det.cls.item())
            label = labels2[classidx]

            if conf > min_thresh and label in ALLOWED_LABELS:
                xmin, ymin, xmax, ymax = xyxy
                cv2.rectangle(frame_resized, (xmin, ymin), (xmax, ymax), bbox_colors2, 2)
                cv2.putText(frame_resized, f'{label}: {int(conf * 100)}%', (xmin, ymin - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, bbox_colors2, 2)
                object_count += 1


                center_x = xmin + (xmax - xmin) // 2
                center_y = ymin + (ymax - ymin) // 2
                if label == 'person':
                    people_locations.append((center_x, center_y))
                elif label in ['suitcase', 'handbag','bag']:
                    bags_locations.append((xmin, ymin, xmax - xmin, ymax - ymin))
        # Check unattended bags
        for bag in bags_locations:
            dist, nearest_person = is_bag_unattended(bag, people_locations)
            bag_center = (bag[0] + bag[2] // 2, bag[1] + bag[3] // 2)

            if dist > 150:
                if bag not in unattended_bag_time:
                    unattended_bag_time[bag] = time.time()
                # If the bag has been unattended for more than 5 seconds
                if time.time() - unattended_bag_time[bag] > 5:
                    cv2.putText(frame_resized, 'Unattended', (bag_center[0], bag_center[1] - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    
                    cv2.imwrite('detected_frame.jpg', frame_resized)

                    upload_to_s3('detected_frame.jpg')
                    print("Image Uploaded")

                    os.remove('detected_frame.jpg')

                    
            else:
                if bag in unattended_bag_time:
                    del unattended_bag_time[bag]  # Reset if the bag is no longer unattended

        # Show FPS
        t_stop = time.perf_counter()
        fps = 1 / (t_stop - t_start)
        frame_rate_buffer.append(fps)
        if len(frame_rate_buffer) > fps_avg_len:
            frame_rate_buffer.pop(0)
        avg_frame_rate = np.mean(frame_rate_buffer)

        cv2.putText(frame_resized, f'FPS: {avg_frame_rate:.2f}', (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.putText(frame_resized, f'Objects: {object_count}', (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        if recorder:
            recorder.write(frame_resized)

        if not no_display:
            cv2.imshow('Dual YOLO Detection', frame_resized)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break


        # cv2.imshow('Dual YOLO Detection', frame_resized)
        # if cv2.waitKey(5) & 0xFF == ord('q'):
            # break
