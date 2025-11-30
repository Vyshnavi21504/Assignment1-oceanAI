# Autonomous QA Agent

An intelligent QA agent that generates test cases and Selenium scripts from documentation.
The Autonomous QA Agent is an intelligent system that builds a "testing brain" from project documentation and automatically generates comprehensive test cases and executable Selenium scripts. It ensures all test generation is strictly grounded in provided documentation with no hallucinations.
> Transform project documentation into executable test cases and Selenium scripts automatically

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red)](https://streamlit.io)
## DEMO VIDEO
[https://drive.google.com/file/d/1uxkCLhSZHSzM_bEMg6G4-l2hzJSx3tHO/view?usp=sharing](https://drive.google.com/file/d/1Kf36k_QFIyuITg89bCFIUtx-NPpWrsEq/view?usp=sharing)

## Features
- **📚 Document-Grounded Testing** - All tests based strictly on provided documentation
- **🤖 AI-Powered Generation** - Intelligent test case creation using RAG pipeline
- **⚡ Automated Scripts** - Convert test cases to runnable Selenium code
- **🎯 No Hallucinations** - Strict adherence to source documentation
- **🔧 Modular Architecture** - Extensible and maintainable codebase

## Setup
1. Clone repo: `git clone https://github.com/yourusername/autonomous-qa-agent.git`
2. Create virtual environment: `python -m venv venv`
3. Install dependencies: `pip install -r requirements.txt`
4. Set OpenAI API key in `.env` file
5. Run backend: `python -m uvicorn app.main:app --reload`
6. Run frontend: `streamlit run frontend/app.py`

## 🏗️ Architecture


graph TB
    A[User Interface<br>Streamlit] --> B[Backend API<br>FastAPI]
    B --> C[AI Agents<br>TestCase & Script Generation]
    C --> D[Vector Database<br>ChromaDB]
    D --> E[Document Processing<br>LangChain]
    C --> F[LLM Integration<br>OpenAI/Local]
    F --> G[Test Output<br>Selenium Scripts]
    
    style A fill:#ff6b6b
    style B fill:#4ecdc4
    style C fill:#45b7d1
    style D fill:#96ceb4
    style F fill:#feca57

## Access
- Frontend: http://localhost:8501

- Backend API: http://localhost:8000



