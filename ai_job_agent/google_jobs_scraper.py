import requests
from bs4 import BeautifulSoup
from .scraper_base import JobScraper
import re
from urllib.parse import quote


class GoogleJobsScraper(JobScraper):
    def __init__(self, search_terms, filters):
        self.search_terms = search_terms
        self.filters = filters

    def fetch_jobs(self):
        query = quote(f"{self.search_terms} jobs remote")
        url = f"https://www.google.com/search?q={query}"
        print(f"[Google Jobs] Fetching from: {url}")

        headers = {
            "User-Agent": "Mozilla/5.0",
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            jobs = []

            cards = soup.find_all("div", string=re.compile(r"^\w+ at "))
            for card in cards:
                parent = card.find_parent("div")
                title = card.text.strip() if card else "N/A"
                company = "N/A"
                link = url
                description = parent.get_text(separator=" ").strip() if parent else title

                jobs.append({
                    "source": "Google Jobs",
                    "title": title,
                    "company": company,
                    "description": description,
                    "link": link,
                    "date_posted": None,
                    "salary": None,
                    "education": None
                })

            print(f"[Google Jobs] Found {len(jobs)} job cards for: {self.search_terms}")
            return jobs

        except Exception as e:
            print(f"[Google Jobs] Request failed: {e}")
            return []

