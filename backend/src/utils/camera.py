cctv_footage_available = [
    {"name": "CAM_01",
     "info": {
            "video_path": "../../demonstration_data/videos/Unattended_Bag.mp4",
            "address": "Westminster, Underground Ltd, Westminster Station, Bridge St, London SW1A 2JR, United Kingdom",
            "location":"Westminister, UK"}},
            
    {"name": "CAM_02",
     "info": {
            "video_path": "../../demonstration_data/videos/Shooting.mp4",
            "address": "5161 San Felipe St, Houston, TX 77056, United States",
            "location":"Houston, USA"}}
]

def get_cctv_footage_info(number):
    if number < 1 or number > len(cctv_footage_available):
        raise ValueError("Invalid camera number. Please provide 1 or 2.")
    
    return cctv_footage_available[number - 1]