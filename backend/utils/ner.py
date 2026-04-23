import spacy

nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    return text.strip().replace("\n", " ")

def extract_entities(text):
    doc = nlp(text)

    entities = {
        "PERSON": set(),
        "ORG": set(),
        "DATE": set(),
        "MONEY": set(),
        "LOCATION": set()
    }

    for ent in doc.ents:
        value = clean_text(ent.text)

        
        if len(value) < 3:
            continue
        if value.lower() in ["the", "this", "that"]:
            continue

        
        if ent.label_ == "PERSON":
            entities["PERSON"].add(value)

        elif ent.label_ == "ORG":
            entities["ORG"].add(value)

        elif ent.label_ == "DATE":
            entities["DATE"].add(value)

        elif ent.label_ == "MONEY":
            entities["MONEY"].add(value)

        elif ent.label_ in ["GPE", "LOC"]:
            entities["LOCATION"].add(value)

   
    return {k: sorted(list(v)) for k, v in entities.items() if v}