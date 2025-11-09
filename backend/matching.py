"""
Resume-JD matching logic with multiple scoring methods.
Combines keyword matching, semantic similarity, and LLM-based analysis.
"""

import os
from typing import Dict, List, Tuple
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from models_cache import get_embedding_model
from sections import parse_resume_sections, parse_job_requirements
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def calculate_keyword_match_score(resume_data: Dict, jd_data: Dict) -> Tuple[float, List[str], List[str]]:
    """
    Calculate matching score based on keyword overlap.
    Returns score (0-100), matched skills, and missing skills.
    """
    resume_skills = set([s.lower() for s in resume_data['skills']])
    jd_skills = set([s.lower() for s in jd_data['skills']])
    
    if not jd_skills:
        return 0.0, [], []
    
    matched_skills = resume_skills.intersection(jd_skills)
    missing_skills = jd_skills - resume_skills
    
    # Calculate score based on matched skills
    match_percentage = (len(matched_skills) / len(jd_skills)) * 100
    
    # Convert back to original case for display
    matched_list = list(matched_skills)
    missing_list = list(missing_skills)
    
    return match_percentage, matched_list, missing_list

def calculate_semantic_similarity(resume_text: str, jd_text: str) -> float:
    """
    Calculate semantic similarity using sentence embeddings.
    Returns similarity score (0-100).
    """
    try:
        model = get_embedding_model()
        
        # Generate embeddings
        resume_embedding = model.encode([resume_text])
        jd_embedding = model.encode([jd_text])
        
        # Calculate cosine similarity
        similarity = cosine_similarity(resume_embedding, jd_embedding)[0][0]
        
        # Convert to percentage (0-100)
        similarity_score = float(similarity * 100)
        
        return similarity_score
    except Exception as e:
        print(f"Error calculating semantic similarity: {e}")
        return 0.0

def calculate_experience_score(resume_years: int, jd_years: int) -> float:
    """
    Calculate score based on experience years match.
    Returns score (0-100).
    """
    if jd_years == 0:
        return 100.0  # No specific requirement
    
    if resume_years >= jd_years:
        return 100.0
    elif resume_years >= jd_years * 0.8:
        return 80.0
    elif resume_years >= jd_years * 0.6:
        return 60.0
    else:
        return (resume_years / jd_years) * 50.0

def calculate_education_score(resume_education: List[str], jd_education: List[str]) -> float:
    """
    Calculate score based on education match.
    Returns score (0-100).
    """
    if not jd_education:
        return 100.0  # No specific requirement
    
    if not resume_education:
        return 0.0
    
    # Simple match: if any degree matches, give full score
    resume_edu_lower = [e.lower() for e in resume_education]
    jd_edu_lower = [e.lower() for e in jd_education]
    
    for req_edu in jd_edu_lower:
        for res_edu in resume_edu_lower:
            if req_edu in res_edu or res_edu in req_edu:
                return 100.0
    
    return 50.0  # Partial credit if education exists but doesn't match

def generate_suggestions(resume_data: Dict, jd_data: Dict, missing_skills: List[str]) -> List[str]:
    """
    Generate improvement suggestions based on gaps.
    Returns list of actionable suggestions.
    """
    suggestions = []
    
    # Missing skills suggestions
    if missing_skills:
        top_missing = missing_skills[:5]  # Top 5 most important
        suggestions.append(f"Add these key skills to your resume: {', '.join(top_missing)}")
    
    # Experience gap
    resume_exp = resume_data.get('experience_years', 0)
    jd_exp = jd_data.get('experience_years', 0)
    if jd_exp > 0 and resume_exp < jd_exp:
        suggestions.append(f"The role requires {jd_exp}+ years of experience. Highlight relevant projects or expand on your experience to meet this requirement.")
    
    # Education gap
    if jd_data.get('education') and not resume_data.get('education'):
        suggestions.append("Consider adding your education qualifications to match the job requirements.")
    
    # Certifications
    if jd_data.get('certifications') and not resume_data.get('certifications'):
        suggestions.append("The job mentions certifications. If you have relevant certifications, add them to your resume.")
    
    # Section improvements
    resume_sections = resume_data.get('sections', {})
    if 'summary' not in resume_sections:
        suggestions.append("Add a professional summary at the top highlighting your key skills and experience.")
    
    if 'projects' not in resume_sections:
        suggestions.append("Include a projects section to showcase practical application of your skills.")
    
    # Generic suggestions if no specific gaps
    if not suggestions:
        suggestions.append("Your resume is well-matched! Consider adding quantifiable achievements to stand out.")
        suggestions.append("Tailor your resume summary to emphasize the skills most relevant to this role.")
    
    return suggestions

def perform_matching(resume_text: str, jd_text: str) -> Dict:
    """
    Main function to perform resume-JD matching.
    Returns comprehensive matching results with scores and suggestions.
    """
    print("Parsing resume and job description...")
    
    # Parse both texts
    resume_data = parse_resume_sections(resume_text)
    jd_data = parse_job_requirements(jd_text)
    
    print(f"Found {len(resume_data['skills'])} skills in resume")
    print(f"Found {len(jd_data['skills'])} skills in JD")
    
    # Calculate different scores
    keyword_score, matched_skills, missing_skills = calculate_keyword_match_score(resume_data, jd_data)
    semantic_score = calculate_semantic_similarity(resume_text, jd_text)
    experience_score = calculate_experience_score(
        resume_data.get('experience_years', 0),
        jd_data.get('experience_years', 0)
    )
    education_score = calculate_education_score(
        resume_data.get('education', []),
        jd_data.get('education', [])
    )
    
    # Calculate weighted overall score
    overall_score = (
        keyword_score * 0.40 +      # 40% weight on skills match
        semantic_score * 0.30 +      # 30% weight on semantic similarity
        experience_score * 0.20 +    # 20% weight on experience
        education_score * 0.10       # 10% weight on education
    )
    
    # Generate suggestions
    suggestions = generate_suggestions(resume_data, jd_data, missing_skills)
    
    print(f"Overall matching score: {overall_score:.2f}%")
    
    return {
        'overall_score': round(overall_score, 2),
        'keyword_match_score': round(keyword_score, 2),
        'semantic_similarity_score': round(semantic_score, 2),
        'experience_score': round(experience_score, 2),
        'education_score': round(education_score, 2),
        'matched_skills': matched_skills[:20],  # Top 20
        'missing_skills': missing_skills[:20],   # Top 20
        'suggestions': suggestions,
        'resume_data': {
            'skills': resume_data['skills'][:30],
            'experience_years': resume_data.get('experience_years', 0),
            'education': resume_data.get('education', []),
            'certifications': resume_data.get('certifications', [])
        },
        'jd_data': {
            'skills': jd_data['skills'][:30],
            'experience_years': jd_data.get('experience_years', 0),
            'education': jd_data.get('education', []),
            'certifications': jd_data.get('certifications', [])
        }
    }

async def llm_enhanced_matching(resume_text: str, jd_text: str, provider: str = "openrouter") -> Dict:
    """
    Optional: Use LLM (OpenRouter or Gemini) for enhanced analysis.
    Returns additional insights from the LLM.
    """
    try:
        if provider == "openrouter":
            return await openrouter_analysis(resume_text, jd_text)
        elif provider == "gemini":
            return await gemini_analysis(resume_text, jd_text)
        else:
            return {"error": "Invalid provider"}
    except Exception as e:
        print(f"LLM analysis failed: {e}")
        return {"error": str(e)}

async def openrouter_analysis(resume_text: str, jd_text: str) -> Dict:
    """Use OpenRouter API for enhanced analysis."""
    try:
        import openai
        
        api_key = os.getenv("OpenRouter_API_Key")
        model = os.getenv("OpenRouter_LLM_model", "openai/gpt-3.5-turbo")
        
        if not api_key:
            return {"error": "OpenRouter API key not found"}
        
        client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        
        prompt = f"""Analyze this resume against the job description and provide insights:

JOB DESCRIPTION:
{jd_text[:1000]}

RESUME:
{resume_text[:1000]}

Provide:
1. Key strengths of the candidate
2. Main gaps or weaknesses
3. Top 3 specific recommendations
"""
        
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        
        return {
            "llm_insights": response.choices[0].message.content,
            "provider": "OpenRouter"
        }
    except Exception as e:
        return {"error": f"OpenRouter analysis failed: {str(e)}"}

async def gemini_analysis(resume_text: str, jd_text: str) -> Dict:
    """Use Google Gemini API for enhanced analysis."""
    try:
        import google.generativeai as genai
        
        api_key = os.getenv("Gemini_API_Key")
        model_name = os.getenv("Gemini_LLM_model", "gemini-pro")
        
        if not api_key:
            return {"error": "Gemini API key not found"}
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        
        prompt = f"""Analyze this resume against the job description and provide insights:

JOB DESCRIPTION:
{jd_text[:1000]}

RESUME:
{resume_text[:1000]}

Provide:
1. Key strengths of the candidate
2. Main gaps or weaknesses
3. Top 3 specific recommendations
"""
        
        response = model.generate_content(prompt)
        
        return {
            "llm_insights": response.text,
            "provider": "Gemini"
        }
    except Exception as e:
        return {"error": f"Gemini analysis failed: {str(e)}"}
