from utils.config import RECIPIENT_LIST

from email.mime.text import MIMEText
import smtplib


def send_notification(date, image_link, address):
    """
    Send an email notification with the captured image and details.
    Args:
        date (str): The date of the capture.
        image_link (str): The link to the captured image.
        address (str): The address of the camera.
    """
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

    recipients = RECIPIENT_LIST  
    msg = MIMEText(html_content, 'html')
    msg["Subject"] = "🚨 URGENT: THREAT DETECTED – IMMEDIATE ACTION REQUIRED"
    msg["To"] = ", ".join(recipients)
    msg["From"] = "agent.guardianai@gmail.com"

    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login("agent.guardianai@gmail.com", "bjwa imaq leds bktt") 
    smtp_server.sendmail(msg["From"], recipients, msg.as_string())
    smtp_server.quit()
