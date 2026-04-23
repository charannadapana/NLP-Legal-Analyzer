IMPORTANT = {
    "Confidentiality Clause": 30,
    "Termination Clause": 25,
    "Payment Terms": 20,
    "Liability Clause": 25,
    "Governing Law": 15
}

def analyze_risk(detected):
    issues = []
    score = 100  

    for clause, weight in IMPORTANT.items():
        if clause not in detected:
            score -= weight
            issues.append(f"Missing {clause} → High Risk (-{weight})")

    score = max(min(score, 100), 5)

    return {
        "score": score,
        "issues": issues
    }