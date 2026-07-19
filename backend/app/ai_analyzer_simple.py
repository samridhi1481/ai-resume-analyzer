import re
from typing import Dict, List

class SimpleAIResumeAnalyzer:
    def __init__(self):
        pass
    
    def extract_structured_info(self, text: str) -> Dict:
        info = {
            "name": self._extract_name(text),
            "email": self._extract_email(text),
            "phone": self._extract_phone(text),
            "education": self._extract_education(text),
            "experience": self._extract_experience(text),
            "skills": self._extract_skills(text),
        }
        return info
    
    def _extract_name(self, text: str) -> str:
        lines = text.split('\n')
        for line in lines[:5]:
            line = line.strip()
            if line and len(line) < 40 and not any(x in line.lower() for x in ['email', 'phone', 'resume']):
                if any(c.isupper() for c in line) and ' ' in line:
                    return line
        return "Not Found"
    
    def _extract_email(self, text: str) -> str:
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(pattern, text)
        return emails[0] if emails else "Not Found"
    
    def _extract_phone(self, text: str) -> str:
        patterns = [
            r'\b\d{10}\b',
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            r'\b\+\d{1,3}\s?\d{10}\b'
        ]
        for pattern in patterns:
            phones = re.findall(pattern, text)
            if phones:
                return phones[0]
        return "Not Found"
    
    def _extract_education(self, text: str) -> List[str]:
        education_keywords = [
            'b.tech', 'b.e', 'b.sc', 'm.tech', 'm.sc', 'phd',
            'bachelor', 'master', 'university', 'college', 'institute',
            'school of', 'degree', 'diploma', 'certification'
        ]
        education = []
        lines = text.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in education_keywords):
                clean_line = line.strip()
                if len(clean_line) > 5:
                    education.append(clean_line)
        return education[:3] if education else ["No education found"]
    
    def _extract_experience(self, text: str) -> List[str]:
        experience_keywords = [
            'experience', 'intern', 'developer', 'engineer', 'analyst',
            'consultant', 'worked', 'internship', 'associate', 'trainee',
            'project', 'built', 'developed', 'created', 'implemented'
        ]
        experience = []
        lines = text.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in experience_keywords):
                if len(line.strip()) > 15:
                    experience.append(line.strip())
        return experience[:3] if experience else ["No experience found"]
    
    def _extract_skills(self, text: str) -> List[str]:
        common_skills = [
            'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php',
            'go', 'rust', 'swift', 'kotlin', 'typescript', 'c',
            'react', 'angular', 'vue', 'django', 'flask', 'spring',
            'node.js', 'express', 'rails', 'laravel', 'fastapi',
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle',
            'sqlite', 'firebase',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins',
            'terraform', 'ansible', 'git', 'ci/cd', 'github actions',
            'linux', 'unix', 'bash', 'shell',
            'machine learning', 'deep learning', 'nlp', 'natural language processing',
            'computer vision', 'reinforcement learning', 'transfer learning',
            'tensorflow', 'pytorch', 'keras', 'opencv', 'nltk', 'spacy',
            'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn',
            'plotly', 'jupyter', 'huggingface', 'transformers',
            'data science', 'data analytics', 'data analysis', 'data visualization',
            'power bi', 'tableau', 'excel', 'r', 'matlab', 'statistics',
            'leadership', 'communication', 'problem solving', 'teamwork',
            'project management', 'agile', 'scrum', 'mentoring'
        ]
        
        found_skills = []
        text_lower = text.lower()
        for skill in common_skills:
            if skill in text_lower:
                found_skills.append(skill)
        
        return list(set(found_skills))