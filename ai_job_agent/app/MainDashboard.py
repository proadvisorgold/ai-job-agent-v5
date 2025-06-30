


import streamlit as st
import json
import os
from user_feedback import record_feedback, load_feedback

# === File paths ===
EVALUATED_FILE = os.path.join("memory", "evaluated_jobs.json")
CONFIG_FILE = os.path.join("config", "config.json")

# === Load config ===
def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {"review_queue_limit": 10}
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# === Load jobs with GPT evaluation ===
def load_evaluated_jobs():
    if not os.path.exists(EVALUATED_FILE):
        return []
    with open(EVALUATED_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# === Load already reviewed titles to avoid duplicates ===
def load_reviewed_titles():
    reviewed = load_feedback()
    reviewed_titles = {(entry["job_title"], entry["company"]) for entry in reviewed}
    return reviewed_titles

# === Main Streamlit App ===
def main():
    st.set_page_config(layout="wide")
    st.title("🧠 AI Job Agent – Smart Review Queue")

    config = load_config()
    queue_limit = config.get("review_queue_limit", 10)

    evaluated_jobs = load_evaluated_jobs()
    reviewed_set = load_reviewed_titles()

    # Filter out already-reviewed jobs and limit queue size
    filtered_jobs = [
        job for job in evaluated_jobs
        if (job["title"], job["company"]) not in reviewed_set
    ][:queue_limit]

    if not filtered_jobs:
        st.info("✅ No new jobs to review. All matching posts have been processed or are awaiting new data.")
        return

    for job in filtered_jobs:
        job_id = f"{job['title']} at {job['company']}"
        with st.expander(f"{job_id} ({job.get('location', 'Unknown')})", expanded=False):
            st.markdown(f"**📝 Summary**: {job['evaluation']['summary']}")
            st.markdown(f"**🧠 Match Score**: `{job['evaluation']['match_score']}`")
            st.markdown(f"**🔎 Status**: `{job['evaluation']['status']}`")
            st.markdown(f"**💬 Reason**: {job['evaluation']['reason']}")

            st.markdown("### 📄 Full Job Description")
            st.text_area(
                label="",
                value=job.get("description", "No description available."),
                height=200,
                disabled=True,
            )

            st.markdown("### 🗳 Provide Your Feedback")

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("✅ Accept", key=f"accept_{job_id}"):
                    record_feedback(job, job["evaluation"], "accept", reason="Approved via dashboard")
                    st.success("✓ Feedback saved.")
                    st.experimental_rerun()
            with col2:
                if st.button("❌ Reject", key=f"reject_{job_id}"):
                    record_feedback(job, job["evaluation"], "reject", reason="Rejected via dashboard")
                    st.warning("✗ Feedback saved.")
                    st.experimental_rerun()
            with col3:
                if st.button("🤔 Undecided", key=f"undecided_{job_id}"):
                    record_feedback(job, job["evaluation"], "undecided", reason="Undecided via dashboard")
                    st.info("Feedback saved as undecided.")
                    st.experimental_rerun()

if __name__ == "__main__":
    main()
