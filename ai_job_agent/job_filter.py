class JobFilter:
    def __init__(self, min_salary=96000, education_required="Associate's degree or equivalent experience", remote_only=True):
        self.min_salary = min_salary
        self.education_required = education_required
        self.remote_only = remote_only

    def filter(self, jobs):
        filtered_jobs = []

        for job in jobs:
            # Salary filter
            if job['salary']:
                try:
                    salary_str = job['salary'].replace("$", "").replace(",", "").split(" ")[0]
                    salary_val = int(salary_str)
                    if salary_val < self.min_salary:
                        continue
                except Exception:
                    pass  # Skip salary filtering if parsing fails

            # Education filter
            if self.education_required and job['education']:
                edu_text = job['education'].lower()
                if "associate" not in edu_text and "experience" not in edu_text:
                    continue

            # Remote filter (simple keyword match)
            if self.remote_only and "remote" not in job['description'].lower():
                continue

            filtered_jobs.append(job)

        return filtered_jobs
