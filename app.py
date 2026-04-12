import os
import random
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# ---------- Config ----------
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

USE_API = True

if not GOOGLE_API_KEY:
    USE_API = False
else:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")

# ---------- Roles ----------
ROLES = [
    "Software Developer",
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Developer",
    "Data Scientist",
    "Data Analyst",
    "Machine Learning Engineer",
    "AI Engineer",
    "DevOps Engineer",
    "Cyber Security Analyst",
    "Cloud Engineer",
    "HR Interview",
    "Behavioral Interview"
]

# ---------- OFFLINE QUESTION BANK ----------
OFFLINE_QUESTIONS = {
    "Software Developer": [
        "What is OOP? Explain its principles.",
        "What is a REST API?",
        "Difference between list and tuple in Python?",
        "Explain time complexity."
    ],
    "Data Scientist": [
        "What is overfitting?",
        "Explain supervised vs unsupervised learning.",
        "What is a confusion matrix?",
        "What is feature engineering?"
    ],
    "HR Interview": [
        "Tell me about yourself.",
        "What are your strengths and weaknesses?",
        "Why should we hire you?",
        "Where do you see yourself in 5 years?"
    ],
    "Behavioral Interview": [
        "Describe a challenging situation you handled.",
        "Tell me about a time you worked in a team.",
        "How do you handle pressure?",
        "Describe a failure and what you learned."
    ]
}

# ---------- AI / Offline Functions ----------
def generate_question(role, level):
    if USE_API:
        try:
            prompt = f"""
            You are an interviewer for a {role} role.
            Ask ONE {level} level interview question.
            Only give the question.
            """
            response = model.generate_content(prompt)
            return response.text.strip()

        except Exception:
            st.warning("⚠️ API failed. Switching to offline mode.")
    
    # OFFLINE fallback
    return random.choice(OFFLINE_QUESTIONS.get(role, ["Explain a concept you know."]))


def evaluate_answer(question, answer):
    if USE_API:
        try:
            prompt = f"""
            Evaluate this answer:

            Question: {question}
            Answer: {answer}

            Give:
            Score: X/10
            Feedback:
            Improvement:
            """
            response = model.generate_content(prompt)
            return response.text.strip()

        except Exception:
            st.warning("⚠️ API failed. Using offline evaluation.")

    # OFFLINE evaluation
    length = len(answer.split())

    if length > 50:
        score = 8
        feedback = "Good detailed answer."
    elif length > 20:
        score = 6
        feedback = "Decent answer but needs more depth."
    else:
        score = 4
        feedback = "Answer is too short."

    return f"""
Score: {score}/10  
Feedback: {feedback}  
Improvement: Try adding more explanation and examples.
"""

# ---------- UI ----------
st.set_page_config(page_title="AI Interview Bot", page_icon="💼", layout="wide")

st.title("💼 AI Interview Practice Bot")
st.caption("Works with AI + Offline Mode 🚀")

# Session state
if "question" not in st.session_state:
    st.session_state.question = None
if "feedback" not in st.session_state:
    st.session_state.feedback = None

# ---------- Sidebar ----------
with st.sidebar:
    st.header("Interview Settings")

    role = st.selectbox("Select Role", ROLES)
    level = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])

    if st.button("🔄 Generate Question"):
        st.session_state.question = generate_question(role, level)
        st.session_state.feedback = None

# ---------- Main ----------
if st.session_state.question:
    st.subheader("🧠 Interview Question")
    st.markdown(st.session_state.question)

    st.markdown("## ✍️ Answer Section")

    st.info("🎤 Use Windows + H for voice typing or type manually.")

    answer = st.text_area("Your Answer", height=150)

    if st.button("Submit Answer"):
        if answer.strip():
            feedback = evaluate_answer(st.session_state.question, answer)
            st.session_state.feedback = feedback
        else:
            st.warning("Please enter your answer.")

# ---------- Feedback ----------
if st.session_state.feedback:
    st.subheader("📊 Feedback")
    st.markdown(st.session_state.feedback)