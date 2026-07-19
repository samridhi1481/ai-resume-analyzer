"""
Agentic AI Orchestrator - Coordinates all ML, Data Science, and AI components
"""

import json
from typing import Dict, List, Optional
from google import genai
from .ml_resume_classifier import MLResumeClassifier
from .semantic_analyzer import SemanticResumeAnalyzer
from .data_science_analyzer import DataScienceAnalyzer
from .ai_analyzer_simple import SimpleAIResumeAnalyzer
from .matcher import ResumeMatcher
from .interview import InterviewGenerator

class AgenticOrchestrator:
    def __init__(self, api_key: str):
        """
        Initialize the Agentic Orchestrator with all components
        """
        self.client = genai.Client(api_key=api_key)
        
        # Initialize ML components
        self.ml_classifier = MLResumeClassifier()
        self.semantic_analyzer = SemanticResumeAnalyzer()
        self.ds_analyzer = DataScienceAnalyzer()
        
        # Initialize existing components
        self.analyzer = SimpleAIResumeAnalyzer()
        self.matcher = ResumeMatcher()
        self.interview = InterviewGenerator()
        
        # Train ML classifier on startup
        print("Training ML Resume Classifier...")
        self.ml_classifier.train()
        print("All components initialized successfully")
    
    def analyze(self, resume_text: str, job_text: Optional[str] = None) -> Dict:
        """
        Complete agentic analysis with all ML, Data Science, and AI components
        """
        print("Starting Agentic AI Analysis...")
        
        # Step 1: Extract structured information
        print("Step 1: Extracting structured information...")
        structured_info = self.analyzer.extract_structured_info(resume_text)
        
        # Step 2: ML Classification
        print("Step 2: ML Classification...")
        ml_result = self.ml_classifier.predict(resume_text)
        
        # Step 3: Semantic Analysis
        print("Step 3: Semantic Analysis...")
        if job_text:
            semantic_result = self.semantic_analyzer.calculate_semantic_match(
                resume_text, job_text
            )
        else:
            semantic_result = {"message": "No job description provided"}
        
        # Step 4: Data Science Insights
        print("Step 4: Data Science Insights...")
        ds_insights = self.ds_analyzer.generate_insights(structured_info)
        
        # Step 5: Job Matching
        print("Step 5: Job Matching...")
        if job_text:
            match_score = self.matcher.calculate_match_score(resume_text, job_text)
            job_skills = self.analyzer._extract_skills(job_text)
            skills_match = self.matcher.get_skills_match(
                structured_info.get('skills', []), 
                job_skills
            )
        else:
            match_score = None
            skills_match = None
        
        # Step 6: Interview Questions
        print("Step 6: Generating Interview Questions...")
        questions = self.interview.generate_questions(
            role=ml_result.get('predicted_category', 'Machine Learning Engineer'),
            question_type="technical",
            count=5
        )
        
        # Step 7: AI Generated Summary
        print("Step 7: Generating AI Summary...")
        ai_summary = self._generate_ai_summary(
            structured_info,
            ml_result,
            semantic_result,
            ds_insights,
            match_score,
            skills_match,
            questions,
            job_text
        )
        
        # Step 8: Career Recommendations
        print("Step 8: Generating Career Recommendations...")
        recommendations = self._generate_career_recommendations(
            structured_info,
            ml_result,
            ds_insights
        )
        
        return {
            "structured_info": structured_info,
            "ml_classification": ml_result,
            "semantic_analysis": semantic_result,
            "data_science_insights": ds_insights,
            "match_score": match_score,
            "skills_match": skills_match,
            "questions": questions,
            "ai_summary": ai_summary,
            "career_recommendations": recommendations,
            "status": "Agentic analysis complete"
        }
    
    def _generate_ai_summary(self, info: Dict, ml_result: Dict, 
                             semantic_result: Dict, ds_insights: Dict,
                             match_score: float, skills_match: Dict,
                             questions: List, job_text: str) -> str:
        """
        Generate AI-powered summary using Gemini
        """
        skills = info.get('skills', [])
        predicted_role = ml_result.get('predicted_category', 'Not classified')
        confidence = ml_result.get('confidence', 0)
        
        prompt = f"""
        You are a professional career advisor. Create a comprehensive summary for this candidate.
        
        Candidate Profile:
        - Name: {info.get('name', 'Not provided')}
        - Education: {info.get('education', [])}
        - Experience: {info.get('experience', [])}
        - Skills: {', '.join(skills[:15])}
        
        ML Classification:
        - Predicted Role: {predicted_role}
        - Confidence: {confidence:.1%}
        
        {'- Job Match Score: ' + str(match_score) + '%' if match_score else ''}
        
        Data Science Insights:
        - Total Skills: {ds_insights.get('skill_analysis', {}).get('total_skills', 0)}
        - Experience Level: {ds_insights.get('experience_analysis', {}).get('experience_level', 'Unknown')}
        - Skill Diversity: {ds_insights.get('skill_analysis', {}).get('skill_diversity', 0):.1f}%
        
        Job Description: {job_text if job_text else 'Not provided'}
        
        Provide a concise summary that includes:
        1. Overall assessment
        2. Key strengths
        3. Areas for improvement
        4. Recommendations for the candidate
        
        Keep it professional and concise.
        """
        
        response = self.client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return response.text
    
    def _generate_career_recommendations(self, info: Dict, ml_result: Dict,
                                         ds_insights: Dict) -> Dict:
        """
        Generate career recommendations using AI
        """
        skills = info.get('skills', [])
        predicted_role = ml_result.get('predicted_category', 'Not classified')
        
        prompt = f"""
        Based on this candidate's profile, provide career recommendations.
        
        Skills: {', '.join(skills[:10])}
        Predicted Role: {predicted_role}
        Education: {info.get('education', [])}
        Experience: {info.get('experience', [])}
        
        Provide JSON with:
        1. role_suggestions: array of recommended job titles
        2. skill_development: skills to learn or improve
        3. next_steps: actionable recommendations
        """
        
        response = self.client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        
        try:
            return json.loads(response.text)
        except:
            return {
                "role_suggestions": ["Machine Learning Engineer", "Data Scientist"],
                "skill_development": ["Deep Learning", "Cloud Computing"],
                "next_steps": ["Build portfolio projects", "Get relevant certifications"]
            }