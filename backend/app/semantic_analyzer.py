"""
Semantic Resume Analyzer using Sentence Transformers
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List, Optional
import re

class SemanticResumeAnalyzer:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def calculate_semantic_match(self, resume_text: str, job_text: str) -> Dict:
        """
        Calculate semantic similarity between resume and job description
        """
        # Generate embeddings
        resume_embedding = self.model.encode([resume_text])
        job_embedding = self.model.encode([job_text])
        
        # Calculate similarity
        similarity = cosine_similarity(resume_embedding, job_embedding)[0][0]
        
        # Section-wise analysis (simplified)
        sections = self._extract_sections(resume_text)
        section_scores = {}
        
        for section_name, section_text in sections.items():
            if section_text.strip():
                section_emb = self.model.encode([section_text])
                section_score = cosine_similarity(section_emb, job_embedding)[0][0]
                section_scores[section_name] = float(section_score)
        
        # Calculate weighted score
        weights = {
            "skills": 0.4,
            "experience": 0.3,
            "education": 0.2,
            "projects": 0.1
        }
        
        weighted_score = 0
        for section, weight in weights.items():
            if section in section_scores:
                weighted_score += section_scores[section] * weight
        
        return {
            "overall_similarity": float(similarity * 100),
            "weighted_score": float(weighted_score * 100),
            "section_scores": {k: float(v * 100) for k, v in section_scores.items()},
            "strength_areas": self._identify_strengths(section_scores),
            "weakness_areas": self._identify_weaknesses(section_scores)
        }
    
    def _extract_sections(self, text: str) -> Dict:
        """
        Extract different sections from resume text
        """
        sections = {
            "skills": "",
            "experience": "",
            "education": "",
            "projects": ""
        }
        
        lines = text.split('\n')
        current_section = "skills"  # default
        
        for line in lines:
            line_lower = line.lower()
            if 'education' in line_lower or 'university' in line_lower:
                current_section = "education"
            elif 'experience' in line_lower or 'intern' in line_lower or 'worked' in line_lower:
                current_section = "experience"
            elif 'project' in line_lower or 'developed' in line_lower or 'built' in line_lower:
                current_section = "projects"
            elif 'skill' in line_lower or 'technologies' in line_lower:
                current_section = "skills"
            
            if line.strip() and not line.strip().startswith('---'):
                sections[current_section] += line + " "
        
        return sections
    
    def _identify_strengths(self, section_scores: Dict) -> List[str]:
        """
        Identify strongest sections
        """
        if not section_scores:
            return []
        
        threshold = 50  # 50% threshold
        strengths = []
        for section, score in section_scores.items():
            if score * 100 > threshold:
                strengths.append(f"{section.capitalize()} ({score * 100:.1f}%)")
        
        return strengths[:3] if strengths else ["No clear strengths identified"]
    
    def _identify_weaknesses(self, section_scores: Dict) -> List[str]:
        """
        Identify weakest sections
        """
        if not section_scores:
            return []
        
        threshold = 30  # 30% threshold
        weaknesses = []
        for section, score in section_scores.items():
            if score * 100 < threshold:
                weaknesses.append(f"{section.capitalize()} ({score * 100:.1f}%)")
        
        return weaknesses[:3] if weaknesses else ["No clear weaknesses identified"]