# AI Resume Analyzer

An AI-powered resume analysis system that extracts skills, matches with job descriptions, generates interview questions, and provides career recommendations.

## Features

- **PDF Resume Upload** - Upload and parse PDF resumes
- **Skill Extraction** - Automatically extract skills from resumes
- **ML Classification** - Predict job roles using machine learning
- **Job Description Matching** - Calculate match score with job descriptions
- **Agentic AI** - Multi-agent system for comprehensive analysis
- **Personalized Interview Questions** - Generate questions based on resume
- **Career Recommendations** - Get role and skill development suggestions

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | FastAPI |
| Frontend | React |
| ML Classification | Scikit-learn (Random Forest) |
| Semantic Analysis | Sentence Transformers |
| Agentic AI | Google Gemini API |
| PDF Parsing | PyMuPDF |
| Data Science | Pandas, NumPy |

## System Architecture

### Frontend Layer
- **React Application** with three tabs:
  - Upload PDF
  - AI Analysis
  - Interview Prep

### Backend Layer
- **FastAPI Server** handling all API requests

### Agentic AI Layer
- **Planner Agent** - Creates analysis plan
- **Researcher Agent** - Extracts resume information
- **Analyzer Agent** - Analyzes skills and patterns
- **Question Generator** - Creates personalized questions
- **Summary Agent** - Generates professional summary
- **Career Advisor** - Suggests roles and skills

### ML Components
- **ML Classifier** - Predicts job role from resume
- **Semantic Analyzer** - Matches resume with job description
- **Data Science Analyzer** - Analyzes skill patterns
- **PDF Parser** - Extracts text from PDF

### AI Services
- **Google Gemini API** for:
  - Question Generation
  - Summary Generation
  - Career Recommendations

### Data Flow
1. User uploads PDF or pastes text
2. Backend extracts text from PDF
3. Agentic AI system starts analysis
4. ML Classifier predicts role
5. Semantic Analyzer matches with job
6. Questions and summary are generated
7. Results displayed to user


## Installation

### Prerequisites

- Python 3.8+
- Node.js 16+
- Google Gemini API Key

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

### Configure Gemini API Key

Go to: https://aistudio.google.com/app/apikey

Create a free API key

Add it to backend/app/gemini_config.py


### Frontend Setup
cd frontend
npm install

### Running the Application
Start Backend
cd backend
python -m app.main

### Start Frontend (New Terminal)
cd frontend
npm start

### Open Browser
Backend: http://localhost:8000

Frontend: http://localhost:3000