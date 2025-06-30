from bs4 import BeautifulSoup
import requests
from .scraper_base import JobScraper
from datetime import datetime
import re

class LinkedInScraper(JobScraper):
    BASE_URL = "https://www.linkedin.com"

    def __init__(self, search_terms, filters):
        self.search_terms = search_terms
        self.filters = filters

    def fetch_jobs(self):
        query = "+".join(self.search_terms.split())
        url = f"https://www.linkedin.com/jobs/search/?keywords={query}&location=Remote"
        print(f"[LinkedIn] Fetching from: {url}")

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        job_cards = soup.find_all("li")
        jobs = []

        for idx, card in enumerate(job_cards):
            try:
                title_elem = card.find("h3")
                company_elem = card.find("h4")
                date_elem = card.find("time")
                link_elem = card.find("a", href=True)

                title = title_elem.text.strip() if title_elem else "N/A"
                company = company_elem.text.strip() if company_elem else "N/A"
                date_posted = date_elem['datetime'] if date_elem and date_elem.has_attr('datetime') else str(datetime.now().date())
                link = link_elem['href'] if link_elem else "N/A"
                description_raw = card.get_text(separator=" ", strip=True)
                description = re.sub(r'[*]{3,}', '', description_raw)

                # If too much noise, skip or fallback
                if len(re.findall(r'\*', description)) > len(description) * 0.4:
                    jobs.append({
                        "source": "LinkedIn",
                        "title": title,
                        "company": company,
                        "description": "This job matches but couldn’t be parsed — [See on LinkedIn]",
                        "link": link,
                        "date_posted": date_posted,
                        "salary": None,
                        "education": None
                    })
                else:
                    jobs.append({
                        "source": "LinkedIn",
                        "title": title,
                        "company": company,
                        "description": description,
                        "link": link,
                        "date_posted": date_posted,
                        "salary": None,
                        "education": None
                    })

            except Exception as e:
                print(f"[LinkedIn] Skipping job card due to error: {e}")
                continue

        print(f"[LinkedIn] Found {len(jobs)} job cards for: {self.search_terms}")
        return jobs
