import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
from modules.prompts import get_enhancement_prompt

# Load environment variables
load_dotenv()

# Configure API
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def enhance_resume_content(original_text, job_description, missing_keywords=None):
    """
    Enhances resume content using Gemini AI with intelligent keyword injection.
    """
    try:
        # Use Flash for speed/cost, fallback to Pro
        try:
            model = genai.GenerativeModel('gemini-flash-latest')
        except:
            model = genai.GenerativeModel('gemini-pro')
        
        # Get the centralized prompt
        prompt = get_enhancement_prompt(original_text, job_description, missing_keywords)
        
        response = model.generate_content(
            prompt,
            generation_config={'response_mime_type': 'application/json'}
        )
        
        text = response.text
        # Clean up if the model adds markdown code blocks (even with mime type it sometimes happens)
        clean_text = text.replace("```json", "").replace("```", "").strip()
        
        if "{" in clean_text:
            clean_text = clean_text[clean_text.find("{"):]
        if "}" in clean_text:
            clean_text = clean_text[:clean_text.rfind("}")+1]
            
        data = json.loads(clean_text)
        
        # Ensure default fields exist
        data.setdefault('keywords_added', [])
        data.setdefault('keywords_skipped', [])
            
        return data
        
    except json.JSONDecodeError as e:
        return {
            "error": f"Failed to parse AI response as JSON: {str(e)}", 
            "raw": response.text if 'response' in locals() else "No response"
        }
    except Exception as e:
        return {
            "error": f"Enhancement failed: {str(e)}", 
            "raw": str(e)
        }
