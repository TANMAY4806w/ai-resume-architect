import re
import os
import json
import time
import google.generativeai as genai
from collections import Counter
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    # Use a logger or silent fail in production, but print is fine for now
    print("⚠️ Warning: GEMINI_API_KEY not found.")

# Standard stopwords for ATS analysis
STOPWORDS = {
    "about", "above", "across", "after", "against", "along", "among", "apart", "around", "at", 
    "because", "before", "behind", "being", "below", "beneath", "beside", "between", "beyond", 
    "both", "but", "by", "can", "cannot", "come", "could", "did", "do", "does", "doing", "down", 
    "during", "each", "else", "even", "ever", "every", "for", "from", "get", "got", "had", "has", 
    "have", "he", "her", "here", "hers", "herself", "him", "himself", "his", "how", "if", "in", 
    "into", "is", "it", "its", "itself", "just", "kept", "know", "less", "let", "like", "likely", 
    "make", "many", "may", "me", "might", "more", "most", "much", "must", "my", "myself", "near", 
    "need", "no", "nor", "not", "now", "of", "off", "often", "on", "once", "one", "only", "or", 
    "other", "our", "ours", "ourselves", "out", "over", "own", "said", "same", "say", "see", 
    "shall", "she", "should", "since", "so", "some", "such", "than", "that", "the", "their", 
    "them", "then", "there", "these", "they", "this", "those", "through", "to", "too", "towards", 
    "under", "until", "up", "upon", "us", "use", "used", "uses", "very", "want", "was", "way", 
    "we", "well", "were", "what", "when", "where", "which", "while", "who", "whom", "whose", 
    "why", "will", "with", "within", "without", "would", "yes", "yet", "you", "your", "yours", 
    "yourself", "job", "description", "requirements", "role", "overview", "responsibilities", 
    "qualifications", "looking", "seeking", "must", "have", "ability", "experience", "year", 
    "years", "work", "team", "skills", "using", "strong", "proficient", "knowledge", "creating", 
    "working", "candidate", "ideal", "opportunity"
}

def extract_keywords(text):
    """Extracts keywords from text, removing stopwords and non-alphanumeric chars."""
    if not text:
        return []
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    words = text.split()
    keywords = [w for w in words if w not in STOPWORDS and len(w) > 1]
    return sorted(list(set(keywords)))

def calculate_ats_score(resume_text, job_desc_text):
    """Calculates a simple keyword match score."""
    resume_keywords = set(extract_keywords(resume_text))
    jd_keywords = set(extract_keywords(job_desc_text))
    
    if not jd_keywords:
        return 0, []
        
    matches = resume_keywords.intersection(jd_keywords)
    missing = jd_keywords - resume_keywords
    score = (len(matches) / len(jd_keywords)) * 100
    
    return round(score, 2), list(missing)

def calculate_ai_score(resume_text, job_desc):
    """
    Calculates ATS score using Gemini AI for context-aware matching.
    """
    # Truncate inputs if too long
    max_length = 4000
    resume_truncated = resume_text[:max_length]
    job_truncated = job_desc[:max_length]
    
    # Simple prompt for scoring, keeping it inline as it's small/specific
    prompt = f"""Evaluate the resume match to the job description (0-100).
JOB: {job_truncated}
RESUME: {resume_truncated}
Return JSON: {{"score": 85, "missing": ["skill1", "skill2"]}}"""

    for attempt in range(2):
        try:
            # Try efficient model first
            try:
                model = genai.GenerativeModel('gemini-flash-latest')
            except:
                model = genai.GenerativeModel('gemini-pro')
            
            response = model.generate_content(
                prompt,
                generation_config={'temperature': 0.1, 'response_mime_type': 'application/json'}
            )
            
            if not response.text:
                continue
                
            data = json.loads(response.text)
            return data.get("score", 0), data.get("missing", [])
            
        except Exception as e:
            if attempt == 0:
                time.sleep(1)
                continue
            print(f"AI Scoring failed: {e}")
            
    return 0, []
