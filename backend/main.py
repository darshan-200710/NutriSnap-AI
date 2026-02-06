from fastapi import FastAPI, UploadFile, File, HTTPException
# Force reload to pick up new .env changes
from backend.models import AnalysisResponse, NutritionInfo
from backend.integration import FitnessIntegration
from backend.firebase_utils import db
from ai_core.gemini_client import analyze_food_image
# from ai_core.openai_client import analyze_food_image
# from ai_core.groq_client import analyze_food_image
import shutil
import os
from datetime import datetime

app = FastAPI(title="Food Vision API")

@app.get("/")
def read_root():
    return {"status": "online", "message": "Food Vision Backend is Running"}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_food(file: UploadFile = File(...), user_id: str = "demo_user"):
    """
    Receives an image, processing it via AI, 
    saves to Firebase, and syncs with Fitness Platform.
    """
    
    # 1. Save temp file
    temp_filename = f"temp_{file.filename}"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # 2. Call AI
    ai_result = analyze_food_image(temp_filename)
    # Use Groq result if available; on error return HTTP 502
    if "error" in ai_result:
        print(f"AI Error: {ai_result.get('error')}")
        raise HTTPException(status_code=502, detail=f"AI analysis failed: {ai_result.get('error')}")

    # Build nutrition model from AI result
    nutrition_data = ai_result
    nutrition_info = NutritionInfo(**nutrition_data)
    final_message = "Food analyzed successfully"

    # 3. Store in Firebase

    
    # 3. Store in Firebase
    try:
        if db:
            doc_ref = db.collection(u'food_logs').document()
            doc_ref.set({
                u'user_id': user_id,
                u'food_name': nutrition_info.food_name,
                u'calories': nutrition_info.calories,
                u'timestamp': datetime.now(),
                u'nutrition': nutrition_info.dict()
            })
    except Exception as e:
        print(f"\n[WARNING] Database Write Failed: {e}")
        print("Continuing without saving to DB (Hackathon Mode)\n")
    
    # 4. Integrate with Fitness Platform
    sync_result = FitnessIntegration.sync_workout(
        user_id=user_id, 
        calories=nutrition_info.calories, 
        protein=nutrition_info.protein_g
    )
    
    # Clean up
    if os.path.exists(temp_filename):
        os.remove(temp_filename)
        
    return AnalysisResponse(
        nutrition=nutrition_info,
        message=final_message,
        fitness_sync_status=sync_result
    )

@app.get("/history/{user_id}")
async def get_history(user_id: str):
    """
    Fetches food history for a specific user from Firebase.
    """
    if not db:
        raise HTTPException(status_code=503, detail="Database not initialized")
        
    try:
        logs_ref = db.collection(u'food_logs')
        query = logs_ref.where(u'user_id', u'==', user_id).order_by(u'timestamp', direction=firestore.Query.DESCENDING).limit(10)
        docs = query.stream()
        
        history = []
        for doc in docs:
            log_data = doc.to_dict()
            # Convert datetime to string for JSON serialization
            if 'timestamp' in log_data and log_data['timestamp']:
                log_data['timestamp'] = log_data['timestamp'].isoformat()
            history.append(log_data)
            
        return {"user_id": user_id, "history": history}
    except Exception as e:
        print(f"Error fetching history: {e}")
        # Fallback if index is not created yet (Firestore requires indexes for where + order_by)
        try:
            docs = logs_ref.where(u'user_id', u'==', user_id).limit(10).stream()
            history = []
            for doc in docs:
                log_data = doc.to_dict()
                if 'timestamp' in log_data and log_data['timestamp']:
                    log_data['timestamp'] = log_data['timestamp'].isoformat()
                history.append(log_data)
            return {"user_id": user_id, "history": history, "note": "Simple query used (no ordering)"}
        except:
            raise HTTPException(status_code=500, detail=f"Failed to fetch history: {str(e)}")

# Ensure firestore is imported for DESCENDING
from firebase_admin import firestore
