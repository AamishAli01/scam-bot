from fastapi import FastAPI
import pickle

app = FastAPI()

# load model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

@app.get("/")
def home():
    return {"status": "API running"}

@app.get("/predict")
def predict(text: str):
    text_lower = text.lower()

    # greeting
    if text_lower in ["hi", "hello", "hey"]:
        return {
            "response": "Hello 👋 Aamish Scam Detector here! Enter your message to check!"
        }

    # prediction
    vec = vectorizer.transform([text])
    pred = model.predict(vec)[0]

    return {
        "text": text,
        "prediction": "scam" if pred == 1 else "safe"
    }