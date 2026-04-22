SUGGESTIONS = {
    "Termination Clause": "Either party may terminate this agreement with 30 days notice.",
    "Confidentiality Clause": "Both parties agree not to disclose confidential information.",
    "Payment Terms": "Payment must be made within 30 days of invoice."
}

def suggest_clauses(detected):
    missing = []

    for clause, text in SUGGESTIONS.items():
        if clause not in detected:
            missing.append({
                "clause": clause,
                "suggestion": text
            })

    return missing