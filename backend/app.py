from fastapi import FastAPI, UploadFile, File
from models.clause_detector import detect_clauses
from models.risk_engine import analyze_risk
from models.suggestion_engine import suggest_clauses
from utils.parser import extract_text
from utils.ner import extract_entities
from utils.summarizer import generate_summary

app = FastAPI()

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    text = extract_text(file)

    clauses = detect_clauses(text)
    entities = extract_entities(text)
    risk = analyze_risk(clauses)
    suggestions = suggest_clauses(clauses)
    summary = generate_summary(text)

    return {
        "clauses": clauses,
        "entities": entities,
        "risk": risk,
        "suggestions": suggestions,
        "summary": summary
    }