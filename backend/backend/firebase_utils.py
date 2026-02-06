import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

load_dotenv()

def initialize_firebase():
    """Initializes Firebase Admin SDK and returns Firestore client."""
    cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "serviceAccountKey.json")
    
    try:
        if not firebase_admin._apps:
            if os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
                print(f"✅ Firebase initialized successfully with {cred_path}")
            else:
                print(f"⚠️ WARNING: {cred_path} not found. Firebase not initialized.")
                return None
        
        # This part only runs if initialization succeeded or already existed
        return firestore.client()
    except Exception as e:
        print(f"❌ Firebase Critical Error: {e}")
        return None

# Initialize on module load
db = initialize_firebase()
