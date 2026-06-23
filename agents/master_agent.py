from profile_agent import analyze_profile
from career_agent import generate_career_roadmap
from study_agent import generate_study_plan
from resume_agent import generate_resume
from security import validate_input

from gemini_client import client

print("=== EduPilot AI ===")

user_input = input("\nEnter Student Details:\n")

if not validate_input(user_input):
    print("Invalid Request Detected")
    exit()

profile_prompt = analyze_profile()

career_prompt = generate_career_roadmap()

study_prompt = generate_study_plan()

resume_prompt = generate_resume()

final_prompt = f"""
You are EduPilot AI.

Student:

{user_input}

Tasks:

{profile_prompt}

{career_prompt}

{study_prompt}

{resume_prompt}

Generate a complete response.
"""

response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=final_prompt
)

print("\n")
print(response.text)