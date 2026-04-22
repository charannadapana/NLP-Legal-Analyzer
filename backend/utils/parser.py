import pdfplumber

def extract_text(file):
    if file.filename.endswith(".pdf"):
        with pdfplumber.open(file.file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
            return text

    return file.file.read().decode("utf-8")