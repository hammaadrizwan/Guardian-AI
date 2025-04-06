from object_detection.military_person_detection import is_military_person

IMG_SIZE = 32  

MODEL_PATH = "/Users/hammaad/EdgeAI-1/backend/models/military_person_identification/military_classifier_50_epoch.keras"
TEST_IMAGE_PATH = "/Users/hammaad/EdgeAI-1/demonstration_data/images/military.jpg"


result = is_military_person(TEST_IMAGE_PATH, MODEL_PATH, IMG_SIZE)
if result:
    print("The image contains a military person.")
else:
    print("The image does not contain a military person.")