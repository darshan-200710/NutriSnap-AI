from google import genai
from google.genai import types
import os
import json
from dotenv import load_dotenv
from ai_core.prompts import NUTRITION_PROMPT
from PIL import Image
import io

load_dotenv()

# Initialize Client (Best practice is to do this once or per request depending on architecture)
# Here we'll do it lazily in functions to allow env var loading
def get_client():
    load_dotenv(override=True)
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

def analyze_food_image(image_path):
    """
    Sends image to Gemini 1.5 Flash and returns parsed JSON.
    """
    client = get_client()
    if not client:
        return {"error": "API Key not found. Please add GOOGLE_API_KEY to .env"}

    # Define models to try
    models_to_try = ['gemini-2.0-flash-exp', 'gemini-1.5-flash', 'gemini-1.5-pro']
            
    # Read Image Bytes
    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
            
        # Create Part/Image object - specific to new SDK
        # For new SDK, we often just pass the bytes or specific types
        # Let's use simple bytes/mime_type dict or types.Part
        image_part = types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg") 
    except Exception as e:
        return {"error": f"Failed to read image file: {e}"}

    last_error = None
    
    for model_name in models_to_try:
        try:
            print(f"🤖 Trying AI Model: {model_name}...")
            
            # New SDK Call structure
            response = client.models.generate_content(
                model=model_name,
                contents=[NUTRITION_PROMPT, image_part]
            )
            
            if response.text:
                # Clean response
                text_response = response.text.replace("```json", "").replace("```", "").strip()
                return json.loads(text_response)
            else:
                 raise Exception("Empty response text")
            
        except Exception as e:
            print(f"❌ {model_name} Failed: {e}")
            last_error = e
            
    return {"error": f"All models failed. Last error: {str(last_error)}"}

def generate_text(prompt):
    """
    Sends text prompt to Gemini and returns string response.
    """
    client = get_client()
    if not client:
        return "Error: No API Key"
    
    models_to_try = ['gemini-2.0-flash-exp', 'gemini-1.5-flash', 'gemini-1.5-pro']

    for model_name in models_to_try:
        try:
            print(f"🤖 NutriChat trying: {model_name}")
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            return response.text.strip() if response.text else "No response generated."
        except Exception as e:
            print(f"❌ NutriChat {model_name} Fail: {e}")
            
    return "I'm sorry, I'm having trouble connecting to my AI brain right now. Please try again in a moment."

def analyze_audio(audio_bytes, mime_type="audio/wav", prompt=""):
    """
    Directly processes audio bytes with Gemini 1.5.
    """
    client = get_client()
    if not client:
        return "Error: No API Key"
    
    models_to_try = ['gemini-2.0-flash-exp', 'gemini-1.5-flash', 'gemini-1.5-pro']

    for model_name in models_to_try:
        try:
            print(f"🎙️ NutriVoice trying: {model_name}")
            
            # Construct Media Part
            audio_part = types.Part.from_bytes(data=audio_bytes, mime_type=mime_type)

            response = client.models.generate_content(
                model=model_name,
                contents=[prompt, audio_part]
            )
            return response.text.strip() if response.text else "I couldn't process the audio."
        except Exception as e:
            print(f"❌ NutriVoice {model_name} Fail: {e}")
            
    return "I couldn't hear you clearly. Could you please try recording again or typing your request?"
