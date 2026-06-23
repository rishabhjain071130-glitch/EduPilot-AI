import streamlit as st
import sys
import os

# ensure parent package is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.gemini_client import client

st.set_page_config(page_title="EduPilot AI", page_icon="🎓", layout="wide")

# SIDEBAR
with st.sidebar:
    st.title("⚙️ EduPilot AI")
    st.markdown("---")
    st.write("### Features")
    st.write("✅ Profile Analysis")
    st.write("✅ Skill Gap Analysis")
    st.write("✅ Career Roadmap")
    st.write("✅ Weekly Study Plan")
    st.write("✅ Resume Suggestions")
    st.markdown("---")
    st.write("### AI Agents")
    st.write("🤖 Profile Agent")
    st.write("🤖 Career Agent")
    st.write("🤖 Study Agent")
    st.write("🤖 Resume Agent")
    st.markdown("---")
    st.caption("Built for AI Agent Challenge")

# HERO SECTION
st.markdown(
    """
# 🎓 EduPilot AI

### Your AI-Powered Career Mentor

Get personalized career guidance, study plans, skill-gap analysis, resume suggestions and career roadmaps powered by AI.
"""
)

# METRICS
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("AI Agents", "4")
with col2:
    st.metric("Career Domains", "20+")
with col3:
    st.metric("Response Time", "<10 sec")

st.markdown("---")

# FEATURES
st.markdown(
    """
### 🚀 Personalized AI Career Planning

Get instant:

✅ Profile Analysis

✅ Skill Gap Analysis

✅ Career Roadmap

✅ Weekly Study Plan

✅ Resume Suggestions
"""
)

feature1, feature2 = st.columns(2)
with feature1:
    st.info("🎓 Student Profile Analysis")
with feature2:
    st.info("💼 Career Roadmap Generation")

# INPUT
student_details = st.text_area(
    "📝 Enter Student Details",
    height=220,
    placeholder="""
Example:

Age:  Your age

Education: Your current education level: Your coding skills, certifications, projects

Interest: Your career interests 

Goal:   Your career goals

Skills: Python, Networking
""",
)

# BUTTON
if st.button("🚀 Generate AI Career Report"):
    if student_details.strip() == "":
        st.warning("Please enter student details.")
    else:
        with st.spinner("EduPilot AI is analyzing your profile..."):
            prompt = f"""
You are EduPilot AI.

Student:
{student_details}

Provide:

1. Profile Analysis
2. Skill Gap Analysis
3. Career Roadmap
4. Weekly Study Plan
5. Resume Suggestions

Format the response clearly using headings.
"""
            try:
                response = client.models.generate_content(model="gemini-2.5-flash-lite", contents=prompt)
                st.success("Analysis Complete!")
                st.markdown("---")
                st.header("📊 EduPilot AI Report")
                st.markdown(response.text)
            except Exception as e:
                st.error("Gemini API is temporarily unavailable.")
                with st.expander("View Technical Details"):
                    st.code(str(e))

# FOOTER
st.markdown("---")
st.caption("🚀 EduPilot AI | Multi-Agent Career Guidance Platform")
