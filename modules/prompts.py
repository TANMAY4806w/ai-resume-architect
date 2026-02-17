"""
Centralized prompts for the AI Resume Agent.
"""

def get_score_prompt(resume_text, job_description):
    """Returns the prompt for the keyword scoring (AI Scorer)."""
    return f"""Evaluate the match between the resume and the job description on a scale of 0-100.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Return ONLY a JSON object (no markdown, no extra text) with this structure:
{{
    "score": <number 0-100>,
    "missing": ["list", "of", "missing", "crucial", "keywords"]
}}
"""

def get_enhancement_prompt(original_text, job_description, missing_keywords=None):
    """Returns the prompt for the resume enhancement task."""
    
    keywords_instruction = ""
    if missing_keywords:
        # Filter for meaningful keywords (simple heuristic)
        filtered = [k for k in missing_keywords if len(k) > 2]
        if filtered:
            keywords_instruction = f"""
CRITICAL TASK:
The following keywords are missing from the resume but are important for the job:
{', '.join(filtered[:15])}

Your goal is to NATURALLY incorporate these keywords into the resume content where they are contextually relevant and truthful.
- DO NOT force them in if they don't fit.
- DO NOT invent false experiences.
- Track which ones you added in the 'keywords_added' field.
"""

    return f"""You are an expert Resume Optimizer. Your goal is to rewrite the resume to be more impactful and ATS-friendly, targeting the specific job description provided.

{keywords_instruction}

INPUTS:
1. ORIGINAL RESUME:
{original_text}

2. JOB DESCRIPTION:
{job_description}

OUTPUT FORMAT:
Return ONLY a valid JSON object with the following structure. Do not include markdown formatting (like ```json).

{{
    "name": "Candidate Name",
    "email": "email@example.com",
    "phone": "Phone Number",
    "linkedin": "LinkedIn URL (if found)",
    "github": "GitHub URL (if found)",
    "website": "Website URL (if found)",
    "summary": "A powerful, professional summary optimized for the target role...",
    "experience": [
        {{
            "title": "Job Title",
            "company": "Company Name",
            "dates": "Date Range",
            "bullets": [
                "Action-oriented bullet point 1 using keywords...",
                "Quantifiable achievement 2..."
            ]
        }}
    ],
    "education": [
        {{
            "school": "University Name",
            "degree": "Degree",
            "year": "Year",
            "gpa": "GPA (optional)"
        }}
    ],
    "skills": [
         {{ "category": "Languages", "items": "Python, Java..." }},
         {{ "category": "Frameworks", "items": "React, Flask..." }}
    ],
    "projects": [
        {{
            "name": "Project Name",
            "link": "Project URL",
            "description": "Brief description highlighting tech stack and impact"
        }}
    ],
    "keywords_added": ["list", "of", "keywords", "you", "successfully", "integrated"],
    "keywords_skipped": [
        {{ "keyword": "skipped_keyword", "reason": "Not relevant/truthful" }}
    ]
}}
"""
