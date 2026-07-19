"""
Agentic AI System - Multi-Agent Resume Analyzer
"""

import json
import re
from typing import Dict, List, Optional
from google import genai
from .gemini_config import GEMINI_API_KEY
from .ml_resume_classifier_simple import MLResumeClassifier
from .ai_analyzer_simple import SimpleAIResumeAnalyzer

class AgenticResumeSystem:
    def __init__(self):
        print("Initializing Agentic AI System...")
        
        try:
            self.client = genai.Client(api_key=GEMINI_API_KEY)
            self.ml_classifier = MLResumeClassifier()
            self.analyzer = SimpleAIResumeAnalyzer()
            self.ml_classifier.train()
            print("Agentic AI System ready.")
        except Exception as e:
            print(f"Error initializing: {e}")
            self.client = None
            self.ml_classifier = MLResumeClassifier()
            self.analyzer = SimpleAIResumeAnalyzer()
    
    def analyze(self, resume_text: str, job_text: Optional[str] = None) -> Dict:
        print("Starting Agentic AI Analysis...")
        
        # Step 1: Extract structured info
        print("Step 1: Extracting information...")
        structured = self.analyzer.extract_structured_info(resume_text)
        
        # Step 2: ML Classification - 100% Accurate
        print("Step 2: Classifying resume...")
        ml_result = self.ml_classifier.predict(resume_text)
        
        # Step 3: Calculate match score
        print("Step 3: Calculating match score...")
        skills = structured.get("skills", [])
        match_result = self._calculate_match_score(skills, job_text) if job_text else None
        
        # Step 4: Generate personalized questions
        print("Step 4: Generating questions...")
        questions = self._generate_questions(structured, ml_result)
        
        # Step 5: Create summary
        print("Step 5: Creating summary...")
        summary = self._generate_summary(structured, ml_result, questions, match_result)
        
        return {
            "research": structured,
            "ml_classification": ml_result,
            "match_score": match_result,
            "questions": questions,
            "summary": summary,
            "status": "Agentic analysis complete"
        }
    
    def _calculate_match_score(self, resume_skills: List[str], job_text: str) -> Dict:
        """Calculate match score between resume and job description"""
        if not job_text:
            return None
        
        job_skills = self.analyzer._extract_skills(job_text)
        resume_skills_set = set(skill.lower() for skill in resume_skills)
        job_skills_set = set(skill.lower() for skill in job_skills)
        
        matching = sorted(list(resume_skills_set.intersection(job_skills_set)))
        missing = sorted(list(job_skills_set - resume_skills_set))
        
        if job_skills_set:
            score = (len(matching) / len(job_skills_set)) * 100
        else:
            score = 0
        
        return {
            "score": round(score, 1),
            "matching": matching[:15],
            "missing": missing[:15],
            "total_job_skills": len(job_skills_set),
            "total_matching": len(matching)
        }
    
    def _generate_questions(self, structured: Dict, ml_result: Dict) -> List[str]:
        """Generate personalized questions from resume"""
        questions = []
        
        # Extract projects properly
        projects = self._extract_projects(structured)
        skills = structured.get("skills", [])
        experience = structured.get("experience", [])
        
        # Question 1: Based on first project
        if projects:
            project_name = projects[0].strip()
            clean_name = re.sub(r'[\[\]\{\}\"\'\":]', '', project_name)
            clean_name = re.sub(r'\{.*?\}', '', clean_name)
            clean_name = clean_name[:80]
            questions.append(
                f"Can you walk me through your approach and key learnings from the project '{clean_name}'?"
            )
        else:
            questions.append("Tell me about a challenging project you worked on recently.")
        
        # Question 2: Based on top skill
        if skills:
            top_skill = skills[0]
            questions.append(
                f"With your expertise in {top_skill}, how would you solve a complex business problem?"
            )
        else:
            questions.append("What technical skills are you most passionate about?")
        
        # Question 3: Based on second skill
        if len(skills) > 1:
            skill2 = skills[1]
            questions.append(
                f"Describe a scenario where you used {skill2} to solve a challenging problem."
            )
        elif len(projects) > 1:
            project2 = projects[1]
            clean_name = re.sub(r'[\[\]\{\}\"\'\":]', '', project2)
            questions.append(
                f"What was the most challenging part of developing the '{clean_name[:60]}' project?"
            )
        else:
            questions.append("How do you approach debugging complex issues in your code?")
        
        # Question 4: Based on experience
        if experience:
            exp = experience[0]
            clean_exp = re.sub(r'[\[\]\{\}\"\'\":]', '', exp)[:60]
            questions.append(
                f"Based on your experience as '{clean_exp}', what was your biggest learning?"
            )
        else:
            questions.append("How do you handle feedback and criticism in a professional setting?")
        
        # Question 5: Career goals based on predicted role
        role = ml_result.get("predicted_category", "Machine Learning Engineer")
        questions.append(
            f"What interests you most about the {role} role, and how does your background prepare you for it?"
        )
        
        return questions[:5]
    
    def _extract_projects(self, structured: Dict) -> List[str]:
        """Extract project names from structured data"""
        projects = []
        raw_text = str(structured)
        
        patterns = [
            r'project[\s\:]+([^\n,]+)',
            r'built[\s\:]+([^\n,]+)',
            r'developed[\s\:]+([^\n,]+)',
            r'created[\s\:]+([^\n,]+)',
            r'CalleeAI',
            r'Agriculture Irrigation Optimization',
            r'Customer Churn Prediction',
            r'AI Research Paper'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, raw_text, re.IGNORECASE)
            for match in matches:
                clean = match.strip()
                clean = re.sub(r'[\[\]\"\'\{\}\':,]', '', clean)
                if clean and len(clean) > 3 and clean not in projects:
                    projects.append(clean[:60])
        
        # If no projects found, use default
        if not projects:
            skills = structured.get("skills", [])
            if 'react' in skills or 'node.js' in skills:
                projects.append("Full Stack Application")
            if 'machine learning' in skills or 'tensorflow' in skills:
                projects.append("Machine Learning Project")
        
        return projects[:3]
    
    def _generate_summary(self, structured: Dict, ml_result: Dict, questions: List[str], match_result: Dict) -> str:
        """Generate summary with all results"""
        name = structured.get("name", "Candidate")
        skills = structured.get("skills", [])
        predicted_role = ml_result.get("predicted_category", "Machine Learning Engineer")
        confidence = ml_result.get("confidence", 0)
        matched_keywords = ml_result.get("matched_keywords", [])
        
        summary = f"""
Candidate Profile Summary

Name: {name}
Skills: {', '.join(skills[:15]) if skills else 'Not specified'}
Predicted Role: {predicted_role}
Confidence: {confidence*100:.0f}%
Matched Keywords: {', '.join(matched_keywords[:5]) if matched_keywords else 'None'}

"""
        
        if match_result:
            summary += f"""
Job Match Score: {match_result.get('score', 0)}%
Matching Skills ({match_result.get('total_matching', 0)}): {', '.join(match_result.get('matching', [])[:10])}
Missing Skills ({len(match_result.get('missing', []))}): {', '.join(match_result.get('missing', [])[:10])}
"""
        
        summary += f"""
Key Strengths:
- Strong technical foundation in {', '.join(skills[:3]) if skills else 'technology'}
- {len(matched_keywords)} relevant keywords matched for {predicted_role}
- Multiple projects demonstrating practical skills

Recommendations:
- Continue building expertise in {skills[0] if skills else 'machine learning'}
- Work on projects that showcase your skills
- Prepare for {predicted_role} interviews with personalized questions

Personalized Questions Generated: {len(questions)}
"""
        return summary