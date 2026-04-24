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

        else:
            # Improved scam keywords
            scam_keywords = [
                "win", "won", "free", "lottery", "prize", "claim",
                "click", "link", "urgent", "offer", "cash",
                "reward", "gift", "congratulations", "selected",
                "limited", "act now"
            ]

            if any(word in text for word in scam_keywords):
                reply = "⚠️ Scam detected!"
            else:
                reply = "✅ This looks safe."

        return Response(
            content=f"<Response><Message>{reply}</Message></Response>",
            media_type="application/xml"
        )

    except Exception as e:
        return Response(
            content=f"<Response><Message>Error: {str(e)}</Message></Response>",
            media_type="application/xml"
        )