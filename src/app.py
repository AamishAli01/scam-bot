from fastapi import FastAPI, Request
from fastapi.responses import Response

app = FastAPI()

# Home route
@app.get("/")
def home():
    return {"status": "API running"}

# WhatsApp webhook
@app.post("/webhook")
async def whatsapp_reply(request: Request):
    try:
        form = await request.form()
        text = form.get("Body", "").lower()

        # Greeting
        if text in ["hi", "hello", "hey"]:
            reply = "Hello 👋 Aamish here! Send me a message and I’ll check it."

        # Simple scam logic (temporary)
        elif any(word in text for word in ["win", "free", "lottery", "prize"]):
            reply = "⚠️ Scam detected!"

        else:
            reply = "✅ This looks safe."

        # Twilio response format (XML)
        return Response(
            content=f"<Response><Message>{reply}</Message></Response>",
            media_type="application/xml"
        )

    except Exception as e:
        return Response(
            content=f"<Response><Message>Error: {str(e)}</Message></Response>",
            media_type="application/xml"
        )