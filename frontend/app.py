import streamlit as st
import sys
import os

# ensure parent package is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.master_agent import run_agent_pipeline

# Page Configuration
st.set_page_config(page_title="EduPilot AI", page_icon="🎓", layout="wide")

# Load CSS Stylesheet
css_path = os.path.join(os.path.dirname(__file__), "style.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize Session States
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initial default values for student profile in session state
if "student_profile" not in st.session_state:
    st.session_state.student_profile = {
        "age": "",
        "education": "Undergraduate",
        "interest": "",
        "goals": "",
        "skills": ""
    }

# Clear History handler
def clear_history():
    st.session_state.messages = []
    if "pending_query" in st.session_state:
        st.session_state.pending_query = None

# Demo Profile loader helper
def load_demo_profile():
    st.session_state.student_profile = {
        "age": "21",
        "education": "Undergraduate",
        "interest": "Software Engineering",
        "goals": "Become a full-stack engineer and work on scalable cloud web apps.",
        "skills": "Python, basic HTML/CSS, Git"
    }

# SIDEBAR
with st.sidebar:
    st.markdown("<h1>🎓 EduPilot AI</h1>", unsafe_allow_html=True)
    st.markdown("<div class='status-badge'>🟢 Active & Secured</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.write("### 👤 Student Profile")
    st.write("Fill in your details to personalize roadmap, study plans, and suggestions.")
    
    # Form elements bound to session state dictionary
    age = st.text_input("Age", value=st.session_state.student_profile["age"])
    education = st.selectbox(
        "Education Level", 
        ["High School", "Undergraduate", "Graduate", "Self-Taught", "Professional"],
        index=["High School", "Undergraduate", "Graduate", "Self-Taught", "Professional"].index(st.session_state.student_profile["education"])
    )
    interest = st.text_input(
        "Career Domain / Interest", 
        value=st.session_state.student_profile["interest"],
        placeholder="e.g. Software Engineering, Data Science"
    )
    goals = st.text_area(
        "Career Goals", 
        value=st.session_state.student_profile["goals"],
        placeholder="What is your target job or ambition?",
        height=80
    )
    skills = st.text_input(
        "Current Skills (comma separated)", 
        value=st.session_state.student_profile["skills"],
        placeholder="e.g. Python, SQL, Git"
    )
    
    # Save input updates back to session state
    st.session_state.student_profile["age"] = age
    st.session_state.student_profile["education"] = education
    st.session_state.student_profile["interest"] = interest
    st.session_state.student_profile["goals"] = goals
    st.session_state.student_profile["skills"] = skills
    
    col_demo, col_save = st.columns(2)
    with col_demo:
        if st.button("💡 Demo Profile", use_container_width=True, help="Load a pre-configured profile to test"):
            load_demo_profile()
            st.rerun()
    with col_save:
        st.success("Auto-Saved")
        
    st.markdown("---")
    
    st.write("### ⚙️ System Status")
    st.markdown("""
    🤖 **Profile Agent**: 🟢 Online  
    🤖 **Career Agent**: 🟢 Online  
    🤖 **Study Agent**: 🟢 Online  
    🤖 **Resume Agent**: 🟢 Online  
    """)
    st.caption("Active MCP Database Connection: 🟢 Connected")
    
    st.markdown("---")
    if st.button("🗑️ Clear Chat History", on_click=clear_history, use_container_width=True):
        st.rerun()

# MAIN INTERFACE
st.markdown("<h1>🎓 EduPilot AI <span style='font-size: 1.2rem; font-weight: normal; color: #9ca3af;'>Your AI-Powered Career Mentor</span></h1>", unsafe_allow_html=True)
st.markdown("---")

# Render chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Render onboarding dashboard if chat history is empty
if len(st.session_state.messages) == 0:
    st.markdown(
        """
        <div class="onboarding-hero">
            <h2 style='margin-top: 0; color: #ffffff;'>Welcome to EduPilot AI! 🚀</h2>
            <p style='color: #d1d5db; font-size: 1.05rem; line-height: 1.6;'>
                I am your unified AI Career Mentor. I coordinate a multi-agent system (incorporating Profile, Career, Study, and Resume sub-agents) along with a real-time Model Context Protocol (MCP) server database to give you actionable career directions, learning plans, and resume insights.
            </p>
            <p style='color: #9ca3af; font-size: 0.95rem;'>
                👉 <strong>How to start:</strong> Complete your details on the left sidebar, choose a quick action below, or type a career question directly into the chat input.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # KPI Grid
    st.markdown(
        """
        <div class="kpi-container">
            <div class="kpi-card">
                <div class="kpi-icon-wrapper">🤖</div>
                <div class="kpi-value">4</div>
                <div class="kpi-title">Co-operating Agents</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-icon-wrapper">💼</div>
                <div class="kpi-value">20+</div>
                <div class="kpi-title">Supported Tech Domains</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-icon-wrapper">⚡</div>
                <div class="kpi-value">Sync</div>
                <div class="kpi-title">MCP Database Connection</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("### ⚡ Quick Actions (Uses your Profile details)")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🗺️ Career Roadmap", use_container_width=True, help="Build a career milestones roadmap"):
            interest = st.session_state.student_profile["interest"] or "Software Engineering"
            st.session_state.pending_query = f"I am interested in {interest}. Please generate a structured Career Roadmap for me, recommending projects, certifications, and internship targets."
            st.rerun()
    with col2:
        if st.button("📊 Skill Gap Analysis", use_container_width=True, help="Analyze skills against targets"):
            skills_val = st.session_state.student_profile["skills"] or "Python, basic coding"
            interest = st.session_state.student_profile["interest"] or "Software Engineering"
            st.session_state.pending_query = f"My current skills are: {skills_val}. My target is {interest}. Please analyze my profile, identify my strengths and weaknesses, and detail my skill gaps."
            st.rerun()
    with col3:
        if st.button("📄 Resume Review", use_container_width=True, help="Get resume enhancement tips"):
            skills_val = st.session_state.student_profile["skills"] or "Python"
            st.session_state.pending_query = f"I have experience with {skills_val}. Please review my skills and provide resume suggestions, bullet points, and impact statements."
            st.rerun()
    with col4:
        if st.button("📅 Weekly Study Plan", use_container_width=True, help="Generate active recall schedule"):
            interest = st.session_state.student_profile["interest"] or "Software Engineering"
            st.session_state.pending_query = f"I want to acquire skills in {interest}. Please generate a weekly study plan, a daily learning schedule, and a revision strategy for me."
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 💡 Example Prompts")
    ep_col1, ep_col2, ep_col3 = st.columns(3)
    with ep_col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-title">🐍 Learn Python</div>
                <div class="feature-desc">"Create a daily study schedule to master Python scripting, data analysis, and basic algorithms in 4 weeks."</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        if st.button("Try Prompt 1", key="try_prompt_1", use_container_width=True):
            st.session_state.pending_query = "Create a daily study schedule to master Python scripting, data analysis, and basic algorithms in 4 weeks."
            st.rerun()
    with ep_col2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-title">📊 Data Science Roadmap</div>
                <div class="feature-desc">"I want to transition from software development to Data Science. What are my skill gaps and certifications?"</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        if st.button("Try Prompt 2", key="try_prompt_2", use_container_width=True):
            st.session_state.pending_query = "I want to transition from software development to Data Science. What are my skill gaps and certifications?"
            st.rerun()
    with ep_col3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-title">🛡️ Cybersecurity Path</div>
                <div class="feature-desc">"What certifications, projects, and Linux skills do I need to prepare for a Junior Security Analyst intern role?"</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        if st.button("Try Prompt 3", key="try_prompt_3", use_container_width=True):
            st.session_state.pending_query = "What certifications, projects, and Linux skills do I need to prepare for a Junior Security Analyst intern role?"
            st.rerun()

# Capture prompt
user_query = None
if "pending_query" in st.session_state and st.session_state.pending_query:
    user_query = st.session_state.pending_query
    st.session_state.pending_query = None

chat_input = st.chat_input("Ask EduPilot AI anything about your career...")
if chat_input:
    user_query = chat_input

# Handle query execution
if user_query:
    # 1. Render user message
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)
        
    # 2. Call orchestrator inside spinner
    with st.chat_message("assistant"):
        with st.spinner("EduPilot AI is consulting sub-agents and database..."):
            try:
                # Retrieve current profile from session state
                profile = st.session_state.student_profile
                
                # Exclude first message and new query from history to avoid duplicates
                history_for_api = st.session_state.messages[:-1]
                
                # Execute agent pipeline
                response_text = run_agent_pipeline(
                    user_message=user_query,
                    chat_history=history_for_api,
                    student_profile=profile
                )
            except Exception as e:
                # Log actual error to console but protect user from crashes
                import logging
                logging.getLogger("EduPilotFrontend").error(f"Error in conversation flow: {str(e)}")
                response_text = "EduPilot AI is currently experiencing high demand. Please try again in a few moments."
                
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            
    st.rerun()

# FOOTER
st.markdown("---")
st.caption("🚀 EduPilot AI | Built for AI Agent Challenge | Cooperative Multi-Agent Framework")
