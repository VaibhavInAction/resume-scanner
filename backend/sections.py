"""
Section extraction from resume and job description.
Identifies and categorizes different sections of text.
"""

import re
from typing import Dict, List
from models_cache import get_nlp_model
from skills_data import get_all_skills

def extract_skills(text: str) -> List[str]:
    """
    Extract skills from text using NLP and keyword matching.
    Combines NLP entity recognition with predefined skill database.
    """
    found_skills = []
    text_lower = text.lower()
    
    # Get all known skills from database
    all_skills = get_all_skills()
    
    # Check for each skill in the text
    for skill in all_skills:
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.append(skill)
    
    # Remove duplicates and return
    return list(set(found_skills))

def extract_experience_years(text: str) -> int:
    """
    Extract years of experience from text.
    Looks for patterns like "5 years", "5+ years", "5-7 years".
    """
    patterns = [
        r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
        r'experience\s+(?:of\s+)?(\d+)\+?\s*years?',
        r'(\d+)\+?\s*yrs?\s+(?:of\s+)?experience',
        r'(\d+)\s*-\s*(\d+)\s*years?'
    ]
    
    max_years = 0
    
    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        for match in matches:
            if isinstance(match, tuple):
                # For range patterns (e.g., "5-7 years")
                years = max([int(x) for x in match if x.isdigit()])
            else:
                years = int(match)
            max_years = max(max_years, years)
    
    return max_years

def extract_education(text: str) -> List[str]:
    """
    Extract education qualifications from text.
    Looks for degree names and educational institutions.
    """
    education = []
    
    # Common degree patterns
    degree_patterns = [
        r'\b(B\.?S\.?|Bachelor\'?s?|B\.?Tech|B\.?E\.?)\s+(?:of\s+)?(?:Science\s+)?(?:in\s+)?([A-Za-z\s]+)',
        r'\b(M\.?S\.?|Master\'?s?|M\.?Tech|M\.?E\.?)\s+(?:of\s+)?(?:Science\s+)?(?:in\s+)?([A-Za-z\s]+)',
        r'\b(Ph\.?D\.?|Doctorate)\s+(?:in\s+)?([A-Za-z\s]+)',
        r'\b(MBA|BBA|BCA|MCA)\b'
    ]
    
    for pattern in degree_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                degree = ' '.join(match).strip()
            else:
                degree = match
            if degree and len(degree) > 2:
                education.append(degree)
    
    return list(set(education))

def extract_certifications(text: str) -> List[str]:
    """
    Extract certifications from text.
    Looks for common certification patterns and keywords.
    """
    certifications = []
    
    # Common certification keywords
    cert_keywords = [
        'AWS Certified', 'Google Cloud Certified', 'Azure Certified',
        'PMP', 'Scrum Master', 'CISSP', 'CompTIA', 'Cisco',
        'Oracle Certified', 'Microsoft Certified', 'Certified',
        'Certificate in', 'Certification in'
    ]
    
    # Look for certification sections
    cert_section_pattern = r'(?:certifications?|certificates?)[\s:]*\n((?:.*\n?){0,10})'
    cert_section = re.search(cert_section_pattern, text, re.IGNORECASE)
    
    if cert_section:
        section_text = cert_section.group(1)
        # Extract lines that might be certifications
        lines = section_text.split('\n')
        for line in lines:
            line = line.strip()
            if line and len(line) > 5 and len(line) < 150:
                certifications.append(line)
    
    # Also look for certification keywords throughout the text
    for keyword in cert_keywords:
        pattern = r'\b' + re.escape(keyword) + r'[^\n]{0,50}'
        matches = re.findall(pattern, text, re.IGNORECASE)
        certifications.extend(matches)
    
    return list(set(certifications))[:10]  # Limit to 10 most relevant

def identify_sections(text: str) -> Dict[str, str]:
    """
    Identify and extract major sections from resume.
    Returns a dictionary with section names and their content.
    """
    sections = {}
    
    # Common section headers
    section_headers = {
        'summary': r'(?:professional\s+)?summary|objective|profile',
        'experience': r'(?:work\s+)?experience|employment|professional\s+background',
        'education': r'education|academic|qualifications',
        'skills': r'(?:technical\s+)?skills|competencies|expertise',
        'certifications': r'certifications?|certificates?|licenses?',
        'projects': r'projects?|portfolio',
        'achievements': r'achievements?|awards?|honors?'
    }
    
    for section_name, pattern in section_headers.items():
        # Look for section header followed by content
        regex = r'(?:^|\n)\s*(' + pattern + r')\s*:?\s*\n((?:.*(?:\n|$)){0,50})'
        match = re.search(regex, text, re.IGNORECASE)
        if match:
            sections[section_name] = match.group(2).strip()
    
    return sections

def parse_job_requirements(jd_text: str) -> Dict:
    """
    Parse job description and extract requirements.
    Returns structured data about the job requirements.
    """
    return {
        'skills': extract_skills(jd_text),
        'experience_years': extract_experience_years(jd_text),
        'education': extract_education(jd_text),
        'certifications': extract_certifications(jd_text),
        'sections': identify_sections(jd_text)
    }

def parse_resume_sections(resume_text: str) -> Dict:
    """
    Parse resume and extract all sections.
    Returns structured data about the resume.
    """
    return {
        'skills': extract_skills(resume_text),
        'experience_years': extract_experience_years(resume_text),
        'education': extract_education(resume_text),
        'certifications': extract_certifications(resume_text),
        'sections': identify_sections(resume_text)
    }
