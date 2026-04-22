from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import pickle
import re

app = Flask(__name__)

# =========================
# LOAD MODEL
# =========================
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

BOT_NAME = "🤖 Aamish AI Scam Detector Bot"

# =========================
# CLEAN TEXT FUNCTION
# =========================
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text

# =========================
# PREDICTION FUNCTION
# =========================
def predict_message(msg):
    msg = clean_text(msg)
    vec = vectorizer.transform([msg])
    return model.predict(vec)[0]

# =========================
# WHATSAPP ROUTE
# =========================
@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get('Body', '')
    incoming_msg = incoming_msg.strip().lower()

    resp = MessagingResponse()
    msg = resp.message()

    # 🔥 DEBUG (VERY IMPORTANT)
    print("Incoming RAW:", incoming_msg)

    # =========================
    # 👋 WELCOME FIX (BULLETPROOF)
    # =========================
    if any(word in incoming_msg for word in ["hi", "hello", "hey", "start"]):
        reply = f"""👋 Welcome to {BOT_NAME}!
Send me any message and I will tell you if it's SAFE or SCAM 🚨"""

    # =========================
    # 🤖 SCAM CHECK
    # =========================
    else:
        prediction = predict_message(incoming_msg)

        if prediction == "scam":
            reply = f"""{BOT_NAME}
🚨 SCAM DETECTED!
⚠️ This message looks suspicious."""

        else:
            reply = f"""{BOT_NAME}
✅ SAFE MESSAGE
No threat detected."""

    msg.body(reply)
    return str(resp)

# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(port=5000, debug=True)