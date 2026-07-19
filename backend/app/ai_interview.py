from google import genai

class AIInterviewGenerator:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
    
    def generate_questions(self, role, skills, experience):
        prompt = f"""
        Generate 5 technical interview questions for a {role} position.
        The candidate has skills: {skills}
        Experience: {experience} years
        
        Return ONLY the questions, numbered.
        """
        response = self.client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return response.text