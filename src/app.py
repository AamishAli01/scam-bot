from fastapi import FastAPI, Form
from fastapi.responses import Response
import pickle
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, "model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "vectorizer.pkl")

model = None
vectorizer = None

def load():
    global model, vectorizer
    if model is None:
        model = pickle.load(open(model_path, "rb"))
        vectorizer = pickle.load(open(vectorizer_path, "rb"))

@app.get("/")
def home():
    return {"status": "API running"}

@app.post("/webhook")
def whatsapp_reply(Body: str = Form(...)):
    load()

    text = Body.lower()

    if text in ["hi", "hello", "hey"]:
        reply = "Hello 👋 Aamish here! Send me a message to check scam."

    else:
        vec = vectorizer.transform([text])
        pred = model.predict(vec)[0]
        reply = "⚠️ Scam detected!" if pred == 1 else "✅ Safe message"

    return Response(
        content=f"<Response><Message>{reply}</Message></Response>",
        media_type="application/xml"
    )