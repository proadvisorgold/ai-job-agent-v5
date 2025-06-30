

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

import json

from dotenv import load_dotenv
from gpt_evaluator import evaluate_job_post
from user_feedback import load_feedback

# === Load environment ===
load_dotenv()

# === File paths ===
RAW_JOBS_FILE = os.path.join("memory", "raw_jobs.json")
EVALUATED_FILE = os.path.join("memory", "evaluated_jobs.json")
CONFIG_FILE = os.path.join("config", "config.json")

# === Load config ===
def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {"review_queue_limit": 10}
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# === Load raw jobs to evaluate ===
def load_raw_jobs():
    if not os.path.exists(RAW_JOBS_FILE):
        return []
    with open(RAW_JOBS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# === Load previously evaluated jobs ===
def load_existing_evaluations():
    if not os.path.exists(EVALUATED_FILE):
        return []
    with open(EVALUATED_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# === Get set of already reviewed titles for filtering ===
def load_reviewed_titles():
    reviewed = load_feedback()
    return {(entry["job_title"], entry["company"]) for entry in reviewed}

# === Main batch processor ===
def main():
    print("🚀 Starting batch GPT evaluation...")

    config = load_config()
    review_limit = config.get("review_queue_limit", 10)

    raw_jobs = load_raw_jobs()
    existing_evals = load_existing_evaluations()
    reviewed_titles = load_reviewed_titles()

    already_queued = {(j["title"], j["company"]) for j in existing_evals}
    processed = []
    count = 0

    for job in raw_jobs:
        key = (job.get("title"), job.get("company"))
        if key in reviewed_titles or key in already_queued:
            continue

        print(f"🔍 Evaluating: {key[0]} at {key[1]}")

        evaluation = evaluate_job_post(job, resume_text="(placeholder resume)", mock_mode=False)

        job_record = {
            "title": job.get("title"),
            "company": job.get("company"),
            "location": job.get("location"),
            "description": job.get("description"),
            "evaluation": evaluation
        }

        processed.append(job_record)
        count += 1

        if count >= review_limit:
            print(f"⚠️ Reached review_queue_limit ({review_limit}) — stopping.")
            break

    # Combine with existing results and write to file
    all_jobs = existing_evals + processed

    with open(EVALUATED_FILE, "w", encoding="utf-8") as f:
        json.dump(all_jobs, f, indent=2)

    print(f"✅ Finished evaluating {count} new job(s).")
    print(f"📂 Output written to: {EVALUATED_FILE}")


if __name__ == "__main__":
    main()
