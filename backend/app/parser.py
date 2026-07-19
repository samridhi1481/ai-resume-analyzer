import fitz
import re

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_contact_info(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    
    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)
    
    return {
        "emails": emails,
        "phones": phones
    }

def extract_skills(text):
    common_skills = [
        'python', 'java', 'javascript', 'react', 'node.js', 'sql',
        'machine learning', 'deep learning', 'nlp', 'data science',
        'aws', 'azure', 'docker', 'kubernetes', 'git',
        'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy'
    ]
    
    found_skills = []
    text_lower = text.lower()
    for skill in common_skills:
        if skill in text_lower:
            found_skills.append(skill)
    
    return found_skills