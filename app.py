import streamlit as st
import google.generativeai as genai
import json
import re

# --- Config ---
st.set_page_config(page_title="EduGenie - Gemini Learning Assistant")
genai.configure(api_key=st.secrets.get("GEMINI_API_KEY", "YOUR_API_KEY_HERE"))
model = genai.GenerativeModel("gemini-1.5-pro")

st.title("EduGenie - Gemini Learning Assistant")
st.write("AI Powered Learning - Built with Gemini 1.5 Pro")

# --- Module 1: Explanation Module ---
def explain_topic(topic):
    prompt = f"Explain the topic '{topic}' in a simple way for a beginner student."
    response = model.generate_content(prompt)
    return response.text

# --- Module 2: QnA Module ---
def answer_question_with_gemini(context, question):
    prompt = f"Based on this context: {context}\nAnswer this question: {question}"
    response = model.generate_content(prompt)
    return response.text

# --- Module 3: Summary Module ---
def summarize_text(text):
    prompt = f"Summarize this text in short points: {text}"
    response = model.generate_content(prompt)
    return response.text

# --- Module 4: Quiz Module ---
def clean_json_block(text):
    # Remove ```json ``` blocks if present
    cleaned = re.sub(r'```json|```', '', text).strip()
    return cleaned

def generate_quiz(passage):
    prompt = f"""
    Create 3 Multiple Choice Questions with 4 options from this passage: {passage}
    Return ONLY in JSON format like:
    [{{"question": "...", "options": ["A","B","C","D"], "answer": "A"}}]
    """
    response = model.generate_content(prompt)
    cleaned = clean_json_block(response.text)
    try:
        return json.loads(cleaned)
    except:
        return cleaned

# --- Module 5: Learning Path Module ---
def get_learning_recommendations(topic):
    prompt = f"Create a learning path from beginner to advanced for the topic: {topic}"
    response = model.generate_content(prompt)
    return response.text

# --- Streamlit UI ---
menu = st.sidebar.selectbox("Select Module", ["Explanation", "QnA", "Quiz", "Summary", "Learning Path"])

if menu == "Explanation":
    topic = st.text_input("Enter Topic")
    if st.button("Explain"):
        st.success(explain_topic(topic))

if menu == "QnA":
    context = st.text_area("Enter Passage/Context")
    question = st.text_input("Enter Question")
    if st.button("Ask Question"):
        st.success(answer_question_with_gemini(context, question))

if menu == "Summary":
    text = st.text_area("Enter Text to Summarize")
    if st.button("Summarize"):
        st.success(summarize_text(text))

if menu == "Quiz":
    passage = st.text_area("Enter Passage for Quiz")
    if st.button("Generate Quiz"):
        st.json(generate_quiz(passage))

if menu == "Learning Path":
    topic = st.text_input("Enter Topic for Learning Path")
    if st.button("Get Path"):
        st.success(get_learning_recommendations(topic))
