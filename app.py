import streamlit as st
import joblib
import re

model = joblib.load('spam_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

USER_CREDENTIALS = {
    "admin": "admin123",
    "user": "pass"
}

def clean_text(text):
    text = re.sub(r'\W', ' ', text)
    return text.lower()

def predict_spam(text):
    text = clean_text(text)
    vect = vectorizer.transform([text])
    return model.predict(vect)[0]

def login():
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if USER_CREDENTIALS.get(username) == password:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.success("Logged in!")
        else:
            st.error("Invalid credentials")

def main():
    st.title("🛡️ Spam Detection App")
    st.write("Enter a message to check if it's **Spam** or **Not Spam**.")
    message = st.text_area("Message", height=100)
    if st.button("Detect"):
        if message.strip():
            label = predict_spam(message)
            if label == "spam":
                st.error("⚠️ This message is **SPAM**.")
            else:
                st.success("✅ This message is **Not Spam**.")
        else:
            st.warning("Please enter a message.")

def run_app():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if not st.session_state.logged_in:
        login()
    else:
        st.sidebar.success(f"Logged in as: {st.session_state.user}")
        main()

run_app()
