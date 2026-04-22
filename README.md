#  NLP Legal Document Analyzer

## Description
This project analyzes legal documents using NLP techniques like:
- Clause Detection
- Named Entity Recognition (NER)
- Risk Analysis
- Summary Generation

## Tech Stack
- Python
- Streamlit
- NLP

## Project Structure
backend/
frontend/

##  How to Run
## ▶️ How to Run

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Run backend (Terminal 1)
cd backend
uvicorn app:app --reload

# Run frontend (Terminal 2)
cd frontend
streamlit run app.py
```

 Run backend and frontend in separate terminals.

