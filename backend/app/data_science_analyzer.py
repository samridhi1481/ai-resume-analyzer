"""
Data Science Analytics for Resume Analysis
"""

import pandas as pd
import numpy as np
from collections import Counter
from typing import Dict, List, Optional
import re

class DataScienceAnalyzer:
    def __init__(self):
        pass
    
    def analyze_skill_trends(self, skills: List[str]) -> Dict:
        """
        Analyze skill patterns and trends
        """
        # Categorize skills
        categories = {
            "programming": ['python', 'java', 'javascript', 'c++', 'go', 'rust', 'typescript'],
            "web_frameworks": ['react', 'angular', 'django', 'flask', 'node.js', 'fastapi'],
            "databases": ['sql', 'postgresql', 'mysql', 'mongodb', 'redis'],
            "cloud_devops": ['aws', 'docker', 'kubernetes', 'jenkins', 'azure', 'gcp'],
            "ml_ai": ['machine learning', 'deep learning', 'nlp', 'tensorflow', 'pytorch', 'scikit-learn'],
            "data_science": ['pandas', 'numpy', 'data science', 'analytics', 'visualization'],
            "soft_skills": ['leadership', 'communication', 'problem solving', 'teamwork']
        }
        
        skill_counts = Counter(skills)
        categorized_skills = {cat: [] for cat in categories}
        
        for skill in skills:
            for category, cat_skills in categories.items():
                if skill.lower() in cat_skills:
                    categorized_skills[category].append(skill)
        
        return {
            "total_skills": len(skills),
            "unique_skills": len(set(skills)),
            "top_skills": skill_counts.most_common(10),
            "categorized_skills": {k: len(v) for k, v in categorized_skills.items()},
            "skill_diversity": len(categorized_skills) / len(categories) * 100
        }
    
    def analyze_experience_patterns(self, experience_text: str) -> Dict:
        """
        Analyze experience patterns from text
        """
        # Extract years of experience
        year_patterns = [
            r'(\d+)\s*years?',
            r'(\d+)\s*yrs?',
            r'(\d+)\s*\+\s*years?'
        ]
        
        years = []
        for pattern in year_patterns:
            matches = re.findall(pattern, experience_text)
            years.extend([int(m) for m in matches])
        
        total_years = sum(years) if years else 0
        
        # Extract roles
        roles = []
        role_keywords = ['engineer', 'developer', 'analyst', 'scientist', 'intern', 'consultant']
        for keyword in role_keywords:
            if keyword in experience_text.lower():
                roles.append(keyword)
        
        return {
            "total_years_experience": total_years,
            "roles_identified": list(set(roles)),
            "experience_level": self._get_experience_level(total_years)
        }
    
    def _get_experience_level(self, years: int) -> str:
        """
        Determine experience level based on years
        """
        if years <= 0:
            return "Entry Level"
        elif years <= 2:
            return "Junior"
        elif years <= 5:
            return "Mid-Level"
        elif years <= 8:
            return "Senior"
        else:
            return "Lead/Principal"
    
    def generate_insights(self, resume_data: Dict) -> Dict:
        """
        Generate data-driven insights from resume
        """
        skills = resume_data.get('skills', [])
        experience_text = ' '.join(resume_data.get('experience', []))
        
        skill_analysis = self.analyze_skill_trends(skills)
        experience_analysis = self.analyze_experience_patterns(experience_text)
        
        # Generate recommendations based on data
        recommendations = []
        
        if skill_analysis['unique_skills'] < 10:
            recommendations.append("Add more diverse skills to your resume")
        
        if skill_analysis['skill_diversity'] < 50:
            recommendations.append("Build skills across multiple categories")
        
        if experience_analysis['total_years_experience'] < 2:
            recommendations.append("Consider internships or projects to gain more experience")
        
        if 'soft_skills' not in str(skill_analysis['categorized_skills']):
            recommendations.append("Add soft skills like leadership and communication")
        
        return {
            "skill_analysis": skill_analysis,
            "experience_analysis": experience_analysis,
            "insights": {
                "recommendations": recommendations,
                "strengths": self._identify_strengths(skill_analysis),
                "growth_areas": self._identify_growth_areas(skill_analysis)
            }
        }
    
    def _identify_strengths(self, skill_analysis: Dict) -> List[str]:
        """
        Identify strength areas from skill analysis
        """
        strengths = []
        categorized = skill_analysis.get('categorized_skills', {})
        
        for category, count in categorized.items():
            if count >= 2:
                category_name = category.replace('_', ' ').title()
                strengths.append(f"{category_name}: {count} skills")
        
        return strengths[:3] if strengths else ["No clear strengths identified"]
    
    def _identify_growth_areas(self, skill_analysis: Dict) -> List[str]:
        """
        Identify growth areas from skill analysis
        """
        growth_areas = []
        categorized = skill_analysis.get('categorized_skills', {})
        
        for category, count in categorized.items():
            if count == 0:
                category_name = category.replace('_', ' ').title()
                growth_areas.append(f"Consider learning {category_name} skills")
        
        return growth_areas[:3] if growth_areas else ["No specific growth areas identified"]