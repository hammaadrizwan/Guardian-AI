import boto3
from utils.config import RECIPIENT_LIST
# # AWS SNS configuration (credentials should be configured via AWS CLI or environment variables)
# AWS_ACCESS_KEY_ID = 'AKIAXHB7CVFK7XWERS2V'  # Replace if not using AWS CLI
# AWS_SECRET_ACCESS_KEY = '+z8L3z+zbDq5DFj5uTr8nRtehyuagKLMe5md8f2w'  # Replace if not 

# # Initialize S3 client
# sns_client = boto3.client(
#     'sns',
#     aws_access_key_id=AWS_ACCESS_KEY_ID,
#     aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
#     region_name='ap-south-1'
# )

# PHONE_NUMBER = '+94774443366'  # Your registered phone number

# def send_notification(message):
#     """
#     Send an SMS notification to the specified phone number via Amazon SNS.
    
#     Args:
#         message: str, the text message to send (max 140 bytes for SMS)
#     """
#     try:
#         # Publish the message directly to the phone number
#         response = sns_client.publish(
#             PhoneNumber=PHONE_NUMBER,
#             Message=message,
#             MessageAttributes={
#                 'AWS.SNS.SMS.SenderID': {
#                     'DataType': 'String',
#                     'StringValue': 'GuardianAI'# Optional: Sender ID (may not work in all regions)
#                 },
#                 'AWS.SNS.SMS.SMSType': {
#                     'DataType': 'String',
#                     'StringValue': 'Promotional'  # Transactional for critical alerts
#                 }
#             }
#         )
#         print(f"SMS sent successfully: Message ID {response['MessageId']}")
#     except Exception as e:
#         print(f"Error sending SMS: {e}")
# notification
# bjwa imaq leds bktt
from email.mime.text import MIMEText
import smtplib


def send_notification(date, image_link, address):
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <h2 style="color: red;">⚠️ URGENT: THREAT DETECTED</h2>
        <p><strong>Address:</strong> {address}</p>
        <p><strong>Capture Time:</strong> {date}</p>
        <p><strong>Captured Frame:</strong> <a href="{image_link}" style="color: #d9534f;">View Image</a></p>
        <br>
        <p style="color: gray;">This is an automated alert from <strong>GuardianAI</strong>. Please respond immediately.</p>
    </body>
    </html>
    """

    recipients = RECIPIENT_LIST  # Make sure RECIPIENT_LIST is defined elsewhere
    msg = MIMEText(html_content, 'html')
    msg["Subject"] = "🚨 URGENT: THREAT DETECTED – IMMEDIATE ACTION REQUIRED"
    msg["To"] = ", ".join(recipients)
    msg["From"] = "agent.guardianai@gmail.com"

    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login("agent.guardianai@gmail.com", "bjwa imaq leds bktt")  # Consider using environment vars for security
    smtp_server.sendmail(msg["From"], recipients, msg.as_string())
    smtp_server.quit()