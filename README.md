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

## Architecture
User Interface
│
▼
FastAPI Backend
│
├── Agentic AI System
│ ├── Planner Agent
│ ├── Researcher Agent
│ ├── Analyzer Agent
│ ├── Question Generator
│ ├── Summary Agent
│ └── Career Advisor
│
├── ML Components
│ ├── ML Classifier (Role Prediction)
│ ├── Semantic Analyzer (Job Matching)
│ └── Data Science Analyzer
│
└── PDF Parser (Text Extraction)
│
▼
Google Gemini API
├── Question Generation
├── Summary Generation
└── Career Advice


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

3. Configure Gemini API Key
Go to: https://aistudio.google.com/app/apikey

Create a free API key

Add it to backend/app/gemini_config.py

Frontend Setup
cd frontend
npm install

Running the Application
Start Backend
cd backend
python -m app.main

Start Frontend (New Terminal)
bash
cd frontend
npm start

Open Browser
Backend: http://localhost:8000

Frontend: http://localhost:3000