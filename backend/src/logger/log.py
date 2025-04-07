import boto3
from datetime import datetime

AWS_ACCESS_KEY_ID = 'AKIAXHB7CVFK7XWERS2V'  # Replace if not using AWS CLI
AWS_SECRET_ACCESS_KEY = '+z8L3z+zbDq5DFj5uTr8nRtehyuagKLMe5md8f2w'  # Replace if not using AWS CLI
S3_BUCKET_NAME = 'security-detection-images'

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def upload_to_s3(image, bucket_name=S3_BUCKET_NAME, folder='images'):
    """
    Upload an image to S3 with filename as current timestamp (dd_mm_yyyy_hh_mm_ss.jpg)
    inside the specified folder prefix.
    
    Args:
        image: numpy array (OpenCV image)
        bucket_name: str, S3 bucket name
        folder: str, folder prefix in S3 (e.g., 'images')
    """
    try:
        # Generate filename with current timestamp
        timestamp = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
        filename = f'{timestamp}.jpg'
        
        s3_key = f'{folder}/{filename}'

        s3_client.upload_file(image, bucket_name, s3_key)
        print(f"Uploaded {s3_key} to S3 bucket {bucket_name}")
        

    except Exception as e:
        print(f"Error uploading to S3: {e}")
