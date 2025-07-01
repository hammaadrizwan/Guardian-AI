import boto3
from datetime import datetime
import os
import csv

AWS_ACCESS_KEY_ID = 'AWS_ACCESS_KEY_ID' 
AWS_SECRET_ACCESS_KEY = 'AWS_SECRET_ACCESS_KEY' 
S3_BUCKET_NAME = 'security-detection-images'
AWS_REGION = 'ap-south-1'  

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='ap-south-1'
)

def upload_image_to_s3(image, bucket_name=S3_BUCKET_NAME, folder='images'):
    """
    Upload an image to S3 with filename as current timestamp (dd_mm_yyyy_hh_mm_ss.jpg)
    inside the specified folder prefix.
    
    Args:
        image: numpy array (OpenCV image)
        bucket_name: str, S3 bucket name
        folder: str, folder prefix in S3 (e.g., 'images')
    """
    try:
        timestamp = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
        filename = f'{timestamp}.jpg'
        
        s3_key = f'{folder}/{filename}'

        s3_client.upload_file(image, bucket_name, s3_key)
        print(f"Uploaded {s3_key} to S3 bucket {bucket_name}")
        return f"https://{bucket_name}.s3.amazonaws.com/{s3_key}"

    except Exception as e:
        print(f"Error uploading to S3: {e}")

def append_csv_to_s3(date, time_str, image_link, location, bucket_name=S3_BUCKET_NAME, csv_filename='detection_logs.csv'):
    """
    Append a log entry to a CSV file and upload it to S3 at the root level.
    
    Args:
        date: str, date in 'dd_mm_yyyy' format
        time_str: str, time in 'hh_mm_ss' format
        image_link: str, S3 URL of the image
        location: str, location of detection
        bucket_name: str, S3 bucket name
        csv_filename: str, name of the CSV file (e.g., 'detection_logs.csv')
    
    Returns:
        str: Full S3 URL of the updated CSV file
    """
    try:
        temp_csv = f'/tmp/{csv_filename}'
        s3_key = csv_filename

        try:
            s3_client.download_file(bucket_name, s3_key, temp_csv)
            existing_data = True
        except s3_client.exceptions.NoSuchKey:
            existing_data = False

        # Append to the CSV
        with open(temp_csv, 'a' if existing_data else 'w', newline='') as f:
            writer = csv.writer(f)
            if not existing_data:
                writer.writerow(['date', 'time', 'image_link', 'location'])
            writer.writerow([date, time_str, image_link, location])

        s3_client.upload_file(temp_csv, bucket_name, s3_key)
        print(f"Appended to {s3_key} in S3 bucket {bucket_name}")

        os.remove(temp_csv)

        s3_url = f'https://{bucket_name}.s3.{AWS_REGION}.amazonaws.com/{s3_key}'
        return s3_url
    except Exception as e:
        print(f"Error appending to S3 CSV: {e}")
        return None
