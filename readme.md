#  NLP Legal Document Analyzer

## Description
This project analyzes legal documents using NLP techniques like:
- Clause Detection
- Named Entity Recognition (NER)
- Risk Analysis
- Summary Generation

## 🛠 Tech Stack
- Python
- Streamlit
- NLP

## 📂 Project Structure
backend/
frontend/

## ▶️ How to Run
```bash
pip install -r requirements.txt

python -m spacy download en_core_web_sm
```run backend first
cd backend
uvicorn app:app --reload

```run frontend 
cd frontend
streamlit run frontend/app.py