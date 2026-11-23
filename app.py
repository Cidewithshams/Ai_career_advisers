import os
import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Career Advisor", page_icon="🚀", layout="wide")

st.markdown("""
<style>
.stApp {background:#f6f8fc;}
.block-container {max-width:1200px;padding-top:2rem;}
.hero {padding:2rem;border-radius:18px;background:linear-gradient(120deg,#102a43,#245b88);color:white;margin-bottom:1.5rem;}
.hero h1 {color:white;}
.hero p {color:#e5eef8;font-size:1.05rem;}
</style>
<div class="hero">
<h1>🚀 AI Career Advisor</h1>
<p>Discover your strengths. Identify skill gaps. Build your next career step.</p>
</div>
""", unsafe_allow_html=True)

def get_api_key():
    try:
        return st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        return os.getenv("GROQ_API_KEY", "")

def ask_ai(prompt):
    key = get_api_key()
    if not key:
        return ("**Groq API key missing.** Open Streamlit Cloud → Manage app → "
                "Settings → Secrets and add GROQ_API_KEY. Never put the key in GitHub.")
    try:
        client = Groq(api_key=key)
        result = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role":"system","content":
                 "You are a practical AI Career Advisor. Give personalized, realistic guidance with clear headings and actionable steps. Never guarantee jobs or salaries."},
                {"role":"user","content":prompt}
            ],
            temperature=0.7,
            max_tokens=1800
        )
        return result.choices[0].message.content
    except Exception as e:
        return f"**AI request failed:** `{e}`. Check your Groq key and model availability."

st.sidebar.header("👤 Your Career Profile")
name = st.sidebar.text_input("Full name")
education = st.sidebar.selectbox("Education", ["Select education","Matric","Intermediate","Bachelor's","Master's","Other"])
interests = st.sidebar.text_area("Career interests", placeholder="AI, cybersecurity, web development...")
skills = st.sidebar.text_area("Current skills", placeholder="Python, HTML, communication...")
experience = st.sidebar.selectbox("Experience level", ["No experience","Beginner","Intermediate","Experienced"])
goal = st.sidebar.text_input("Career goal", placeholder="Become an AI Engineer")

profile_ready = all([name.strip(), education != "Select education", interests.strip(), skills.strip(), goal.strip()])
profile = f"Name: {name}\nEducation: {education}\nInterests: {interests}\nSkills: {skills}\nExperience: {experience}\nGoal: {goal}"

c1,c2,c3 = st.columns(3)
c1.metric("Career tools","4")
c2.metric("Guidance","Personalized")
c3.metric("Platform","AI-powered")
st.header("Career Development Workspace")
st.write("Complete your profile in the sidebar, then choose a tool.")

tab1,tab2,tab3 = st.tabs(["🧭 Career Recommendations","📊 Skill Gap & Roadmap","💬 AI Career Assistant"])

with tab1:
    st.subheader("Find career paths that match your profile")
    if st.button("Generate Career Recommendations", type="primary"):
        if not profile_ready:
            st.warning("Complete all profile fields in the sidebar first.")
        else:
            with st.spinner("Analyzing your profile..."):
                st.markdown(ask_ai(f"""
{profile}
Recommend 3 to 5 suitable career paths. For each explain why it may fit,
entry-level job roles, skills to learn next, and one beginner project.
Finish with a practical starting recommendation.
"""))

with tab2:
    st.subheader("Identify what to learn next")
    analysis_type = st.radio("Choose analysis", ["Skill Gap Analysis","Learning Roadmap","Job Role Explorer"], horizontal=True)
    if st.button("Generate My Plan", type="primary"):
        if not profile_ready:
            st.warning("Complete all profile fields in the sidebar first.")
        else:
            instructions = {
                "Skill Gap Analysis": "Compare current skills with the career goal. List missing skills by priority, explain why they matter, and suggest practice tasks.",
                "Learning Roadmap": "Create a realistic 12-week learning roadmap with weekly topics, practice tasks, small projects, and revision time.",
                "Job Role Explorer": "Explore 5 relevant job roles. Explain responsibilities, core skills, and a beginner preparation path. Do not guarantee jobs or salaries."
            }
            with st.spinner("Building your plan..."):
                st.markdown(ask_ai(profile + "\n\n" + instructions[analysis_type]))

with tab3:
    st.subheader("Ask your personal career assistant")
    question = st.text_area("Your career question", placeholder="How can I start learning Python for an AI career?")
    if st.button("Ask AI Advisor", type="primary"):
        if not question.strip():
            st.warning("Enter a question first.")
        else:
            with st.spinner("Preparing your answer..."):
                st.markdown(ask_ai(profile + "\n\nQuestion: " + question + "\nGive clear, practical next steps."))

st.divider()
st.caption("AI Career Advisor · Built with Python, Streamlit and Groq")
