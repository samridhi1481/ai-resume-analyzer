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
┌─────────────────────────────────────────────────────────────┐
│                      USER INTERFACE                         │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ Upload PDF  │  │ AI Analysis │  │  Interview Prep     │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND                          │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │              AGENTIC AI SYSTEM (Multi-Agent)           ││
│  │                                                         ││
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐          ││
│  │  │ Planner   │  │Researcher │  │ Analyzer  │          ││
│  │  │  Agent    │→│  Agent    │→│  Agent    │          ││
│  │  └───────────┘  └───────────┘  └───────────┘          ││
│  │                                                         ││
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐          ││
│  │  │ Question  │  │ Summary   │  │ Career    │          ││
│  │  │ Generator │←│  Agent    │←│ Advisor   │          ││
│  │  └───────────┘  └───────────┘  └───────────┘          ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │              ML COMPONENTS                             ││
│  │                                                         ││
│  │  ┌───────────────────┐  ┌──────────────────────────┐  ││
│  │  │  ML Classifier    │  │  Semantic Analyzer       │  ││
│  │  │  Role Prediction  │  │  Job Matching            │  ││
│  │  └───────────────────┘  └──────────────────────────┘  ││
│  │                                                         ││
│  │  ┌───────────────────┐  ┌──────────────────────────┐  ││
│  │  │  Data Science     │  │  PDF Parser              │  ││
│  │  │  Analyzer         │  │  Text Extraction         │  ││
│  │  └───────────────────┘  └──────────────────────────┘  ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  GOOGLE GEMINI API                          │
│                                                             │
│  ┌───────────────┐  ┌───────────────┐  ┌─────────────────┐ │
│  │  Question     │  │   Summary     │  │  Career Advice  │ │
│  │  Generation   │  │  Generation   │  │                 │ │
│  └───────────────┘  └───────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────┘


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