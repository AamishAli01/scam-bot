from fastapi import FastAPI, Form
from fastapi.responses import Response

app = FastAPI()

@app.get("/")
def home():
    return {"status": "API running"}

@app.post("/webhook")
def whatsapp_reply(Body: str = Form(...)):
    text = Body.lower()

    if text in ["hi", "hello", "hey"]:
        reply = "Hello 👋 Aamish here! Send me a message."

    elif "win" in text or "free" in text or "lottery" in text:
        reply = "⚠️ Scam detected!"

    else:
        reply = "✅ Message received!"

    return Response(
        content=f"<Response><Message>{reply}</Message></Response>",
        media_type="application/xml"
    )