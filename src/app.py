from fastapi import FastAPI
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

app = FastAPI()

# ✅ HuggingFace model
model_path = "AamishAli/scam-detection-model"

tokenizer = None
model = None

def load_model():
    global tokenizer, model
    if tokenizer is None or model is None:
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSequenceClassification.from_pretrained(model_path)

        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)
        model.eval()

@app.get("/")
def home():
    return {"status": "API running"}

@app.get("/predict")
def predict(text: str):
    load_model()

    # 👋 greeting logic
    text_lower = text.lower()
    if text_lower in ["hi", "hello", "hey"]:
        return {
            "text": text,
            "response": "Hello 👋 Aamish Scam Detector here! Enter your message to check!"
        }

    device = "cuda" if torch.cuda.is_available() else "cpu"

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    outputs = model(**inputs)
    pred = outputs.logits.argmax().item()

    return {
        "text": text,
        "prediction": "scam" if pred == 1 else "safe"
    }