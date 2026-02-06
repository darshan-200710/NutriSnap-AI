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

@app.get("/coach/{user_id}")
async def get_coaching(user_id: str):
    """
    Analyzes user history and provides coaching insights and meal suggestions.
    """
    if not db:
        raise HTTPException(status_code=503, detail="Database not initialized")
        
    try:
        # 1. Fetch recent history
        logs_ref = db.collection(u'food_logs')
        docs = logs_ref.where(u'user_id', u'==', user_id).order_by(u'timestamp', direction=firestore.Query.DESCENDING).limit(10).stream()
        
        history_summary = []
        total_calories = 0
        for doc in docs:
            data = doc.to_dict()
            food_name = data.get('food_name', 'Unknown')
            calories = data.get('calories', 0)
            total_calories += calories
            history_summary.append(f"- {food_name}: {calories} kcal")
            
        if not history_summary:
            return {
                "insight": "I need to see some of your meals before I can give advice. Start by analyzing a food photo!",
                "suggestions": ["Upload your first meal!", "Take a photo of your breakfast", "Track a snack"]
            }

        # 2. Call AI for coaching
        history_str = "\n".join(history_summary)
        prompt = f"""
        You are an expert Nutrition Coach. Based on the user's recent food history:
        {history_str}
        
        Total Calories in last 10 meals: {total_calories} kcal.
        
        Provide:
        1. A concise, encouraging 'Coach Insight' (max 2 sentences).
        2. Three specific 'Smart Meal Suggestions' for their next meal that would balance their diet.
        
        Return the result in strictly this JSON format:
        {{
            "insight": "your insight here",
            "suggestions": ["option 1", "option 2", "option 3"]
        }}
        """
        
        from ai_core.gemini_client import genai
        import json
        
        # ensure env is loaded
        from dotenv import load_dotenv
        load_dotenv(override=True)
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        # Clean and parse JSON
        text_response = response.text.replace("```json", "").replace("```", "").strip()
        result = json.loads(text_response)
        
        return result

    except Exception as e:
        print(f"Error in coaching: {e}")
        # Try a simpler query if ordering fails
        try:
             # Logic for simple coaching without ordering if firestore index is missing
             return {
                "insight": "You're doing a great job logging your food! Keep it up for more personalized insights.",
                "suggestions": ["Drink more water", "Eat more greens", "Try a high-protein breakfast"]
             }
        except:
            return {
                "insight": "I'm having a bit of trouble analyzing your data right now, but keep up the great work logging your meals!",
                "suggestions": ["Continue tracking your food", "Stay hydrated", "Aim for variety in your diet"]
            }

# Ensure firestore is imported for DESCENDING
from firebase_admin import firestore
