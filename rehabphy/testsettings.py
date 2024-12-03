import smtplib
from email.mime.text import MIMEText

# Email settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'rehabphyproject@gmail.com'  
EMAIL_HOST_PASSWORD = 'uqwguppgnjpegbbj'  

# Create the email message
msg = MIMEText('This is a test email.')
msg['Subject'] = 'Test Email'
msg['From'] = EMAIL_HOST_USER
msg['To'] = 'angelocarramona@hotmail.com'  

try:
    # Setup the server connection
    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.starttls()  # Start TLS for security
    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)  # Login to your email account
    server.sendmail(EMAIL_HOST_USER, [msg['To']], msg.as_string())  # Send the email
    server.quit()  # Close the server connection
    print("Email sent successfully")
except Exception as e:
    print(f"Failed to send email: {e}")
