from fastapi import FastAPI, Request
from fastapi.responses import Response

app = FastAPI()

# analytics (temporary memory)
total_messages = 0
scam_count = 0

@app.get("/")
def home():
    return {"status": "API running"}

@app.get("/stats")
def stats():
    return {
        "total_messages": total_messages,
        "scam_detected": scam_count
    }

@app.post("/webhook")
async def whatsapp_reply(request: Request):
    global total_messages, scam_count

    try:
        form = await request.form()
        text = form.get("Body", "").strip().lower()

        total_messages += 1

        # Greeting
        if text in ["hi", "hello", "hey"]:
            reply = (
                "Hello 👋\n"
                "I'm Aamish AI — your scam detection assistant.\n\n"
                "📩 Send any message and I will analyze whether it appears safe or potentially fraudulent.\n\n"
                "💡 You can send multiple messages anytime."
            )

        else:
            scam_keywords = [
                "win", "won", "free", "lottery", "prize", "claim",
                "click", "link", "urgent", "offer", "cash",
                "reward", "gift", "congratulations", "selected",
                "limited", "act now"
            ]

            matched = [word for word in scam_keywords if word in text]

            if matched:
                scam_count += 1
                reply = (
                    "⚠️ Potential Scam Detected\n\n"
                    "🔍 Analysis:\n"
                    f"- Suspicious keywords identified: {', '.join(matched)}\n"
                    "- Message structure resembles common scam patterns\n\n"
                    "🛡️ Recommendation:\n"
                    "Avoid clicking links or sharing personal information.\n\n"
                    "💬 You can send another message for analysis."
                )
            else:
                reply = (
                    "✅ Message appears safe\n\n"
                    "🔍 Analysis:\n"
                    "- No suspicious patterns detected\n\n"
                    "💬 Feel free to send another message for verification."
                )

        return Response(
            content=f"<Response><Message>{reply}</Message></Response>",
            media_type="application/xml"
        )

    except Exception as e:
        return Response(
            content=f"<Response><Message>Error: {str(e)}</Message></Response>",
            media_type="application/xml"
        )