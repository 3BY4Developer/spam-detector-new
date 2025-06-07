import streamlit as st
import joblib
import re

# Load model and vectorizer
try:
    model = joblib.load('spam_model.pkl')
    vectorizer = joblib.load('vectorizer.pkl')
except:
    st.error("Model files not found. Please run model.py first.")
    st.stop()

# In-memory user store
USERS = {"admin": "admin123", "user": "pass"}

def clean_text(text):
    text = re.sub(r'\W', ' ', text)
    return text.lower()

def predict_spam(text):
    text = clean_text(text)
    vect = vectorizer.transform([text])
    return model.predict(vect)[0]

def signup():
    st.subheader("Create an Account")
    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type="password")
    if st.button("Sign Up"):
        if new_user and new_pass:
            if new_user in USERS:
                st.warning("Username already exists.")
            else:
                USERS[new_user] = new_pass
                st.success("Account created. Please log in.")
        else:
            st.error("Please fill in all fields.")

def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if USERS.get(username) == password:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.success(f"Welcome {username}!")
        else:
            st.error("Invalid credentials.")

def detector_ui():
    st.subheader("🛡️ Spam Message Detector")
    message = st.text_area("Enter your message:", height=150)
    if st.button("Detect"):
        if message:
            label = predict_spam(message)
            if label == "spam":
                st.error("⚠️ This message is SPAM.")
            else:
                st.success("✅ This message is NOT spam.")
        else:
            st.warning("Please enter a message.")

def footer():
    st.markdown("---")
    st.markdown("<center style='font-size:13px'>Made with ❤️ By AJAY</center>", unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Spam Detector by AJAY", page_icon="🛡️", layout="centered")
    st.title("Spam Detection App 🔍")

    menu = ["Login", "Sign Up"]
    choice = st.sidebar.selectbox("Menu", menu)

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        st.sidebar.success(f"Logged in as: {st.session_state.user}")
        detector_ui()
    else:
        if choice == "Login":
            login()
        elif choice == "Sign Up":
            signup()

    footer()

main()
