import re
from typing import List, Dict

class InterviewGenerator:
    def __init__(self):
        pass
    
    def generate_questions(self, role: str, question_type: str, count: int = 5, resume_text: str = None) -> List[Dict]:
        """
        Generate interview questions - personalized from resume
        """
        if resume_text:
            return self._generate_personalized_questions(resume_text, role, count)
        
        # Fallback if no resume provided
        return self._get_fallback_questions(count)
    
    def _generate_personalized_questions(self, resume_text: str, role: str, count: int = 5) -> List[Dict]:
        """
        Generate questions based on specific resume content
        """
        # Extract all information from resume
        projects = self._extract_projects(resume_text)
        skills = self._extract_skills_from_text(resume_text)
        experience = self._extract_experience(resume_text)
        education = self._extract_education(resume_text)
        achievements = self._extract_achievements(resume_text)
        
        questions = []
        
        # Question 1: Based on projects (most important)
        if projects:
            project = projects[0]
            questions.append({
                "id": 1,
                "question": f"You mentioned your project '{project}'. Can you walk me through your approach, the technical challenges you faced, and how you solved them?",
                "type": "project"
            })
        else:
            questions.append({
                "id": 1,
                "question": "Tell me about a challenging technical project you worked on recently.",
                "type": "general"
            })
        
        # Question 2: Technical skill deep-dive (based on skills)
        if len(skills) > 0:
            skill = skills[0]
            questions.append({
                "id": 2,
                "question": f"You have experience with {skill}. Can you explain a complex problem you solved using {skill} and the approach you took?",
                "type": "technical"
            })
        else:
            questions.append({
                "id": 2,
                "question": "What is your strongest technical skill and how have you applied it in real projects?",
                "type": "technical"
            })
        
        # Question 3: Second project or skill
        if len(projects) > 1:
            project2 = projects[1]
            questions.append({
                "id": 3,
                "question": f"Regarding your project '{project2}', what was your specific contribution and what was the most difficult part?",
                "type": "project"
            })
        elif len(skills) > 1:
            skill2 = skills[1]
            questions.append({
                "id": 3,
                "question": f"How would you handle a scenario where your {skill2} code failed in production? What steps would you take?",
                "type": "technical"
            })
        else:
            questions.append({
                "id": 3,
                "question": "How do you approach debugging complex issues in your code?",
                "type": "technical"
            })
        
        # Question 4: Based on experience or achievements
        if experience:
            exp = experience[0]
            questions.append({
                "id": 4,
                "question": f"Based on your experience as '{exp}', what was your biggest learning and how did it prepare you for this role?",
                "type": "behavioral"
            })
        elif achievements:
            ach = achievements[0]
            questions.append({
                "id": 4,
                "question": f"You mentioned '{ach}'. Can you tell me more about this achievement and what you learned from it?",
                "type": "behavioral"
            })
        else:
            questions.append({
                "id": 4,
                "question": "How do you handle tight deadlines and pressure in a professional setting?",
                "type": "behavioral"
            })
        
        # Question 5: Career goals with role context
        questions.append({
            "id": 5,
            "question": f"What interests you most about the {role} role, and how does your background in {', '.join(skills[:2]) if skills else 'technology'} prepare you for it?",
            "type": "career"
        })
        
        return questions[:count]
    
    def _get_fallback_questions(self, count: int = 5) -> List[Dict]:
        """Fallback questions if no resume provided"""
        fallback = [
            "Tell me about yourself and your background.",
            "What is your experience with machine learning and data science?",
            "Describe a project you're proud of.",
            "What are your career goals and aspirations?",
            "Why do you want to work in this field?"
        ]
        return [{"id": i+1, "question": q, "type": "general"} for i, q in enumerate(fallback[:count])]
    
    def _extract_projects(self, text: str) -> List[str]:
        """Extract project names from resume"""
        projects = []
        lines = text.split('\n')
        
        # Look for patterns like "Project Name" or bullet points with project info
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # Check if line starts with project indicators
            if line_stripped.startswith('•') or line_stripped.startswith('-'):
                if any(keyword in line_stripped.lower() for keyword in ['project', 'built', 'developed', 'created']):
                    clean = re.sub(r'^[•\-]\s*', '', line_stripped)
                    if len(clean) > 5:
                        projects.append(clean)
            
            # Check for project name followed by technologies
            elif any(keyword in line.lower() for keyword in ['project', 'built', 'developed', 'created']):
                if len(line_stripped) > 10:
                    projects.append(line_stripped)
                
                # Also check next line for project name
                elif i + 1 < len(lines) and len(lines[i+1].strip()) > 10:
                    projects.append(lines[i+1].strip())
        
        # Also look for section headers like "Projects:" or "PROJECTS"
        in_projects_section = False
        for line in lines:
            line_lower = line.lower()
            if 'projects:' in line_lower or '## projects' in line_lower:
                in_projects_section = True
                continue
            if in_projects_section:
                if line.strip() and not any(x in line_lower for x in ['skills:', 'experience:', 'education:', 'contact']):
                    if len(line.strip()) > 5 and not line.strip().startswith('#'):
                        projects.append(line.strip())
                if 'experience:' in line_lower or 'skills:' in line_lower:
                    in_projects_section = False
        
        # Remove duplicates and limit
        seen = set()
        unique_projects = []
        for p in projects:
            # Clean up project names
            p_clean = re.sub(r'\s*\([^)]*\)\s*', '', p)  # Remove parentheses content
            p_clean = re.sub(r'\s*\[[^\]]*\]\s*', '', p_clean)  # Remove bracket content
            p_clean = re.sub(r'\b(Link|github|repo|source|code|demo)\b', '', p_clean, flags=re.IGNORECASE)
            p_clean = p_clean.strip()
            
            if p_clean and len(p_clean) > 3 and p_clean not in seen:
                seen.add(p_clean)
                unique_projects.append(p_clean[:80])
        
        return unique_projects[:4]
    
    def _extract_skills_from_text(self, text: str) -> List[str]:
        """Extract skills from resume text"""
        skill_list = [
            'python', 'java', 'javascript', 'typescript', 'c++', 'c', 'go', 'rust',
            'react', 'angular', 'vue', 'node.js', 'fastapi', 'django', 'flask',
            'sql', 'postgresql', 'mysql', 'mongodb', 'redis',
            'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'jenkins', 'git',
            'machine learning', 'deep learning', 'nlp', 'computer vision',
            'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
            'matplotlib', 'seaborn', 'plotly', 'jupyter',
            'reinforcement learning', 'transfer learning', 'llm', 'rag',
            'whisper', 'coqui', 'ppo', 'fastapi',
            'leadership', 'communication', 'problem solving', 'teamwork',
            'linux', 'windows', 'unix', 'bash', 'shell',
            'html', 'css', 'figma', 'github', 'vscode'
        ]
        
        found_skills = []
        text_lower = text.lower()
        for skill in skill_list:
            if skill in text_lower:
                # Only add if it's a whole word match
                found_skills.append(skill)
        
        # Remove duplicates and limit
        return list(set(found_skills))[:8]
    
    def _extract_experience(self, text: str) -> List[str]:
        """Extract experience mentions"""
        experience = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            if any(kw in line_lower for kw in ['intern', 'experience', 'worked at', 'developer', 'engineer']):
                clean_line = line.strip()
                if len(clean_line) > 5:
                    # Clean up the line
                    clean_line = re.sub(r'\s*\([^)]*\)\s*', '', clean_line)
                    clean_line = re.sub(r'\s*•\s*', '', clean_line)
                    if clean_line and clean_line not in experience:
                        experience.append(clean_line[:100])
        
        return experience[:3]
    
    def _extract_education(self, text: str) -> List[str]:
        """Extract education mentions"""
        education = []
        lines = text.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(kw in line_lower for kw in ['b.tech', 'b.e', 'm.tech', 'bachelor', 'master', 'university']):
                clean_line = line.strip()
                if len(clean_line) > 5:
                    education.append(clean_line)
        return education[:3]
    
    def _extract_achievements(self, text: str) -> List[str]:
        """Extract achievements and leadership mentions"""
        achievements = []
        lines = text.split('\n')
        
        for line in lines:
            line_lower = line.lower()
            if any(kw in line_lower for kw in ['achievement', 'leadership', 'campus ambassador', 'hackathon', 'selected', 'top']):
                clean_line = line.strip()
                if len(clean_line) > 5:
                    # Clean up
                    clean_line = re.sub(r'^[•\-]\s*', '', clean_line)
                    if clean_line:
                        achievements.append(clean_line[:100])
        
        return achievements[:3]