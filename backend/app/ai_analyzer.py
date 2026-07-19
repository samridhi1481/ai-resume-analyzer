"""
AI-Powered Resume Analyzer with Gemini API Integration
"""

import re
import json
from typing import Dict, List, Any
from google import genai  # Updated import
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class AIResumeAnalyzer:
    def __init__(self, gemini_api_key: str = None):
        # Initialize embedding model for semantic matching
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        
        # Initialize Gemini (if API key provided)
        if gemini_api_key:
            self.gemini_client = genai.Client(api_key=gemini_api_key)
            self.gemini_available = True
        else:
            self.gemini_available = False
        
        # Common skills database
        self.skills_db = {
            "programming_languages": ['python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'go', 'rust', 'swift', 'kotlin'],
            "frameworks": ['react', 'angular', 'vue', 'django', 'flask', 'spring', 'node.js', 'express', 'rails', 'laravel'],
            "databases": ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sqlite'],
            "cloud": ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins'],
            "ml_ai": ['machine learning', 'deep learning', 'nlp', 'computer vision', 'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy'],
            "soft_skills": ['leadership', 'communication', 'problem solving', 'teamwork', 'project management']
        }
        
        self.all_skills = [skill for skills in self.skills_db.values() for skill in skills]
    
    # ... (all other methods remain the same - _extract_name, _extract_email, etc.)
    
    def generate_resume_improvements(self, resume_text: str, job_text: str = None) -> Dict:
        """Generate AI-powered improvement suggestions"""
        improvements = {
            "formatting": [],
            "content": [],
            "keywords": [],
            "structure": []
        }
        
        # ... (existing formatting/content analysis code)
        
        # AI-powered suggestions (if Gemini is available)
        if self.gemini_available and job_text:
            try:
                prompt = f"""
                Analyze this resume for a {job_text} position and provide:
                1. 3 specific improvements to make the resume more effective
                2. 3 keywords that should be added
                3. 2 things to remove or change
                
                Resume: {resume_text[:3000]}
                """
                response = self.gemini_client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=prompt
                )
                improvements["ai_suggestions"] = response.text.split('\n')
            except Exception as e:
                improvements["ai_suggestions"] = [f"AI suggestions not available: {str(e)}"]
        
        return improvements
    
    def generate_interview_questions_advanced(self, role: str, difficulty: str = "medium", count: int = 5) -> List[Dict]:
        """Generate advanced interview questions using AI"""
        if self.gemini_available:
            try:
                prompt = f"""
                Generate {count} {difficulty} interview questions for a {role} position.
                For each question, provide:
                - The question
                - What to look for in the answer
                - Expected answer structure
                
                Format as JSON with fields: question, answer_hints, expected_points
                """
                response = self.gemini_client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=prompt
                )
                # For now, return structured questions
                # You can parse the response here
            except Exception as e:
                print(f"Error generating questions: {e}")
        
        # Fallback to predefined questions
        questions = {
            "technical": [
                {
                    "question": "Explain the difference between supervised and unsupervised learning.",
                    "answer_hints": "Focus on labeled vs unlabeled data, use cases",
                    "expected_points": ["Supervised uses labeled data", "Unsupervised finds patterns", "Examples"]
                },
                # ... other questions
            ]
        }
        
        return questions["technical"][:count]
    
     
    def extract_structured_info(self, text: str) -> Dict:
        """Extract structured information from resume text"""
        info = {
            "name": self._extract_name(text),
            "email": self._extract_email(text),
            "phone": self._extract_phone(text),
            "education": self._extract_education(text),
            "experience": self._extract_experience(text),
            "skills": self._extract_skills_advanced(text),
            "projects": self._extract_projects(text),
            "certifications": self._extract_certifications(text)
        }
        return info
    
    def _extract_name(self, text: str) -> str:
        """Extract name from resume using patterns"""
        # Look for name patterns (usually at top)
        lines = text.split('\n')[:5]
        for line in lines:
            line = line.strip()
            if line and len(line) < 40 and not any(x in line.lower() for x in ['email', 'phone', 'resume', 'curriculum']):
                # Check if it looks like a name (two words, capitalized)
                words = line.split()
                if 2 <= len(words) <= 4 and all(w[0].isupper() for w in words if w):
                    return line
        return "Not Found"
    
    def _extract_email(self, text: str) -> str:
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(pattern, text)
        return emails[0] if emails else "Not Found"
    
    def _extract_phone(self, text: str) -> str:
        patterns = [
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            r'\b\d{10}\b',
            r'\b\+\d{1,3}\s?\d{10}\b'
        ]
        for pattern in patterns:
            phones = re.findall(pattern, text)
            if phones:
                return phones[0]
        return "Not Found"
    
    def _extract_education(self, text: str) -> List[str]:
        """Extract education details using patterns"""
        education_keywords = ['b.tech', 'b.e', 'b.sc', 'm.tech', 'm.sc', 'phd', 'bachelor', 'master', 
                             'university', 'college', 'institute', 'school of']
        education = []
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in education_keywords):
                # Get the line and next few lines for context
                edu_text = line.strip()
                if len(edu_text) > 5:
                    education.append(edu_text)
        return education[:3] if education else ["Not Found"]
    
    def _extract_experience(self, text: str) -> List[str]:
        """Extract work experience"""
        experience_keywords = ['experience', 'worked as', 'intern', 'developer', 'engineer', 'analyst', 'consultant']
        experience = []
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in experience_keywords):
                # Look for years pattern
                if re.search(r'\b(20\d{2}|19\d{2})\b', line):
                    exp_text = line.strip()
                    if len(exp_text) > 10:
                        experience.append(exp_text)
        return experience[:3] if experience else ["No experience found"]
    
    def _extract_skills_advanced(self, text: str) -> Dict:
        """Advanced skill extraction with categorization"""
        text_lower = text.lower()
        skills_found = {
            "programming_languages": [],
            "frameworks": [],
            "databases": [],
            "cloud": [],
            "ml_ai": [],
            "soft_skills": []
        }
        
        for category, skill_list in self.skills_db.items():
            for skill in skill_list:
                if skill in text_lower:
                    skills_found[category].append(skill)
        
        return skills_found
    
    def _extract_projects(self, text: str) -> List[str]:
        """Extract project information"""
        project_keywords = ['project', 'built', 'developed', 'created', 'implemented']
        projects = []
        lines = text.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in project_keywords) and len(line.strip()) > 20:
                projects.append(line.strip())
        return projects[:3] if projects else ["No projects found"]
    
    def _extract_certifications(self, text: str) -> List[str]:
        """Extract certifications"""
        cert_keywords = ['certified', 'certification', 'certificate', 'credential']
        certifications = []
        lines = text.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in cert_keywords):
                cert_text = line.strip()
                if len(cert_text) > 5:
                    certifications.append(cert_text)
        return certifications[:3] if certifications else ["No certifications found"]
    
    def calculate_ats_score(self, resume_text: str, job_text: str) -> Dict:
        """Calculate ATS compatibility score"""
        # 1. Keyword overlap
        resume_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', resume_text.lower()))
        job_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', job_text.lower()))
        
        common_keywords = resume_words.intersection(job_words)
        keyword_score = len(common_keywords) / len(job_words) * 100 if job_words else 0
        
        # 2. Semantic similarity using embeddings
        resume_embedding = self.embedding_model.encode([resume_text])
        job_embedding = self.embedding_model.encode([job_text])
        semantic_score = cosine_similarity(resume_embedding, job_embedding)[0][0] * 100
        
        # 3. Skills match
        resume_skills = set(self._extract_skills_advanced(resume_text))
        job_skills = set(self._extract_skills_advanced(job_text))
        
        # Calculate weighted score
        final_score = (keyword_score * 0.3) + (semantic_score * 0.4) + (semantic_score * 0.3)
        
        return {
            "ats_score": min(100, final_score),
            "keyword_match_percentage": min(100, keyword_score),
            "semantic_match_percentage": min(100, semantic_score),
            "keyword_overlap": list(common_keywords)[:20],
            "skills": {
                "resume_skills": list(resume_skills),
                "job_skills": list(job_skills),
                "matching_skills": list(resume_skills.intersection(job_skills)),
                "missing_skills": list(job_skills - resume_skills)
            },
            "score_breakdown": {
                "keyword_weight": 30,
                "semantic_weight": 40,
                "skills_weight": 30
            }
        }
    
    def generate_resume_improvements(self, resume_text: str, job_text: str = None) -> Dict:
        """Generate AI-powered improvement suggestions"""
        improvements = {
            "formatting": [],
            "content": [],
            "keywords": [],
            "structure": []
        }
        
        # Analyze formatting
        if len(resume_text.split('\n')) < 20:
            improvements["formatting"].append("Add more sections to your resume (Education, Experience, Projects)")
        
        # Analyze content
        skills = self._extract_skills_advanced(resume_text)
        total_skills = sum(len(s) for s in skills.values())
        if total_skills < 10:
            improvements["content"].append("Add more relevant skills to your resume")
        
        # Analyze structure
        if "education" not in resume_text.lower():
            improvements["structure"].append("Add your education details")
        
        if "experience" not in resume_text.lower() and "intern" not in resume_text.lower():
            improvements["structure"].append("Add work experience or internship details")
        
        # AI-powered suggestions (if Gemini is available)
        if self.gemini_available and job_text:
            try:
                prompt = f"""
                Analyze this resume for a {job_text} position and provide:
                1. 3 specific improvements to make the resume more effective
                2. 3 keywords that should be added
                3. 2 things to remove or change
                
                Resume: {resume_text[:3000]}
                """
                response = self.gemini_client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=prompt
                )
                improvements["ai_suggestions"] = response.text.split('\n')
            except:
                improvements["ai_suggestions"] = ["AI suggestions not available"]
            
    def generate_interview_questions_advanced(self, role: str, difficulty: str = "medium", count: int = 5) -> List[Dict]:
        """Generate advanced interview questions using AI"""
        if self.gemini_available:
            try:
                prompt = f"""
                Generate {count} {difficulty} interview questions for a {role} position.
                For each question, provide:
                - The question
                - What to look for in the answer
                - Expected answer structure
                
                Format as JSON with fields: question, answer_hints, expected_points
                """
                response = self.gemini_model.generate_content(prompt)
                # Parse the response
                # For now, return structured questions
            except:
                pass
        
        # Fallback to predefined questions
        questions = {
            "technical": [
                {
                    "question": "Explain the difference between supervised and unsupervised learning.",
                    "answer_hints": "Focus on labeled vs unlabeled data, use cases",
                    "expected_points": ["Supervised uses labeled data", "Unsupervised finds patterns", "Examples"]
                },
                {
                    "question": "What is overfitting and how do you prevent it?",
                    "answer_hints": "Explain overfitting, regularization, cross-validation",
                    "expected_points": ["Model learns noise", "Use regularization", "Cross-validation"]
                },
                {
                    "question": "Explain the bias-variance tradeoff.",
                    "answer_hints": "Discuss underfitting vs overfitting, model complexity",
                    "expected_points": ["Bias = underfitting", "Variance = overfitting", "Find balance"]
                },
                {
                    "question": "What is the architecture of a transformer model?",
                    "answer_hints": "Explain encoder-decoder, attention mechanism",
                    "expected_points": ["Self-attention", "Multi-head attention", "Positional encoding"]
                }
            ]
        }
        
        return questions["technical"][:count]
    
    def generate_career_recommendations(self, resume_text: str) -> Dict:
        """Generate career path recommendations"""
        skills = self._extract_skills_advanced(resume_text)
        skill_set = set()
        for category_skills in skills.values():
            skill_set.update(category_skills)
        
        recommendations = {
            "role_suggestions": [],
            "skill_gaps": [],
            "learning_path": []
        }
        
        # Suggest roles based on skills
        if "python" in skill_set and "machine learning" in skill_set:
            recommendations["role_suggestions"].append("Machine Learning Engineer")
        if "python" in skill_set and "react" in skill_set:
            recommendations["role_suggestions"].append("Full Stack Developer")
        if "java" in skill_set:
            recommendations["role_suggestions"].append("Java Developer")
        if "aws" in skill_set and "docker" in skill_set:
            recommendations["role_suggestions"].append("DevOps Engineer")
        if "sql" in skill_set:
            recommendations["role_suggestions"].append("Data Analyst")
        
        # If no suggestions, add default
        if not recommendations["role_suggestions"]:
            recommendations["role_suggestions"].append("Consider exploring different technologies")
        
        return recommendations

    def full_analysis(self, resume_text: str, job_text: str = None) -> Dict:
        """Complete resume analysis with all features"""
        print("📊 Analyzing resume...")
        print("This may take a few seconds...")
        
        # Extract structured info
        print("1. Extracting structured information...")
        structured = self.extract_structured_info(resume_text)
        
        # Calculate ATS score (if job provided)
        print("2. Calculating ATS score...")
        if job_text:
            ats = self.calculate_ats_score(resume_text, job_text)
        else:
            ats = {"ats_score": 0, "message": "No job description provided"}
        
        # Generate improvements
        print("3. Generating improvement suggestions...")
        improvements = self.generate_resume_improvements(resume_text, job_text)
        
        # Generate career recommendations
        print("4. Generating career recommendations...")
        career = self.generate_career_recommendations(resume_text)
        
        return {
            "structured_info": structured,
            "ats_analysis": ats,
            "improvements": improvements,
            "career_recommendations": career
        }