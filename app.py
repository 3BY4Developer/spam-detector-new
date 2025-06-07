import streamlit as st
import joblib
import re
from streamlit_lottie import st_lottie
import requests

# Load model and vectorizer
try:
    model = joblib.load('spam_model.pkl')
    vectorizer = joblib.load('vectorizer.pkl')
except:
    st.error("Model files not found. Please run model.py first.")
    st.stop()

# In-memory user store using session_state
if 'USERS' not in st.session_state:
    st.session_state.USERS = {"admin": "admin123", "user": "pass"}

def clean_text(text):
    text = re.sub(r'\W', ' ', text)
    return text.lower()

def predict_spam(text):
    text = clean_text(text)
    vect = vectorizer.transform([text])
    return model.predict(vect)[0]

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def custom_style():
    st.markdown(
        """
        <style>
        body {
            background: linear-gradient(135deg, #f0f4ff 0%, #d9ecff 100%);
        }
        .stButton button {
            background-color: #1f77b4 !important;
            color: white !important;
            border-radius: 10px !important;
            padding: 10px 20px !important;
            font-weight: bold;
        }
        .stTextInput>div>div>input, .stTextArea textarea {
            border: 2px solid #1f77b4 !important;
            border-radius: 10px !important;
        }
        footer {
            text-align: center;
            color: #666;
            font-size: 14px;
            margin-top: 50px;
        }
        .title {
            color: #003366;
            text-align: center;
            font-size: 36px;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def signup():
    st.subheader("📝 Create an Account")
    new_user = st.text_input("New Username", key="signup_user")
    new_pass = st.text_input("New Password", type="password", key="signup_pass")
    if st.button("Sign Up"):
        if new_user and new_pass:
            if new_user in st.session_state.USERS:
                st.warning("⚠️ Username already exists.")
            else:
                st.session_state.USERS[new_user] = new_pass
                st.success("✅ Account created. Please log in.")
        else:
            st.error("Please fill in all fields.")

def login():
    st.subheader("🔐 Login")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    login_btn = st.button("Login")

    if login_btn:
        if st.session_state.USERS.get(username) == password:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.rerun()
        else:
            st.error("Invalid credentials.")

def detector_ui():
    st.subheader("🛡️ Spam Message Detector")
    st.markdown("💡 *Enter your message below to check if it's spam or not.*")
    message = st.text_area("✉️ Your Message:", height=150)
    if st.button("🚀 Detect"):
        if message:
            label = predict_spam(message)
            if label == "spam":
                st.error("⚠️ This message is **SPAM**.")
            else:
                st.success("✅ This message is **NOT spam**.")
        else:
            st.warning("Please enter a message.")

def footer():
    st.markdown("---")
    st.markdown("<footer>✨ Made with ❤️ By AJAY</footer>", unsafe_allow_html=True)

def show_lottie_animation():
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='title'>🎯 Welcome to SpamShield!</div>", unsafe_allow_html=True)
        st.write("🧠 Detect spam messages with the power of Machine Learning.\n🔐 Stay secure and smart.")
    with col2:
        lottie_url = "https://assets4.lottiefiles.com/packages/lf20_h4th9ofg.json"
        lottie_json = load_lottieurl(lottie_url)
        if lottie_json:
            st_lottie(lottie_json, height=220)

def main():
    st.set_page_config(page_title="Spam Detector by AJAY", page_icon="🛡️", layout="centered")
    custom_style()

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        st.sidebar.success(f"✅ Logged in as: {st.session_state.user}")
        show_lottie_animation()
        detector_ui()
    else:
        menu = ["Login", "Sign Up"]
        choice = st.sidebar.radio("🔐 Menu", menu)
        if choice == "Login":
            login()
        elif choice == "Sign Up":
            signup()

    footer()

main()
