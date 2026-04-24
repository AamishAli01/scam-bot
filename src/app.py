from fastapi import FastAPI, Request
from fastapi.responses import Response
import re

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

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", " link ", text)
    text = re.sub(r"\d+", " number ", text)
    return text

@app.post("/webhook")
async def whatsapp_reply(request: Request):
    global total_messages, scam_count

    try:
        form = await request.form()
        raw_text = form.get("Body", "").strip()
        text = clean_text(raw_text)
        raw_lower = raw_text.lower().strip()

        total_messages += 1

        # ✅ Greeting (FIXED)
        if raw_lower in ["hi", "hello", "hey"]:
            reply = (
                "Hello 👋\n"
                "I'm Aamish AI — your scam detection assistant.\n\n"
                "📩 Send any message and I will analyze whether it appears safe or potentially fraudulent.\n\n"
                "💡 You can send multiple messages anytime."
            )

        else:
            # 🔥 ABUSE DETECTION
            abuse_words = [
                "kutta","kameena","ghada","bkl","behn ka lora","behnchod","donkey","ullu",
                "gandu","gando","loru","chutiya","madrchod","lan","lun","gand maru",
                "idiot","stupid","loser","bsdk","fool","harami","haraamzada","kanjar",
                "randi","kutti","kamina","bewakoof","pagal","mental","jahil",
                "badmaash","badtameez","ghatiya","faltu","nikamma","nalayak",
                "fuck","fucker","shit","bullshit","asshole","bastard","jerk",
                "moron","retard","trash","garbage","scum","dog","pathetic",
                "useless","worthless","idiotic","bloody fool","chodu","lund","lora",
                "gand","chor","dakait","fraud","scammer","dhokebaaz","jhoota","bakwaas"
            ]

            name_variations = ["aamish", "amish"]

            if any(name in text for name in name_variations):
                if any(abuse in text for abuse in abuse_words):
                    reply = (
                        "⚠️ Respect Notice\n\n"
                        "You cannot use abusive language towards my developer.\n\n"
                        "Please keep the conversation respectful. 😠"
                    )
                    return Response(
                        content=f"<Response><Message>{reply}</Message></Response>",
                        media_type="application/xml"
                    )

            # 🔥 SCAM DETECTION
            scam_keywords = [
                "win","won","free","lottery","prize","claim",
                "click","link","urgent","offer","cash",
                "reward","gift","congratulations","selected",

                # phishing
                "verify","account","verification","unauthorized",
                "login attempt","suspended","secure link",
                "bank","security alert","update","confirm identity",
                "limited time","24 hours",

                # Urdu
                "mubarak","inaam","hasil","rabta","foran",
                "jeeto","bisp","rupay","maloomat"
            ]

            matched = [word for word in scam_keywords if word in text]
            score = len(matched)

            if "link" in text:
                score += 1
            if "number" in text:
                score += 1

            if score >= 2 or any(x in text for x in ["verify","unauthorized","bank","login"]):
                scam_count += 1
                reply = (
                    "⚠️ Potential Scam Detected\n\n"
                    "🔍 Analysis:\n"
                    f"- Suspicious keywords identified: {', '.join(matched) if matched else 'pattern detected'}\n"
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

        # ✅ FIXED RETURN (proper indentation)
        return Response(
            content=f"<Response><Message>{reply}</Message></Response>",
            media_type="application/xml",
            headers={"Content-Type": "text/xml"}
        )

    except Exception as e:
        return Response(
            content=f"<Response><Message>Error: {str(e)}</Message></Response>",
            media_type="application/xml"
        )