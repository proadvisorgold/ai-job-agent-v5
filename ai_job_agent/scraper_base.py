from abc import ABC, abstractmethod


class JobScraper(ABC):
    """
    Base class for job scrapers.
    All derived classes must implement fetch_jobs().
    """

    @abstractmethod
    def fetch_jobs(self):
        """
        Must return a list of job dictionaries with keys:
        - title
        - company
        - description
        - link
        - date_posted
        - salary
        - education
        - source
        """
        pass

