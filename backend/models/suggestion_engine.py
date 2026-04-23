SUGGESTIONS = {
    "Termination Clause": "Add clear termination conditions and notice period.",
    "Confidentiality Clause": "Define duration and scope of confidentiality obligations.",
    "Payment Terms": "Include penalties for late payments and payment methods.",
    "Liability Clause": "Limit liability to a specific amount to reduce risk.",
    "Governing Law": "Clearly specify jurisdiction to avoid legal ambiguity."
}

def suggest_clauses(detected):
    suggestions = []

    for clause in detected:
        if clause in SUGGESTIONS:
            suggestions.append({
                "clause": clause,
                "suggestion": SUGGESTIONS[clause]
            })

    # Optional: also suggest missing important clauses
    for clause in SUGGESTIONS:
        if clause not in detected:
            suggestions.append({
                "clause": clause,
                "suggestion": f"Consider adding a {clause.lower()} to strengthen the agreement."
            })

    return suggestions