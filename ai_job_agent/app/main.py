import os
from dotenv import load_dotenv
from gpt_evaluator import evaluate_job_post
from user_feedback import record_feedback

# === Load environment variables from .env ===
load_dotenv()

# === Simulated Resume Loader ===
def load_resume():
    return """
Experienced Director of Operations with 18+ years in financial systems, team leadership,
QuickBooks Online, Xero, and performance KPI optimization. Managed global staff, implemented
AI workflows, and delivered measurable cost savings in SaaS, e-commerce, and startup settings.
    """

# === Simulated Job Listing ===
def get_sample_job():
    return {
        "title": "Director of Operations",
        "company": "SaaSCo",
        "location": "Remote",
        "description": """
We’re seeking a Director of Operations to scale our internal processes. This role requires experience
in financial reporting, remote team management, and automation using tools like QuickBooks and Fathom.
Familiarity with AI-based systems and performance metrics is a plus.
        """
    }

# === Main Agent Flow ===
def main():
    resume = load_resume()
    job = get_sample_job()

    result = evaluate_job_post(job, resume, mock_mode=False)

    print("\n=== GPT Evaluation Result ===")
    print(f"Match Score:     {result['match_score']}")
    print(f"Status:          {result['status']}")
    print(f"Reason:          {result['reason']}")
    print(f"Summary:         {result['summary']}")
    print("=============================\n")

    # === Ask User for Feedback ===
    user_input = input("Approve this job? (y = accept, n = reject, u = undecided): ").strip().lower()
    if user_input == "y":
        decision = "accept"
    elif user_input == "n":
        decision = "reject"
    else:
        decision = "undecided"

    reason = input("Optional reason for your decision: ").strip()

    # === Record Feedback ===
    feedback_entry = record_feedback(job, result, decision, reason)
    print(f"\n✓ Feedback saved: {feedback_entry['user_decision']}")

if __name__ == "__main__":
    main()

