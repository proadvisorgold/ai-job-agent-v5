import streamlit as st
import sys
import os
import json
import re
from datetime import datetime

# Fix import path to access ai_job_agent from parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai_job_agent.linkedin_scraper import LinkedInScraper
from ai_job_agent.ziprecruiter_scraper import ZipRecruiterScraper
from ai_job_agent.google_jobs_scraper import GoogleJobsScraper

# Load config
with open("config/config.json") as f:
    config = json.load(f)

search_titles = config.get("search_titles", [])
min_salary = config.get("min_salary", 0)
education_filter = config.get("education_filter", "any")

# Set page config and style
st.set_page_config(page_title="AI Job Agent", layout="wide")
st.markdown("<style>" + open("streamlit_app/style.css").read() + "</style>", unsafe_allow_html=True)

st.title("🤖 AI Job Agent v5")

# Filters
with st.sidebar:
    st.header("Search Filters")
    min_salary = st.number_input("Minimum Salary", value=min_salary, step=1000)
    education_filter = st.radio("Education Requirement", ["associate_or_experience", "bachelor", "any"],
                                index=["associate_or_experience", "bachelor", "any"].index(education_filter),
                                format_func=lambda x: {
                                    "associate_or_experience": "Associate / Related Experience",
                                    "bachelor": "Bachelor's Degree",
                                    "any": "Any"
                                }[x])

    if st.button("Clear Results"):
        st.session_state.jobs = []

# Fetch jobs
if st.button("Search Jobs"):
    all_jobs = []
    for title in search_titles:
        all_jobs += LinkedInScraper(title, {"min_salary": min_salary, "education_filter": education_filter}).fetch_jobs()
        all_jobs += ZipRecruiterScraper(title, {"min_salary": min_salary, "education_filter": education_filter}).fetch_jobs()
        all_jobs += GoogleJobsScraper(title, {"min_salary": min_salary, "education_filter": education_filter}).fetch_jobs()

    # Store in session
    st.session_state.jobs = all_jobs

# Display jobs
if "jobs" in st.session_state and st.session_state.jobs:
    for idx, job in enumerate(st.session_state.jobs):
        with st.container():
            st.markdown("---")
            st.subheader(f"🔹 {job['title']} at {job['company']}")
            st.markdown(f"**📅 Posted:** {job.get('date_posted', 'Unknown')}")
            if job.get("salary"):
                st.markdown(f"**💵 Salary:** {job['salary']}")
            if job.get("education"):
                st.markdown(f"**🎓 Education Required:** {job['education']}")

            description = job.get('description', '').strip()
            description = re.sub(r'[*]{3,}', '', description)
            st.text_area("Job Description", description, height=200, key=f"description_{idx}")

            if job.get("link"):
                st.markdown(f"[Apply on original site]({job['link']})", unsafe_allow_html=True)
else:
    st.info("No jobs available. Try adjusting filters and searching.")
