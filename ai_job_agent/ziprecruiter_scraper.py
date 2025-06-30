from bs4 import BeautifulSoup
import requests
from .scraper_base import JobScraper
from datetime import datetime
import re


class ZipRecruiterScraper(JobScraper):
    BASE_URL = "https://www.ziprecruiter.com"

    def __init__(self, search_terms, filters):
        self.search_terms = search_terms if isinstance(search_terms, list) else [search_terms]
        self.filters = filters

    def fetch_jobs(self):
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        all_jobs = []

        for term in self.search_terms:
            query = "+".join(term.strip().split())
            url = f"https://www.ziprecruiter.com/jobs-search?search={query}&location=Remote"
            print(f"[ZipRecruiter] Fetching from: {url}")

            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"[ZipRecruiter] Request failed: {e}")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            job_elements = soup.select("div.job_content") or soup.select("article.job_result")
            print(f"[ZipRecruiter] Found {len(job_elements)} job cards for: {term}")

            for card in job_elements:
                try:
                    title_elem = card.select_one("a.job_link")
                    company_elem = card.select_one("a.t_org_link") or card.select_one("span.t_org_link")
                    location_elem = card.select_one("span.location") or card.select_one("span.loc")
                    date_elem = card.select_one("time")
                    snippet_elem = card.select_one("p.job_snippet") or card.select_one("div.job_snippet")

                    job_title = title_elem.text.strip() if title_elem else "N/A"
                    company = company_elem.text.strip() if company_elem else "N/A"
                    location = location_elem.text.strip() if location_elem else "N/A"
                    date_posted = date_elem["datetime"] if date_elem and "datetime" in date_elem.attrs else str(datetime.now().date())
                    link = title_elem["href"] if title_elem and "href" in title_elem.attrs else "N/A"

                    # Normalize the link if it's relative
                    if link.startswith("/"):
                        link = f"{self.BASE_URL}{link}"

                    # Extract and clean the snippet
                    raw_snippet = snippet_elem.get_text(separator=" ").strip() if snippet_elem else ""
                    clean_snippet = re.sub(r'[*|•–—]{2,}', ' ', raw_snippet)
                    clean_snippet = re.sub(r'\s{2,}', ' ', clean_snippet).strip()

                    if len(clean_snippet) < 20:
                        description = f"This job matches your title search but couldn't be parsed — [See on ZipRecruiter]({link})"
                    else:
                        description = f"{job_title} at {company} — {location}\n\n{clean_snippet}"

                    all_jobs.append({
                        "source": "ZipRecruiter",
                        "title": job_title,
                        "company": company,
                        "description": description,
                        "link": link,
                        "date_posted": date_posted,
                        "salary": None,
                        "education": None
                    })

                except Exception as e:
                    print(f"[ZipRecruiter] Skipping job card due to error: {e}")
                    continue

        return all_jobs

