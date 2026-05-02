from repositories.job_repository import JobRepository


class JobService:
    def __init__(self):
        self.repo = JobRepository()

    def create_job(self, db , job_data , user_id):
        if not job_data.title or not job_data.description:
            raise ValueError("Title and description are required")
        
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