from transformers import pipeline
import re

classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

CLAUSE_TYPES = {
    "Confidentiality Clause": ["confidential", "non-disclosure", "nda"],
    "Termination Clause": ["terminate", "termination"],
    "Payment Terms": ["payment", "fees", "invoice"],
    "Liability Clause": ["liability", "damages"],
    "Governing Law": ["jurisdiction", "law"],
    "Dispute Resolution": ["arbitration", "dispute"],
    "Force Majeure": ["force majeure"],
    "Intellectual Property": ["intellectual property", "ownership"]
}

def split_sentences(text):
    # Better sentence splitting
    return re.split(r'(?<=[.!?]) +', text)


def detect_clauses(text):
    detected = set()
    sentences = split_sentences(text)

    candidate_labels = list(CLAUSE_TYPES.keys())

    for sentence in sentences[:15]:  
        s = sentence.lower()

       
        for clause, keywords in CLAUSE_TYPES.items():
            if any(word in s for word in keywords):
                detected.add(clause)

        if not any(clause in detected for clause in CLAUSE_TYPES):
            result = classifier(sentence, candidate_labels)

            label = result["labels"][0]
            score = result["scores"][0]

            if score > 0.75:   
                detected.add(label)

    return sorted(list(detected))