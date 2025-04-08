import boto3

# AWS SNS configuration (credentials should be configured via AWS CLI or environment variables)
AWS_ACCESS_KEY_ID = 'AKIAXHB7CVFK7XWERS2V'  # Replace if not using AWS CLI
AWS_SECRET_ACCESS_KEY = '+z8L3z+zbDq5DFj5uTr8nRtehyuagKLMe5md8f2w'  # Replace if not 

# Initialize S3 client
sns_client = boto3.client(
    'sns',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='ap-south-1'
)

PHONE_NUMBER = '+94774443366'  # Your registered phone number

def send_notification(message):
    """
    Send an SMS notification to the specified phone number via Amazon SNS.
    
    Args:
        message: str, the text message to send (max 140 bytes for SMS)
    """
    try:
        # Publish the message directly to the phone number
        response = sns_client.publish(
            PhoneNumber=PHONE_NUMBER,
            Message=message,
            MessageAttributes={
                'AWS.SNS.SMS.SenderID': {
                    'DataType': 'String',
                    'StringValue': 'GuardianAI'# Optional: Sender ID (may not work in all regions)
                },
                'AWS.SNS.SMS.SMSType': {
                    'DataType': 'String',
                    'StringValue': 'Promotional'  # Transactional for critical alerts
                }
            }
        )
        print(f"SMS sent successfully: Message ID {response['MessageId']}")
    except Exception as e:
        print(f"Error sending SMS: {e}")

if __name__ == "__main__":
    # Test the function
    send_notification("Test message from Guardian-AI agent")