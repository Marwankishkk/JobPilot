from repositories.job_repository import JobRepository


class JobService:
    def __init__(self):
        self.repo = JobRepository()

    def create_job(self, db, job_data, user_id):
        print("Creating job with data:", job_data)

        # Required fields validation only
        if not job_data.title or not job_data.title.strip():
            raise ValueError("Title is required")

        if not job_data.company or not job_data.company.strip():
            raise ValueError("Company is required")

        if not job_data.location or not job_data.location.strip():
            raise ValueError("Location is required")

        # Normalize optional fields
        description = job_data.description.strip() if job_data.description else None

        job_data.description = description

        return self.repo.create(db, job_data, user_id)
    def get_jobs_by_user(self, db, user_id):
        return self.repo.get_by_user(db, user_id)
    
    def update_job(self, db, job_id, job_data):
        job = self.repo.get_by_id(db, job_id)
        if not job:
            raise ValueError("Job not found")
        
        return self.repo.update(db, job, job_data)
    
    def delete_job(self, db, job_id):
        if not self.repo.get_by_id(db, job_id):
            raise ValueError("Job not found")
        return self.repo.delete(db, job_id)