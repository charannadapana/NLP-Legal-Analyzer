from transformers import pipeline
summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6"
)
def generate_summary(text):
    text = text[:1000]
    return summarizer(text, max_length=120, min_length=60)[0]['summary_text']