


import json
import os
from datetime import datetime

FEEDBACK_FILE = os.path.join("memory", "user_feedback.json")

def load_feedback():
    if not os.path.exists(FEEDBACK_FILE):
        return []
    with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_feedback(feedback_entry):
    """
    Append a new feedback entry to the log file.
    """
    data = load_feedback()
    data.append(feedback_entry)
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def record_feedback(job_data, evaluation_result, user_decision, reason=""):
    """
    Combines job data, GPT match evaluation, and user feedback.

    Args:
        job_data (dict): Original scraped job data
        evaluation_result (dict): Result from evaluate_job_post()
        user_decision (str): "accept", "reject", or "undecided"
        reason (str): Optional user comment

    Returns:
        dict: The stored feedback record
    """
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "job_title": job_data.get("title"),
        "company": job_data.get("company"),
        "location": job_data.get("location"),
        "job_description": job_data.get("description"),
        "evaluation_result": evaluation_result,
        "user_decision": user_decision,
        "reason": reason
    }
    save_feedback(entry)
    return entry
