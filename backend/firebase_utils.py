import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

load_dotenv()

def initialize_firebase():
    """Initializes Firebase Admin SDK and returns Firestore client."""
    cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "serviceAccountKey.json")
    
    if not firebase_admin._apps:
        if os.path.exists(cred_path):
            try:
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
                print(f"✅ Firebase initialized successfully with {cred_path}")
            except Exception as e:
                print(f"❌ Firebase initialization failed: {e}")
                return None
        else:
            print(f"⚠️ WARNING: {cred_path} not found. Firebase not initialized.")
            return None
            
    client = firestore.client()
    print("🔥 Firestore client connected.")
    return client

# Initialize on module load or create a singleton
db = initialize_firebase()
