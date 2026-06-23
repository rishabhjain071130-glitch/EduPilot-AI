import os
import sys

# Ensure parent and current package are importable
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from profile_agent import analyze_profile
from career_agent import generate_career_roadmap
from study_agent import generate_study_plan
from resume_agent import generate_resume
from security import validate_input
from gemini_client import client, generate_content_robust

def run_agent_pipeline(user_message: str, chat_history: list, student_profile: dict = None) -> str:
    """
    Orchestrates the multi-agent career guidance system.
    Validates user input, aggregates guidelines from domain sub-agents,
    and calls the Gemini API client with tool-calling capabilities.
    """
    # 1. Input Safety Validation
    if not validate_input(user_message):
        return (
            "⚠️ Security Notice: Your input has been flagged by our safety system. "
            "Please revise your message to avoid system instructions or commands."
        )

    # 2. Gather profile details
    profile_str = ""
    if student_profile:
        profile_str = (
            f"Student Profile Context:\n"
            f"- Age: {student_profile.get('age', 'Not specified')}\n"
            f"- Education: {student_profile.get('education', 'Not specified')}\n"
            f"- Primary Interest: {student_profile.get('interest', 'Not specified')}\n"
            f"- Career Goals: {student_profile.get('goals', 'Not specified')}\n"
            f"- Current Skills: {student_profile.get('skills', 'Not specified')}\n"
        )
    else:
        profile_str = "Student Profile Context: No details provided yet. Ask the student for their profile if necessary.\n"

    # 3. Retrieve prompt instructions from sub-agents
    profile_instructions = analyze_profile()
    career_instructions = generate_career_roadmap()
    study_instructions = generate_study_plan()
    resume_instructions = generate_resume()

    # 4. Construct unified system instruction
    system_instruction = (
        "You are EduPilot AI, a unified multi-agent career guidance assistant.\n"
        "You coordinate four specialist sub-agents to help the student:\n"
        f"1. Profile Agent guidelines:\n{profile_instructions}\n"
        f"2. Career Agent guidelines:\n{career_instructions}\n"
        f"3. Study Agent guidelines:\n{study_instructions}\n"
        f"4. Resume Agent guidelines:\n{resume_instructions}\n\n"
        "Context and Instructions:\n"
        "- Base your analysis on the provided Student Profile Context.\n"
        "- When the user requests a career roadmap, skill gap analysis, study plan, or resume advice, "
        "always query the relevant MCP tools when available to get validated database entries.\n"
        "- If a student asks for a weekly study plan, search for a match or fallback to a general study guide.\n"
        "- Do not mention the internal agents or tool names directly to the student. Speak as a cohesive, professional mentor.\n"
        "- Keep responses concise, highly practical, and medium length. Use headings, bullet points, and action items. "
        "Avoid long paragraphs (keep them to a maximum of 3 sentences each)."
    )

    # 5. Build contents payload representing conversation history and profile context
    contents_payload = []

    # Insert profile context as initial grounding
    contents_payload.append({
        "role": "user",
        "parts": [{"text": f"Here is the context of the student profile I want you to reference:\n{profile_str}"}]
    })
    contents_payload.append({
        "role": "model",
        "parts": [{"text": "Understood. I will use this student profile context for all career, roadmap, study, and resume advice."}]
    })

    # Append past conversation history
    for msg in chat_history:
        role = "user" if msg["role"] == "user" else "model"
        contents_payload.append({
            "role": role,
            "parts": [{"text": msg["content"]}]
        })

    # Append new user query
    contents_payload.append({
        "role": "user",
        "parts": [{"text": user_message}]
    })

    # 6. Load local MCP server functions dynamically to avoid shadowing conflicts
    import importlib.util
    mcp_tools = []
    try:
        mcp_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mcp", "server.py"))
        spec = importlib.util.spec_from_file_location("local_mcp_server", mcp_path)
        local_mcp_server = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(local_mcp_server)
        mcp_tools = [
            local_mcp_server.career_advice,
            local_mcp_server.study_plan,
            local_mcp_server.resume_help
        ]
    except Exception as e:
        import logging
        logging.getLogger("EduPilotMasterAgent").error(f"Failed to load MCP tools: {str(e)}")

    # 7. Generate content robustly
    response_text = generate_content_robust(
        contents=contents_payload,
        system_instruction=system_instruction,
        tools=mcp_tools
    )

    return response_text

if __name__ == "__main__":
    print("=== EduPilot AI (CLI Mode) ===")
    user_input = input("\nEnter Student Details:\n")
    response = run_agent_pipeline(user_input, chat_history=[], student_profile=None)
    print("\n")
    print(response)