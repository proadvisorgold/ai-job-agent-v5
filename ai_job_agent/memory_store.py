import json
import os


class MemoryStore:
    def __init__(self, path="data/jobs.json"):
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self.jobs = self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.jobs, f, indent=2)

    def add_jobs(self, new_jobs):
        unique = {job['link']: job for job in self.jobs}
        for job in new_jobs:
            if job['link'] not in unique:
                unique[job['link']] = job
        self.jobs = list(unique.values())
        self.save()

    def get_all_jobs(self):
        return self.jobs

    def clear(self):
        self.jobs = []
        self.save()
