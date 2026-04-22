import streamlit as st
import pickle

# Load model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

st.title("🕵️ Scam Detection AI")
st.write("Paste Your message here & Check")

msg = st.text_area("Enter message:")

if st.button("Check"):
    if msg.strip() != "":
        msg_vec = vectorizer.transform([msg])
        result = model.predict(msg_vec)[0]

        if result == "spam" or result == "scam":
            st.error("🚨 SCAM DETECTED!")
        else:
            st.success("✅ SAFE MESSAGE")
    else:
        st.warning("Please enter a message")