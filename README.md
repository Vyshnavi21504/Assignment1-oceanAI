# Autonomous QA Agent

An intelligent QA agent that generates test cases and Selenium scripts from documentation.
## DEMO VIDEO
[https://drive.google.com/file/d/1uxkCLhSZHSzM_bEMg6G4-l2hzJSx3tHO/view?usp=sharing](https://drive.google.com/file/d/1Kf36k_QFIyuITg89bCFIUtx-NPpWrsEq/view?usp=sharing)

## Features
- Document ingestion (PDF, MD, TXT, JSON)
- Test case generation using RAG
- Selenium script generation
- Streamlit web interface

## Setup
1. Clone repo: `git clone https://github.com/yourusername/autonomous-qa-agent.git`
2. Create virtual environment: `python -m venv venv`
3. Install dependencies: `pip install -r requirements.txt`
4. Set OpenAI API key in `.env` file
5. Run backend: `python -m uvicorn app.main:app --reload`
6. Run frontend: `streamlit run frontend/app.py`

## Access
- Frontend: http://localhost:8501

- Backend API: http://localhost:8000


