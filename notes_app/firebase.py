import firebase_admin
from firebase_admin import credentials
import os
from dotenv import load_dotenv

load_dotenv()

def initialize_firebase():
    cred_path= os.getenv('FIREBASE_CREDENTIALS_PATH')
    if not firebase_admin._apps:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)