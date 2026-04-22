IMPORTANT = [
    "Confidentiality Clause",
    "Termination Clause",
    "Payment Terms"
]
def analyze_risk(detected):
    risks = []

    for clause in IMPORTANT:
        if clause not in detected:
            risks.append(f"Missing {clause} → High Risk")

    score = 10 - len(risks)*2

    return {
        "score": max(score, 1),
        "issues": risks
    }