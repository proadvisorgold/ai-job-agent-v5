import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# === Load .env variables ===
load_dotenv()

# === Initialize OpenAI client ===
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# === Matching threshold (for future use) ===
MATCH_THRESHOLD = 0.75


def evaluate_job_post(job_data, resume_text, memory_examples=None, mock_mode=False):
    """
    Evaluates a job post using OpenAI (or returns mock data if mock_mode=True).

    Args:
        job_data (dict): Job listing data.
        resume_text (str): The full text of the user's resume.
        memory_examples (list): Optional few-shot examples for GPT prompting.
        mock_mode (bool): If True, bypasses GPT and returns mock result.

    Returns:
        dict: {
            "match_score": float,
            "status": "include" | "exclude" | "manual_review",
            "reason": str,
            "summary": str
        }
    """
    if mock_mode:
        return {
            "match_score": 0.87,
            "status": "include",
            "reason": "Strong match based on experience with automation and finance tools.",
            "summary": f"Director of Ops at {job_data.get('company')} with financial/KPI focus"
        }

    prompt = build_prompt(job_data, resume_text, memory_examples)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=prompt,
            temperature=0.4,
            max_tokens=600,
        )

        content = response.choices[0].message.content.strip()
        parsed = json.loads(content)
        return parsed

    except Exception as e:
        return {
            "match_score": 0,
            "status": "manual_review",
            "reason": f"GPT evaluation error: {str(e)}",
            "summary": "Could not evaluate job due to an internal error."
        }


def build_prompt(job_data, resume_text, memory_examples):
    """
    Builds the message prompt for GPT based on job + resume context.

    Args:
        job_data (dict)
        resume_text (str)
        memory_examples (list)

    Returns:
        list: Chat messages formatted for GPT input
    """
    system_msg = {
        "role": "system",
        "content": "You are an expert job-matching assistant. You read job descriptions and determine if they fit a user's background."
    }

    few_shot_msgs = []
    if memory_examples:
        for example in memory_examples:
            few_shot_msgs.append({
                "role": "user",
                "content": f"JOB:\n{example['job']}\n\nRESUME:\n{example['resume']}"
            })
            few_shot_msgs.append({
                "role": "assistant",
                "content": json.dumps(example['result'], indent=2)
            })

    user_msg = {
        "role": "user",
        "content": f"""
Evaluate this job post based on the user's resume.

Return a JSON with: 
- match_score (0.0 to 1.0)
- status ("include", "exclude", "manual_review")
- reason (brief explanation)
- summary (one-line job summary)

JOB:
Title: {job_data.get('title')}
Company: {job_data.get('company')}
Location: {job_data.get('location')}
Description:
{job_data.get('description')}

RESUME:
{resume_text}
        """
    }

    return [system_msg] + few_shot_msgs + [user_msg]
