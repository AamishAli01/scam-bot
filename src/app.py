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

        total_messages += 1

        # ✅ Greeting (same)
        if any(word in text for word in ["hi", "hello", "hey"]):
            reply = (
                "Hello 👋\n"
                "I'm Aamish AI — your scam detection assistant.\n\n"
                "📩 Send any message and I will analyze whether it appears safe or potentially fraudulent.\n\n"
                "💡 You can send multiple messages anytime."
            )

        else:
            # 🔥 ABUSE DETECTION
            abuse_words = [
               "kutta","Kutta","kameena","Kameena","ghada","Ghada","bkl","BKL","behn ka lora","Behn Ka Lora",
"behnchod","Behnchod","donkey","Donkey","ullu","Ullu","gandu","Gandu","gando","Gando",
"loru","Loru","chutiya","Chutiya","madrchod","Madrchod","lan","Lan","lun","Lun",
"gand maru","Gand Maru","idiot","Idiot","stupid","Stupid","loser","Loser","bsdk","BSDK",
"fool","Fool","harami","Harami","haraamzada","Haraamzada","haraami","Haraami","kanjar","Kanjar",
"kanjri","Kanjri","randi","Randi","kutti","Kutti","kuttiya","Kuttiya","kuttey","Kuttey",
"kamina","Kamina","kamini","Kamini","bewakoof","Bewakoof","bewaqoof","Bewaqoof",
"pagal","Pagal","paagal","Paagal","mental","Mental","jahil","Jahil","jaahil","Jaahil",
"badmaash","Badmaash","badtameez","Badtameez","badsoorat","Badsoorat","ghatiya","Ghatiya",
"ghaleez","Ghaleez","ghalat","Ghalat","faltu","Faltu","nikamma","Nikamma","nalayak","Nalayak",
"ullu ka pattha","Ullu Ka Pattha","ullu ka patha","Ullu Ka Patha","ullu ke pathe","Ullu Ke Pathe",
"chawal","Chawal","charsi","Charsi","nashedi","Nashedi","lafanga","Lafanga","luchcha","Luchcha",
"lucha","Lucha","lanti","Lanti","lanti aadmi","Lanti Aadmi","kameenay","Kameenay","kamino","Kamino",
"besharam","Besharam","beghairat","Beghairat","beghairati","Beghairati","bayghairat","Bayghairat",
"bayhaya","Bayhaya","behaya","Behaya","sharam nahi","Sharam Nahi","tameez nahi","Tameez Nahi",
"fuck","Fuck","fucker","Fucker","fucking","Fucking","shit","Shit","bullshit","Bullshit",
"asshole","Asshole","bastard","Bastard","jerk","Jerk","dumb","Dumb","moron","Moron",
"retard","Retard","trash","Trash","garbage","Garbage","scum","Scum","pig","Pig","dog","Dog",
"cheap","Cheap","low life","Low Life","pathetic","Pathetic","useless","Useless","worthless","Worthless",
"nonsense","Nonsense","idiotic","Idiotic","stupid idiot","Stupid Idiot","bloody fool","Bloody Fool",
"gandi aulaad","Gandi Aulaad","haram ki aulaad","Haram Ki Aulaad","haramzada","Haramzada",
"gandi nasal","Gandi Nasal","kuttay ki aulaad","Kuttay Ki Aulaad","kamini nasal","Kamini Nasal",
"chodu","Chodu","chodu aadmi","Chodu Aadmi","chutiye","Chutiye","chutmar","Chutmar",
"lund","Lund","lunday","Lunday","lunn","Lunn","lora","Lora","loray","Loray","lorey","Lorey",
"gand","Gand","gandi","Gandi","ganday","Ganday","gandi soch","Gandi Soch","gand ka keera","Gand Ka Keera",
"gand ka ilaj","Gand Ka Ilaj","gand phat","Gand Phat","gand fat gayi","Gand Fat Gayi",
"ullu ka dimagh","Ullu Ka Dimagh","dimagh kharab","Dimagh Kharab","dimagh se paidal","Dimagh Se Paidal",
"dimagh ka dahi","Dimagh Ka Dahi","andha","Andha","andhi aulaad","Andhi Aulaad",
"chor","Chor","dakait","Dakait","fraudiya","Fraudiya","fraud","Fraud","scammer","Scammer",
"dhokebaaz","Dhokebaaz","dhokeybaaz","Dhokeybaaz","jhoota","Jhoota","jhooti","Jhooti",
"bakwaas","Bakwaas","bakwaasi","Bakwaasi","faltu baat","Faltu Baat"
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

            # 🔥 MULTI-LANGUAGE SCAM DETECTION
            scam_keywords = [
                 # basic
                "win", "won", "free", "lottery", "prize", "claim",
                "click", "link", "urgent", "offer", "cash",
                "reward", "gift", "congratulations", "selected",

                # 🔥 phishing / banking
                "verify", "verify account", "account verification",
                "unauthorized", "login attempt", "suspended",
                "secure link", "bank account", "security alert",
                "update details", "confirm identity",
                "limited time", "within 24 hours",

                # Urdu / Roman Urdu
                "mubarak", "inaam", "hasil", "rabta", "foran",
                "jeeto", "bisp", "rupay", "maloomat"
            ]

            matched = [word for word in scam_keywords if word in text]

            score = len(matched)

            # extra signals
            if "link" in text:
                score += 1
            if "number" in text:
                score += 1

            if score >= 2 or "verify" in text or "unauthorized" in text:
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