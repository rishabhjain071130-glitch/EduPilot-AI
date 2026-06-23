import json
import logging
from typing import Dict, Any, List
from mcp.server.fastmcp import FastMCP

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EduPilotMCPServer")

mcp = FastMCP("EduPilot MCP Server")

# Mock database mapping student domains to rich educational content
CAREER_DATABASE: Dict[str, Dict[str, Any]] = {
    "software engineering": {
        "roadmap": "Learn foundational programming (Python/Java), Data Structures & Algorithms, Databases (SQL/NoSQL), Git, and Web Frameworks (Django/React).",
        "certifications": ["AWS Certified Developer", "Google Professional Cloud Developer"],
        "projects": ["Full-stack CRUD application", "Open-source contribution project"],
        "internship_focus": "Junior Software Engineer or Web Developer Intern."
    },
    "data science": {
        "roadmap": "Learn Python/R, Statistics, Data Manipulation (Pandas), Machine Learning (Scikit-Learn), Data Viz (Tableau/Matplotlib), and SQL.",
        "certifications": ["Google Data Analytics Certificate", "TensorFlow Developer Certificate"],
        "projects": ["Exploratory Data Analysis on public datasets", "Predictive Machine Learning model deployment"],
        "internship_focus": "Data Analyst Intern or Junior ML Engineer."
    },
    "cybersecurity": {
        "roadmap": "Learn Networking basics (TCP/IP), Linux command line, Python scripting, security protocols, and ethical hacking tools.",
        "certifications": ["CompTIA Security+", "Certified Ethical Hacker (CEH)"],
        "projects": ["Set up a secure home lab network", "Conduct vulnerability assessments on mock environments"],
        "internship_focus": "Security Analyst Intern or Network Admin Apprentice."
    }
}

STUDY_PLAN_TEMPLATES: Dict[str, Dict[str, str]] = {
    "exam preparation": {
        "weekly_plan": "Weeks 1-2: Concept review and summary notes. Weeks 3-4: Practice questions. Week 5: Full-length mock exams and weak-spot revision.",
        "daily_schedule": "2 hours study block, 30 mins active recall, 15 mins break.",
        "revision_strategy": "Spaced repetition at 1, 3, 7, and 14-day intervals."
    },
    "skill acquisition": {
        "weekly_plan": "Week 1: Fundamentals and syntax. Week 2: Build small practice scripts. Week 3: Understand advanced concepts. Week 4: Capstone project.",
        "daily_schedule": "1 hour learning tutorial, 1 hour hands-on keyboard coding.",
        "revision_strategy": "Build syntax cheat sheets and explain concepts to a peer."
    }
}

RESUME_TEMPLATES: Dict[str, List[str]] = {
    "python": [
        "Include specific libraries used (e.g., Pandas, Flask, Fastapi) rather than just listing 'Python'.",
        "Quantify project achievements: e.g., 'Reduced API latency by 30% using Redis caching'.",
        "Provide a link to a clean, documented GitHub repository."
    ],
    "javascript": [
        "Specify frontend/backend frameworks: e.g., React, Node.js, Express.",
        "Demonstrate hands-on experience with asynchronous operations and API integration.",
        "Include deployment credentials (e.g., hosted live on Vercel/Render)."
    ]
}

@mcp.tool()
def career_advice(student_interest: str) -> str:
    """
    Provide career guidance, structured roadmaps, recommended projects, 
    and certifications based on a student's domain of interest.

    Args:
        student_interest: The student's area of interest (e.g., 'software engineering', 'data science', 'cybersecurity').
    
    Returns:
        A JSON-formatted string containing the roadmap, certs, projects, and internship focus.
    """
    logger.info(f"Received career_advice request for interest: '{student_interest}'")
    
    if not student_interest or not student_interest.strip():
        logger.warning("Empty student interest provided.")
        return json.dumps({"error": "Student interest cannot be empty."})
    
    normalized_interest = student_interest.strip().lower()
    
    # Try to find a matching category
    matched_key = None
    for key in CAREER_DATABASE.keys():
        if key in normalized_interest or normalized_interest in key:
            matched_key = key
            break
            
    if matched_key:
        result = CAREER_DATABASE[matched_key].copy()
        result["category"] = matched_key
        return json.dumps(result, indent=2)
    
    # Fallback response for unsupported career domains
    logger.info(f"Career domain '{student_interest}' not found in database. Returning generic roadmap.")
    fallback = {
        "category": student_interest,
        "roadmap": f"Research and master core fundamentals of {student_interest}. Build hands-on projects and write articles about your learnings.",
        "certifications": ["Look for industry-standard baseline certifications in this field."],
        "projects": [f"Create 2-3 personal portfolio projects demonstrating core {student_interest} skills."],
        "internship_focus": "Target entry-level coordinator or junior associate roles.",
        "note": "Supported direct domains: software engineering, data science, cybersecurity."
    }
    return json.dumps(fallback, indent=2)

@mcp.tool()
def study_plan(goal: str) -> str:
    """
    Generate a structured, actionable study plan (weekly plan, daily schedule, and revision strategy) 
    based on the student's primary educational goal.

    Args:
        goal: The student's learning goal or type of preparation (e.g., 'exam preparation', 'skill acquisition').
    
    Returns:
        A JSON-formatted string detailing the study plan.
    """
    logger.info(f"Received study_plan request for goal: '{goal}'")
    
    if not goal or not goal.strip():
        logger.warning("Empty goal provided.")
        return json.dumps({"error": "Goal cannot be empty."})
        
    normalized_goal = goal.strip().lower()
    
    # Try to match the goal
    matched_key = None
    for key in STUDY_PLAN_TEMPLATES.keys():
        if key in normalized_goal or normalized_goal in key:
            matched_key = key
            break
            
    if matched_key:
        result = STUDY_PLAN_TEMPLATES[matched_key].copy()
        result["goal"] = matched_key
        return json.dumps(result, indent=2)
        
    # Fallback response
    logger.info(f"Goal '{goal}' not found in database. Returning general study guide.")
    fallback = {
        "goal": goal,
        "weekly_plan": "Break your learning content into 4 equal segments. Dedicate one week to each segment, building a small milestone project at the end of each week.",
        "daily_schedule": "Dedicate 90 minutes daily: 45 minutes focused reading/learning, 45 minutes implementation.",
        "revision_strategy": "Write down key concepts from memory after each study session and review them at the start of the next session.",
        "note": "Supported goals: exam preparation, skill acquisition."
    }
    return json.dumps(fallback, indent=2)

@mcp.tool()
def resume_help(skill: str) -> str:
    """
    Provide actionable feedback and improvement suggestions for highlights 
    or keywords associated with a specific tech skill on a student's resume.

    Args:
        skill: The programming language or tool technology (e.g., 'python', 'javascript').
        
    Returns:
        A JSON-formatted string listing resume bullet point suggestions.
    """
    logger.info(f"Received resume_help request for skill: '{skill}'")
    
    if not skill or not skill.strip():
        logger.warning("Empty skill provided.")
        return json.dumps({"error": "Skill cannot be empty."})
        
    normalized_skill = skill.strip().lower()
    
    # Try to match the skill
    matched_key = None
    for key in RESUME_TEMPLATES.keys():
        if key in normalized_skill or normalized_skill in key:
            matched_key = key
            break
            
    if matched_key:
        return json.dumps({
            "skill": matched_key,
            "suggestions": RESUME_TEMPLATES[matched_key]
        }, indent=2)
        
    # Fallback suggestions
    logger.info(f"Skill '{skill}' not found in database. Returning general advice.")
    fallback = {
        "skill": skill,
        "suggestions": [
            f"Add 2 high-impact bullet points describing projects where you applied {skill}.",
            "Use strong action verbs (e.g., 'Implemented', 'Developed', 'Optimized') to begin each point.",
            "Quantify results where possible: specify the metrics, speed improvements, or user counts affected."
        ]
    }
    return json.dumps(fallback, indent=2)

if __name__ == "__main__":
    mcp.run()

