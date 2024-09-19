import os

# Check if GOOGLE_APPLICATION_CREDENTIALS is set
credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if credentials_path:
    print(f"Service Account Key Path: {credentials_path}")
else:
    print("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")