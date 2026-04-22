from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

CLAUSE_TYPES = {
    "Confidentiality Clause": ["confidential", "non-disclosure", "nda"],
    "Termination Clause": ["terminate", "termination"],
    "Payment Terms": ["payment", "fees", "invoice"],
    "Liability Clause": ["liability", "damages"],
    "Governing Law": ["jurisdiction", "law of"],
    "Dispute Resolution": ["arbitration", "dispute"],
    "Force Majeure": ["force majeure"],
    "Intellectual Property": ["intellectual property", "ownership"]
}

def detect_clauses(text):
    detected = set()
    sentences = text.split(".")

    for sentence in sentences[:20]:
        s = sentence.lower()

        # Rule-based
        for clause, keywords in CLAUSE_TYPES.items():
            if any(word in s for word in keywords):
                detected.add(clause)

        # AI-based
        result = classifier(sentence, list(CLAUSE_TYPES.keys()))
        if result["scores"][0] > 0.7:
            detected.add(result["labels"][0])

    return list(detected)